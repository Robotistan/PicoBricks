import time
from machine import Pin, ADC
from picobricks import  NeoPixel
ldr = ADC(Pin(27))#initialize pin as an input for LDR
neo = NeoPixel(6, n=1, brightness=0.4, autowrite=False)
#define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = (RED, GREEN, BLUE)
while True:#while loop
    print(ldr.read_u16())#run the ldr sensor
    
    if(ldr.read_u16()>10000):#let's check the ldr sensor
        for color in COLORS:
            
            neo.fill(color)
            neo.show()
                
    else:
        neo.fill((0,0,0))#turn off the RGB
        neo.show()