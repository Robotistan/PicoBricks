from machine import Pin, PWM, I2C
from utime import sleep
from picobricks import SSD1306_I2C
import utime
#define the libraries
servo=PWM(Pin(21,Pin.OUT))

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
pos = 5000

servo.freq(50)

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
#calculate the distance
    
while True:
    utime.sleep(0.01)
    if int(getDistance())<=5:
        while pos < 7500:
            pos +=2
            servo.duty_u16(pos) #70 degree
            utime.sleep(0.001)
        utime.sleep(2)
    else:
        while pos > 5000:
            pos -=2
            servo.duty_u16(pos) #70 degree
            utime.sleep(0.001)
