#Ferris Wheel
# You need 3 batteries for this project.

import time
from machine import PWM, Pin, ADC

pot = ADC(26)
motor_1 = PWM(Pin(21))
motor_2 = PWM(Pin(22))
motor_1.freq(50)
motor_2.freq(50)
motor_1.duty_u16(0)
motor_2.duty_u16(0)
while True:
    pot_val = pot.read_u16()
    time.sleep(0.2)
    
    if pot_val > 800:
        print("sa")
        motor_1.duty_u16(pot_val-400)
        motor_2.duty_u16(pot_val-400)
    else:
        motor_1.duty_u16(0)
        motor_2.duty_u16(0)
