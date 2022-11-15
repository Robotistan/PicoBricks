from machine import Pin,ADC,PWM
from utime import sleep
#define libraries

led=PWM(Pin(7))
pot=ADC(Pin(26,Pin.IN))
#define the value we get from the led and pot.
led.freq(1000)

while True:#while loop
    
    led.duty_u16(int((pot.read_u16())))
    print(str(int((pot.read_u16()))))
    #Turn on the LED according to the value from the potentiometer.
    
    sleep(0.1)#delay
                 
