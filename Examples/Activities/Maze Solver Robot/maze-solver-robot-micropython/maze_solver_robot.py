from machine import Pin,
from utime import sleep
import utime

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

m1 = Pin(21, Pin.OUT)
m2 = Pin(22, Pin.OUT)

m1.low()
m2.low()
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
measue=0
while True:
    measure=int(getDistance())
    m1.high()
    m2.high()
    if measure<10:
        m1.low()
        m2.low()
        sleep(1)
        m1.high()
        m2.low()
        sleep(0.5)
        measure=int(getDistance())
        if measure<10:
            m1.low()
            m2.low()
            sleep(1)
            m1.low()
            m2.high()
            sleep(1)