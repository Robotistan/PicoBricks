from machine import Pin, I2C,Timer
from picobricks import SSD1306_I2C
import utime
import urandom
#define the library
WIDTH=128
HEIGHT=64
#define the width and height values
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=2000000)
oled= SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led=Pin(7,Pin.OUT)
#define our input and output pins
while True:
    led.value(0)
    oled.fill(0)
    oled.text("press the button",0,10)
    oled.text("TO START!",25,25)
    oled.show()
    #print "Press the button" and "TO START!" on the OLED screen
    while button.value()==0:
        pass
    oled.fill(0)
    oled.text("Wait For LED",15,30)
    oled.show()
    #write "wait for LED" on the screen when the button is pressed
    utime.sleep(urandom.uniform(1,5))
    led.value(1)
    timer_start=utime.ticks_ms()
    #wait for a rondom second and turn on the led
    while button.value()==0:
        pass
    timer_reaction=utime.ticks_diff(utime.ticks_ms(), timer_start)
    pressed=True
    oled.fill(0)
    oled.text("Your Time",25,25)
    oled.text(str(timer_reaction),50,50)
    oled.show()
    led.value(0)
    utime.sleep(1.5)
    #print the score and "Your Time" to the screen when the button is pressed.
