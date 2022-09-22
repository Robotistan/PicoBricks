from machine import Pin, ADC, PWM#to access the hardware on the pico
from utime import sleep #time library

ldr=ADC(27) #initialize digital pin 27 for LDR
servo=PWM(Pin(21)) #initialize digital PWM pin 27 for Servo Motor
servo.freq(50)

while True:
    sleep(0.01)
    #When LDR data higher than 40000
    if ldr.read_u16()>4000:
        servo.duty_u16(2000)# sets position to 180 degrees
        sleep(0.1)#delay
        servo.duty_u16(1350) # sets position to 0 degrees
        sleep(0.5)#delay