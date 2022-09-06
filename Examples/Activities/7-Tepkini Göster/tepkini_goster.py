from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import utime
import urandom

WIDTH  = 128                                            
HEIGHT = 64

sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(128, 64, i2c)
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led = Pin(7,Pin.OUT)

pressed = False

oled.fill(0)
oled.show()
oled.text("Press the button",0,10)
oled.text("TO START!",25,35)
oled.show()

def button_handler(pin):
    global pressed
    if not pressed:
        timer_reaction= utime.ticks_diff(utime.ticks_ms(), timer_start)
        oled.fill(0)
        oled.show()
        oled.text("Your Time",15,30)
        oled.text(str(timer_reaction), 20, 40)
        oled.show()

led.value(0)
utime.sleep(urandom.uniform(1,5))
led.value(1)
timer_start=utime.ticks_ms()

button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)