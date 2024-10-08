from machine import Pin, PWM, I2C
from picobricks import MotorDriver
import utime

CLOSED_POSITION = 110
OPEN_POSITION = 10

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

motor.servo(1,CLOSED_POSITION)

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
   print(distance,"cm")
   return distance

while True:
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
