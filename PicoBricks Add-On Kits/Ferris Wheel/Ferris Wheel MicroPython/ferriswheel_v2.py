#Ferris Wheel
# You need 3 batteries for this project.

import time
from machine import PWM, Pin, ADC, I2C
from picobricks import MotorDriver

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

pot = ADC(26)

while True:
    pot_val = pot.read_u16()
    time.sleep(0.2)
    speed = int (convert(pot_val, 200, 65535, 0, 255))
    
    if speed > 30:
        motor.dc(1,speed,0)
        motor.dc(2,speed,0)
    else:
        motor.dc(1,0,0)
        motor.dc(2,0,0)
