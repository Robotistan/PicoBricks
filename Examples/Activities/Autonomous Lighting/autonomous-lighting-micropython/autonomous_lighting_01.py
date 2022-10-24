from machine import Pin,ADC
import time
from picobricks import WS2812

ldr = ADC(Pin(27))
ws = WS2812(6, brightness=0.4)
#define the input and output pins

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

COLORS = (RED,GREEN,BLUE)

while True:
    
    print(ldr.read_u16())
    
    if(ldr.read_u16()>20000):
        for color in COLORS:
           ws.fill(color)
           ws.show()
    else:
        ws.fill((0,0,0))
        ws.show()

