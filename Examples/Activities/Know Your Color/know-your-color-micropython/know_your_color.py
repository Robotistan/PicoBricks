from machine import Pin, I2C
from picobricks import SSD1306_I2C
import utime
import urandom
import _thread
from picobricks import WS2812

WIDTH  = 128                                            
HEIGHT = 64                                          
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
ws = WS2812(6, brightness=0.1)

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

button = Pin(10,Pin.IN,Pin.PULL_DOWN)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

oled.fill(0)
oled.show()

ws.fill(BLACK)
ws.show()

global button_pressed
score=0
button_pressed = False

def random_rgb():
    global ledcolor
    ledcolor=int(urandom.uniform(1,4))
    if ledcolor == 1:
        ws.fill(RED)
        ws.show()
    elif ledcolor == 2:
        ws.fill(GREEN)
        ws.show()
    elif ledcolor == 3:
        ws.fill(BLUE)
        ws.show()
    elif ledcolor == 4:
        ws.fill(WHİTE)
        ws.show()

def random_text():
    global oledtext
    oledtext=int(urandom.uniform(1,4))
    if oledtext == 1:
        oled.fill(0)
        oled.show()
        oled.text("RED",45,32)
        oled.show()
    elif oledtext == 2:
        oled.fill(0)
        oled.show()
        oled.text("GREEN",45,32)
        oled.show()
    elif oledtext == 3:
        oled.fill(0)
        oled.show()
        oled.text("BLUE",45,32)
        oled.show()
    elif oledtext == 4:
        oled.fill(0)
        oled.show()
        oled.text("WHITE",45,32)
        oled.show()

def button_reader_thread():
    while True:
        global button_pressed
        if button_pressed == False:
            if button.value() == 1:
                button_pressed = True
                global score
                global oledtext
                global ledcolor
                if ledcolor == oledtext:
                    score += 10
                else:
                    score -= 10
        utime.sleep(0.01)

_thread.start_new_thread(button_reader_thread, ())

oled.text("The Game Begins",0,10)
oled.show()
utime.sleep(2)

for i in range(10):
    random_text()
    random_rgb()
    button_pressed=False
    utime.sleep(1.5)
    oled.fill(0)
    oled.show()
    ws.fill(BLACK)
    ws.show()
utime.sleep(1.5)
oled.fill(0)
oled.text("Your total score:",0,20)
oled.text(str(score), 30,40)
oled.show()
