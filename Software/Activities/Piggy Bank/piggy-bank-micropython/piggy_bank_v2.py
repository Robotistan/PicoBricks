from machine import Pin, PWM, I2C
import utime
#define the libraries

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
#define the input and output pins

motor.servo(1,110)

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
        motor.servo(1,110)
        utime.sleep(1)  #wait
    else:
        motor.servo(1,180) 
