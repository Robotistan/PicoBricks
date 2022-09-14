from machine import Pin, UART
from utime import sleep

uart = UART(0,9600) #If connection cannot be established, try 115200.
m1 = Pin(21, Pin.OUT)
m2 = Pin(22, Pin.OUT)

m1.low()
m2.low()

while True:
    sleep(0.05)
    if uart.any():
        cmd = uart.readline()
    if cmd==b'F':
        m1.high()
        m2.high()
    elif cmd==b'R':
        m1.high()
        m2.low()
    elif cmd==b'L':
        m1.low()
        m2.high()
    elif cmd==b'S':
        m1.low()
        m2.low()
    cmd=""