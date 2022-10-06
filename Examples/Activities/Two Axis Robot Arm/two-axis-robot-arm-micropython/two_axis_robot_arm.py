from machine import Pin, PWM, ADC
from utime import sleep
from picobricks import WS2812
#define libraries

ws = WS2812(6, brightness=0.3)
ldr=ADC(27)
buzzer=PWM(Pin(20, Pin.OUT))
servo1=PWM(Pin(21))
servo2=PWM(Pin(22))
# define LDR, buzzer and servo motors pins

servo1.freq(50)
servo2.freq(50)
buzzer.freq(440)
# define frequencies of servo motors and buzzer

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0) # RGB color settings
angleupdown=4770
angleupdown2=8200

def up():
    global angleupdown
    for i in range (45):
        angleupdown +=76 
        servo2.duty_u16(angleupdown)
        sleep(0.03)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    # servo2 goes up at specified intervals
def down():
    global angleupdown
    for i in range (45):
        angleupdown -=76
        servo2.duty_u16(angleupdown)
        sleep(0.03)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    # servo2 goes down at specified intervals

def open():
    global angleupdown2
    for i in range (45):
        angleupdown2 +=500
        servo1.duty_u16(angleupdown2)
        sleep(0.03)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    # servo1 works for opening the clamps
def close():
    global angleupdown2
    for i in range (45):
        angleupdown2 -=500
        servo1.duty_u16(angleupdown2)
        sleep(0.03)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    # servo1 works for closing the clamps
open()
servo2.duty_u16(angleupdown)
ws.pixels_fill(BLACK)
ws.pixels_show()
while True:
    if ldr.read_u16()>20000:
        ws.pixels_fill(RED)
        ws.pixels_show()
        sleep(1)
        buzzer.duty_u16(2000)
        sleep(1)
        buzzer.duty_u16(0)
        open()
        sleep(0.5)
        down()
        sleep(0.5)
        close()
        sleep(0.5)
        up()
        ws.pixels_fill(GREEN)
        ws.pixels_show()
        sleep(0.5)
        # According to the data received from LDR, RGB LED lights red and green and servo motors move
