from machine import Pin, I2C
from picobricks import MotorDriver, SHTC3
import utime

LIMIT_TEMPERATURE = 20 #define the limit temperature

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)
shtc_sensor = SHTC3(i2c)

motor.dc(1,0,0)

while True:
	temp = shtc_sensor.temperature()
	print(temp)
	if temp >= LIMIT_TEMPERATURE:    #operate if the room temperature is higher than the limit temperature 
		motor.dc(1,255,0)
	else:
		motor.dc(1,0,0)



