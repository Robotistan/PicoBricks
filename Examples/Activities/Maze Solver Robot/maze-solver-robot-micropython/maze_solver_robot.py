from machine import Pin
from utime import sleep
import utime
#define libraries

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
#define sensor pins

m1 = Pin(21, Pin.OUT)
m2 = Pin(22, Pin.OUT)
#define dc motor pins

m1.low()
m2.low()
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
        m1.high()
        m2.high()
        sleep(1) #if the distance is higher than 5, the wheels go straight
    else:
        m1.low()
        m2.low()
        sleep(0.5)
        m1.high()
        m2.low()
        sleep(0.5)
        measure=int(getDistance())
        if measure<5:
            m1.low()
        m2.low()
        sleep(0.5)
        m1.low()
        m2.high()
        sleep(0.5)
        #If the distance is less than 5, wait, move in any direction; if the distance is less than 5, move in the opposite direction
