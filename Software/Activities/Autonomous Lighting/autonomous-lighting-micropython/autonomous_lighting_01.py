import time
from machine import Pin, ADC
from picobricks import  WS2812
#define the library

ldr = ADC(Pin(27))
ws = WS2812(6, brightness=0.4)
#define the input and output pins

#define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = (RED, GREEN, BLUE)
#RGB color Code

while True:#while loop
    print(ldr.read_u16()) #print the value of the LDR sensor to the screen.
    
    if(ldr.read_u16()>10000):#let's check the ldr sensor
        for color in COLORS:
            
            #turn on the LDR
            ws.pixels_fill(color)
            ws.pixels_show()
                
    else:
        ws.pixels_fill((0,0,0))  #turn off the RGB
        ws.pixels_show()
