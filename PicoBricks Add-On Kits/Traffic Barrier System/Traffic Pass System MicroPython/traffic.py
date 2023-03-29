'''
Traffic System
'''
from machine import Pin, PWM, ADC
import utime
from picobricks import WS2812

servo =PWM(Pin(21,Pin.OUT))
buzzer  =PWM(Pin(20,Pin.OUT))
buzzer.freq(1000)
ldr= ADC(Pin(27))
ws = WS2812(6, brightness=0.1)
servo.freq(50)
pos = 5500
ldr_stt = ldr.read_u16()
#define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

def play_buzzer():
    buzzer.freq(700)
    buzzer.duty_u16(2000)
    utime.sleep(0.1)
    buzzer.duty_u16(0)
    
while True:
    ldr_stt = ldr.read_u16()    
    ws.pixels_fill(RED)  #turn off the RGB
    ws.pixels_show()
    print("LDR:" ,ldr_stt)
    print("POS:" , pos)
    if(ldr_stt>17000):
        ws.pixels_fill(YELLOW)
        ws.pixels_show()
        while pos > 1920:
            pos -=5
            servo.freq(50)
            servo.duty_u16(pos) #70 degree
            utime.sleep(0.001)
        play_buzzer()
        servo.freq(50)
        ws.pixels_fill(GREEN)
        ws.pixels_show()
        utime.sleep(2)
    else:
        while pos < 5500:
            pos +=5
            servo.freq(50)
            servo.duty_u16(pos) #70 degree
            utime.sleep(0.001)
        utime.sleep(2)
