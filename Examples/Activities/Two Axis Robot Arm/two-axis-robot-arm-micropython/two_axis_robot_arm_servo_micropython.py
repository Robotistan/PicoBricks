from machine import Pin, PWM
servo1=PWM(Pin(21))
servo2=PWM(Pin(22))

servo1.freq(50)
servo2.freq(50)

servo1.duty_u16(8200) # 180 degree
servo2.duty_u16(4770) # 90 degree 
