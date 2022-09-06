from machine import Pin, PWM, I2C
from utime import sleep
from ssd1306 import SSD1306_I2C
import utime

redLed=Pin(7,Pin.OUT)
button=Pin(10,Pin.IN,Pin.PULL_DOWN)
buzzer=PWM(Pin(20,Pin.OUT))
buzzer.freq(392)
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

WIDTH  = 128                                            
HEIGHT = 64                                          
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(128, 64, i2c)
measure=0
finalDistance=0

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

def getMeasure(pin):
    global measure
    global finalDistance
    redLed.value(1)
    for i in range(20):
        measure += getDistance()
        sleep(0.05)
    redLed.value(0)
    finalDistance = (measure/20) + 6
    oled.fill(0)
    oled.show()
    oled.text(">Digital Ruller<", 2,5)
    oled.text("Distance " + str(round(finalDistance)) +" cm", 0, 32)
    oled.show()
    print(finalDistance)
    buzzer.duty_u16(4000)
    sleep(0.05)
    buzzer.duty_u16(0)
    measure=0
    finalDistance=0
    
button.irq(trigger=machine.Pin.IRQ_RISING, handler=getMeasure)