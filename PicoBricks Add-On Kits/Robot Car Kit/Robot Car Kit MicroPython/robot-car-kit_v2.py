from machine import Pin, PWM, ADC, I2C
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import utime
import time
from picobricks import NEC_16,IR_RX, MotorDriver

#HC-SR04 
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

MAX_LEN = 10
buffer = bytearray()
ble_data = bytearray(5)
ble_data[0] = 72
ble_data[1] = 1
ble_data[2] = 4

sonic = False
dance = False

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def constrain(x, min_val, max_val):
    return max(min(x, max_val), min_val)

def joystick_move(left_speed, right_speed):
    if right_speed > 0:
        if right_speed < 100:
            right_speed = 100
        motor.dc(2,right_speed,1)
    else:
        if -right_speed < 100:
            right_speed = -100
        right_speed = abs(right_speed)
        motor.dc(2,right_speed,0)

    if left_speed > 0:
        if left_speed < 100:
            left_speed = 100
        motor.dc(1,left_speed,1)
    else:
        if -left_speed < 100:
            left_speed = -100
        left_speed = abs(left_speed)
        motor.dc(1,left_speed,0)
        
def getDistance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
       signaloff = utime.ticks_us()
    while echo.value() == 1:
       signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    utime.sleep(0.1)
    #print(distance,"cm")
    return distance

def ir_callback(data, addr, ctrl):
    global ir_data
    global ir_addr, data_rcvd
    if data > 0:
        ir_data = data
        ir_addr = addr
        print('Data {:02x} Addr {:04x}'.format(data, addr))
        data_rcvd = True
        
ir = NEC_16(Pin(0, Pin.IN), ir_callback)
ir_data = 0
data_rcvd = False

def on_rx(data):
    global buffer

    for b in data:
        buffer.append(b)
        if len(buffer) > MAX_LEN:
            buffer = buffer[1:]
#           print("BUFFER:", buffer)
sp.on_write(on_rx)

motor.dc(1,0,0)
motor.dc(2,0,0)

while True:
    if sp.is_connected():
        distance = int(getDistance())
        dist_bytes = distance.to_bytes(2, 'little')
        ble_data[3] = dist_bytes[0]
        ble_data[4] = dist_bytes[1]
        
        sp.send(bytes(ble_data))
        if sonic == True:
            if (getDistance()) > (12):
                #forward
                motor.dc(1,255,0)
                motor.dc(2,255,0)
            else:
                #stop
                motor.dc(1,0,0)
                motor.dc(2,0,0)
                time.sleep((0.5))
                #backward
                motor.dc(1,255,1)
                motor.dc(2,255,1)
                time.sleep((0.1))
                #stop
                motor.dc(1,0,0)
                motor.dc(2,0,0)
                time.sleep((0.2))
                #left
                motor.dc(1,0,0)
                motor.dc(2,190,0)
                time.sleep(0.5)
                #stop
                motor.dc(1,0,0)
                motor.dc(2,0,0)
        if dance == True:
                #forward
                motor.dc(1,255,0)
                motor.dc(2,255,0)
                time.sleep(1)
                #backward
                motor.dc(1,255,1)
                motor.dc(2,255,1)
                time.sleep(1)
                #left
                motor.dc(1,0,0)
                motor.dc(2,255,0)
                time.sleep(2)
                #right
                motor.dc(1,255,0)
                motor.dc(2,0,0)
                time.sleep(2)
        if buffer:
            print(buffer[2])
            if (buffer[0] == 72 and buffer[1] == 1):
                if (buffer[2] == 1): #Joystick
                    if((buffer[3] == 0) and (buffer[4] == 0)):
                        motor.dc(1,0,0)
                        motor.dc(2,0,0)
                    else:
                        xValue = buffer[3]
                        yValue = buffer[4]
                        
                        mappedX = map_value(xValue, 0, 255, -255, 255)
                        mappedY = map_value(yValue, 0, 255, -255, 255)
                        
                        leftMotorSpeed = mappedY + mappedX
                        rightMotorSpeed = mappedY - mappedX

                        leftMotorSpeed = constrain(leftMotorSpeed, -255, 255)
                        rightMotorSpeed = constrain(rightMotorSpeed, -255, 255)
                                     
                        joystick_move(leftMotorSpeed, rightMotorSpeed)
                if (buffer[2] == 2): #Sonic
                    sonic = True
                if (buffer[2] == 3): #Dance
                    dance = True
                if (buffer[2] == 99):
                    sonic = False
                    dance = False
                    motor.dc(1,0,0)
                    motor.dc(2,0,0)
            buffer[:] = b''
        time.sleep(0.2)
    if data_rcvd == True: #remote mode
        data_rcvd = False
        if (getDistance()) < (10):
            stop()
            time.sleep((1))
            backward()
        elif ir_data == IR_RX.number_up: #forward
            motor.dc(1,255,0)
            motor.dc(2,255,0)
        elif ir_data == IR_RX.number_down: #backward
            motor.dc(1,255,1)
            motor.dc(2,255,1)
        elif ir_data == IR_RX.number_left: #left
            motor.dc(1,0,0)
            motor.dc(2,255,0)
        elif ir_data == IR_RX.number_right: #right
            motor.dc(1,255,0)
            motor.dc(2,0,0)
        elif ir_data == IR_RX.number_ok: #stop
            motor.dc(1,0,0)
            motor.dc(2,0,0)



