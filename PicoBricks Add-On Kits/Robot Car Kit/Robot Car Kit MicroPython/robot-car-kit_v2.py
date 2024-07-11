from time import sleep
from machine import Pin, PWM, ADC, I2C
import utime
import time
from picobricks import NEC_16,IR_RX, MotorDriver

#HC-SR04 
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

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

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

def forward():
    motor.dc(1,255,0)
    motor.dc(2,255,0)

def stop():
    motor.dc(1,0,0)
    motor.dc(2,0,0)

def backward():
    motor.dc(1,255,1)
    motor.dc(2,255,1)

def right():
    motor.dc(1,255,0)
    motor.dc(2,0,0)

def left():
    motor.dc(1,0,0)
    motor.dc(2,255,0)
    
while True:
    #print(getDistance())
    if data_rcvd == True:
        data_rcvd = False
        if ir_data == IR_RX.number_up:
            forward()
        elif ir_data == IR_RX.number_down:
            backward()
        elif ir_data == IR_RX.number_left:
            left()
        elif ir_data == IR_RX.number_right:
            right()
        elif ir_data == IR_RX.number_ok:
            stop()
    if (getDistance()) < (10):
        stop()
        time.sleep((1))
        backward()
