from machine import Pin, ADC, PWM, I2C#to access the hardware on the pico
from utime import sleep #time library
from picobricks import MotorDriver

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

ldr=ADC(27) #initialize digital pin 27 for LDR
motor.servo(1,0) # sets position to 0 degrees

while True:
    sleep(0.01)
    #When LDR data higher than 40000
    if ldr.read_u16()>4000:
        motor.servo(1,180)# sets position to 180 degrees
        sleep(0.1)#delay
        motor.servo(1,0) # sets position to 0 degrees
        sleep(0.5)#delay
