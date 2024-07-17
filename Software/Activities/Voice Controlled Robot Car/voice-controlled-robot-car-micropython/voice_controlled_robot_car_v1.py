from machine import Pin, UART
from utime import sleep

uart = UART(0,9600) #If connection cannot be established, try 115200.
m1 = Pin(21, Pin.OUT)
m2 = Pin(22, Pin.OUT)
cmd = uart.readline()

m1.low()
m2.low()
cmd = ""
while True:
    sleep(0.05)
    if uart.any():
        cmd = uart.readline()
        print(cmd)
    if cmd.startswith(b'f') or cmd.startswith(b'F'):
        m1.high()
        m2.high()
    elif cmd.startswith(b'r') or cmd.startswith(b'R'):
        m1.high()
        m2.low()
    elif cmd.startswith(b'l') or cmd.startswith(b'L'):
        m1.low()
        m2.high()
    elif cmd.startswith(b's') or cmd.startswith(b'S'):
        m1.low()
        m2.low()
    cmd=""
