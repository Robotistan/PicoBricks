from machine import Pin, I2C, Timer
from picobricks import SSD1306_I2C
import utime
import urandom

WIDTH  = 128                                            
HEIGHT = 64

sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=2000000)
oled = SSD1306_I2C(128, 64, i2c)
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
led = Pin(7,Pin.OUT)


while True:
    led.value(0)
    oled.fill(0)
    oled.text("Press the button",0,10)
    oled.text("TO START!",25,35)
    oled.show()
    while button.value() == 0:
        pass
    oled.fill(0)
    oled.text("Wait For LED",15,30)
    oled.show()
    utime.sleep(urandom.uniform(1,5))
    led.value(1)
    timer_start = utime.ticks_ms()
    while button.value() == 0:
        pass
    timer_reaction= utime.ticks_diff(utime.ticks_ms(), timer_start)
    pressed = True
    oled.fill(0)
    oled.text("Your Time",25,25)
    oled.text(str(timer_reaction), 50, 40)
    oled.show()
    led.value(0)
    utime.sleep(1.5)
    