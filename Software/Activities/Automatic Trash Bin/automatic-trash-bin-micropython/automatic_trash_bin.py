from machine import Pin, PWM
from utime import sleep

servo=PWM(Pin(21,Pin.OUT))
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

servo.freq(50)
servo.duty_u16(1920) #15 degree

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
    sleep(0.01)
    if int(getDistance())<=10:
        servo.duty_u16(4010) #70 degree
        utime.sleep(0.3)
        servo.duty_u16(1920)
