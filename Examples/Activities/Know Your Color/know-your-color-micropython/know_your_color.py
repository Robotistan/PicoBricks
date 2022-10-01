from machine import Pin, PWM, ADC
from utime import sleep
from picobricks import WS2812

ws = WS2812(6, brightness=0.3)
ldr=ADC(27)
buzzer=PWM(Pin(20, Pin.OUT))
servo1=PWM(Pin(21))
servo2=PWM(Pin(22))

servo1.freq(50)
servo2.freq(50)
buzzer.freq(440)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
angleupdown=4770


def up():
    global angleupdown
    for i in range (45):
        angleupdown +=76 
        servo2.duty_u16(angleupdown)
        sleep(0.03)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)

def down():
    global angleupdown
    for i in range (45):
        angleupdown -=76
        servo2.duty_u16(angleupdown)
        sleep(0.03)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)

def open():
    servo1.duty_u16(8200) #180 degree
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    
def close():
    servo1.duty_u16(2490) #30 degree
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    
open()
servo2.duty_u16(angleupdown)
ws.pixels_fill(BLACK)
ws.pixels_show()
while True:
    if ldr.read_u16()>40000:
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
