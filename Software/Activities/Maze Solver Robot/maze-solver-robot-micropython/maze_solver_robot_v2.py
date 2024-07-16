from machine import Pin, I2C
from picobricks import MotorDriver
from utime import sleep
import utime
#define libraries

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
#define sensor pins

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

motor.dc(1,0,0)
motor.dc(2,0,0)
signaloff = 0
signalon = 0

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
   return distance
#calculate distance

measure=0
while True:
    measure=int(getDistance())
    print(measure)
    if measure>5:
		motor.dc(1,255,0)
		motor.dc(2,255,0)
        sleep(1) #if the distance is higher than 5, the wheels go straight
    else:
		motor.dc(1,0,0)
		motor.dc(2,0,0)
        sleep(0.5)
        motor.dc(1,255,0)
        motor.dc(2,0,0)
        sleep(0.5)
        measure=int(getDistance())
        if measure<5:
            motor.dc(1,0,0)
        motor.dc(2,0,0)
        sleep(0.5)
        motor.dc(1,0,0)
        motor.dc(2,255,0)
        sleep(0.5)
        #If the distance is less than 5, wait, move in any direction; if the distance is less than 5, move in the opposite direction
