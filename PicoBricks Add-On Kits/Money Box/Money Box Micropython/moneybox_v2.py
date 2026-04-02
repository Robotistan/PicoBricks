from machine import Pin, PWM, I2C
from picobricks import MotorDriver
import utime
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

CLOSED_POSITION = 110
OPEN_POSITION = 10

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

motor.servo(1,CLOSED_POSITION)

MAX_LEN = 10
buffer = bytearray()
ble_data = bytearray(5)
ble_data[0] = 72
ble_data[1] = 2
ble_data[2] = 3

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

trashDetected = 0
distance = 100

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
#    print(distance,"cm")
   return distance

def on_rx(data):
    global buffer

    for b in data:
        buffer.append(b)
        if len(buffer) > MAX_LEN:
            buffer = buffer[1:]

#     print("BUFFER:", buffer)

sp.on_write(on_rx)

while True:
    if sp.is_connected():
        distance = int(getDistance())
        dist_bytes = distance.to_bytes(2, 'little')
        ble_data[3] = dist_bytes[0]
        ble_data[4] = dist_bytes[1]
        sp.send(bytes(ble_data))
        if buffer:
            if (buffer[0] == 72 and buffer[1] == 2 and buffer[2] == 1): #Up
                motor.servo(1,OPEN_POSITION)
            elif (buffer[0] == 72 and buffer[1] == 2 and buffer[2] == 2): #Down
                motor.servo(1,OPEN_POSITION)
			buffer[:] = b''
        utime.sleep(0.5)
    else:
        rawDistance = getDistance()
        if rawDistance < 1200:
            distance = rawDistance
        motor.servo(1,CLOSED_POSITION)
        if (distance < 9):
            trashDetected = 1
            utime.sleep(0.3)
        
        if (distance > 13) and trashDetected == 1:
            trashDetected = 0
            motor.servo(1,OPEN_POSITION)
            utime.sleep(0.5)
        utime.sleep(0.5)

