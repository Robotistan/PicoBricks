from machine import Pin, I2C, ADC, PWM
from ssd1306 import SSD1306_I2C
import utime
from ws2812 import NeoPixel

WIDTH  = 128                                            
HEIGHT = 64                                          
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
neo = NeoPixel(6, n=1, brightness=0.3, autowrite=False)

oled = SSD1306_I2C(128, 64, i2c)
ldr = ADC(Pin(27))
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
buzzer = PWM(Pin(20, Pin.OUT))
buzzer.freq(1000)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

oled.fill(0)
oled.show()

neo.fill(BLACK)
neo.show()

if ldr.read_u16()<4000:
    wakeup = True
else:
    wakeup = False
    
while True:
    while wakeup==False:
        oled.fill(0)
        oled.show()
        oled.text("Good night",25,32)
        oled.show()
        utime.sleep(1)
        if ldr.read_u16()<4000:
            while button.value()==0:
                oled.fill(0)
                oled.show()
                oled.text("Good morning",15,32)
                oled.show()
                neo.fill(WHITE)
                neo.show()
                buzzer.duty_u16(6000)
                utime.sleep(1)
                buzzer.duty_u16(0)
                utime.sleep(0.5)
                wakeup=True
            neo.fill(BLACK)
            neo.show()
    oled.fill(0)
    oled.show()
    oled.text("Have a nice day!",0,32)
    oled.show()
    if ldr.read_u16()>40000:
        wakeup= False
        
    utime.sleep(1)
