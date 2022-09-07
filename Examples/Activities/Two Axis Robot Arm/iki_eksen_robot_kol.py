from machine import Pin, PWM, ADC
from utime import sleep
from ws2812 import NeoPixel

neo = NeoPixel(6, n=1, brightness=0.3, autowrite=False)
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

def oppen():
    servo1.duty_u16(8200) #180 degree
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    
def close():
    servo1.duty_u16(2490) #30 degree
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    
oppen()
servo2.duty_u16(angleupdown)
neo.fill(BLACK)
neo.show()
while True:
    if ldr.read_u16()>40000:
        neo.fill(RED)
        neo.show()
        sleep(1)
        buzzer.duty_u16(2000)
        sleep(1)
        buzzer.duty_u16(0)
        oppen()
        sleep(0.5)
        down()
        sleep(0.5)
        close()
        sleep(0.5)
        up()
        neo.fill(GREEN)
        neo.show()
        sleep(0.5)
