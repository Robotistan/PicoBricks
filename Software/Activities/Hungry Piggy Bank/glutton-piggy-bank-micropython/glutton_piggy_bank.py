from machine import Pin, PWM
import utime
#define the libraries

servo=PWM(Pin(21,Pin.OUT))
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
#define the input and output pins

servo.freq(50)
servo.duty_u16(6750)

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
#calculate distance
while True:
    utime.sleep(0.01)
    if int(getDistance())<=5:  #if the distance variable is less than 5
        servo.duty_u16(4010) 
        utime.sleep(0.3)  #wait
        servo.duty_u16(6750)  
