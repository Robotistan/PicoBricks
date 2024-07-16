from machine import Pin, PWM, I2C
from picobricks import MotorDriver
import utime

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

position = 110
motor.servo(1,position)

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
   print("The distance from object is ",distance,"cm")
   return distance

while True:
    utime.sleep(0.01)
    if int(getDistance())<=5:
	    while position < 180: #open
            position +=2
            motor.servo(1,position)
            utime.sleep(0.02)
        utime.sleep(2)
    else:
        while position > 110: #close
            position -=2
            motor.servo(1,position)
            utime.sleep(0.02)
