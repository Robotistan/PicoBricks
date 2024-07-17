from machine import Pin, UART, I2C
from utime import sleep
from picobricks import MotorDriver

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

uart = UART(0,9600) 
cmd = uart.readline()

motor.dc(1,0,0)
motor.dc(2,0,0)
cmd = ""

while True:
    sleep(0.05)
    if uart.any():
        cmd = uart.readline()
        print(cmd)
    if cmd.startswith(b'f') or cmd.startswith(b'F'):
		motor.dc(1,255,0)
		motor.dc(2,255,0)
    elif cmd.startswith(b'r') or cmd.startswith(b'R'):
        motor.dc(1,255,0)
        motor.dc(2,0,0)
    elif cmd.startswith(b'l') or cmd.startswith(b'L'):
        motor.dc(1,0,0)
        motor.dc(2,255,0)
    elif cmd.startswith(b's') or cmd.startswith(b'S'):
		motor.dc(1,0,0)
		motor.dc(2,0,0)
    cmd=""
