from machine import Pin, PWM, I2C

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

motor.servo(1,180)
motor.servo(2,90)
