from machine import Pin,ADC,PWM
from utime import sleep

led=PWM(Pin(7))
pot=ADC(Pin(26,Pin.IN))
led.freq(1000)
while True:
    
    led.duty_u16(int((pot.read_u16()))
    print((int((pot.read_u16()))))
    sleep(0.1)
                 
