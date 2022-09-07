from machine import Pin, ADC
from utime import sleep

ldr=ADC(27)

while True:
    print(ldr.read_u16())
    sleep(0.01)


Projenin Kodları:
from machine import Pin, ADC,PWM
from utime import sleep

ldr=ADC(27)
servo=PWM(Pin(21))
servo.freq(50)

while True:
    sleep(0.01)
    if ldr.read_u16()>40000:
        servo.duty_u16(2000)
        sleep(0.1)
        servo.duty_u16(1350)
        sleep(0.5)