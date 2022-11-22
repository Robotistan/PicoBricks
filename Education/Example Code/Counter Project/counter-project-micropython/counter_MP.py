from machine import Pin, I2C,Timer
from picobricks import SSD1306_I2C
import utime
WIDTH=128
HEIGHT=64
#define the width and height values
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=2000000)
oled= SSD1306_I2C(WIDTH, HEIGHT, i2c)
counter=0
while (counter<10):
    counter=counter+1
    oled.fill(0)
    oled.text(str(counter),64,32)
    utime.sleep(0.5)
    oled.show()
    
   
    