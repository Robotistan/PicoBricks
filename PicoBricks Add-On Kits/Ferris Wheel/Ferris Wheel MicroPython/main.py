#Ferris Wheel
# You need 3 batteries for this project.

import time
from machine import PWM, Pin, ADC

pot = ADC(26)
motor_1 = PWM(Pin(21))
motor_1.duty_u16(0)

while True:
    pot_val = pot.read_u16()
    print(pot_val)
    time.sleep(0.5)
    
    if pot_val > 150:
        motor_1.duty_u16(pot_val)
    else:
        motor_1.duty_u16(0)
   
