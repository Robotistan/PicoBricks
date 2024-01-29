from machine import Pin, PWM
import utime

CLOSED_POSITION = 6600
OPEN_POSITION = 3000

servo=PWM(Pin(21,Pin.OUT))
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

servo.freq(50)
servo.duty_u16(CLOSED_POSITION) #15 degree

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
    servo.duty_u16(CLOSED_POSITION)
    if (distance < 9):
        trashDetected = 1
        utime.sleep(0.3)
    
    if (distance > 13) and trashDetected == 1:
        trashDetected = 0
        servo.duty_u16(OPEN_POSITION)
        utime.sleep(0.5)