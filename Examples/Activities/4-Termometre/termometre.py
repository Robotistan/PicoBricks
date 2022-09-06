from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import utime

WIDTH  = 128                                            
HEIGHT = 64

sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=2000000)
oled = SSD1306_I2C(128, 64, i2c)

pico_temp = ADC(4)
conversion_factor=3.3 / (65536)

while True:
    oled.fill(0)
    oled.show()
    reading =pico_temp.read_u16()*conversion_factor
    temperature= 27 - (reading - 0.706)/0.001721
    oled.text("Temperature:",15,10)
    oled.text(str(int(temperature)),55,30)
    oled.show()
    utime.sleep(0.5)
