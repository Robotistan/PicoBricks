#Include the library files
import time
from machine import Pin, freq, PWM
from picobricks import NEC_16
from time import sleep

# User callback
def ir_callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        print(data)
        if data == Up: #24
            forward()
        elif data == Left: #8
            left()
        elif data == Right: #90
            right()
        elif data == Stop: #28
            stop()
        elif data == Circle: #69
            stop()
def decodeKeyValue(data):
    return data

def forward():
        m1.high()
        m2.high()
def left():
        m1.low()
        m2.high()  
def right():
        m1.high()
        m2.low()
def stop():  
        m1.low()
        m2.low()
def circle():
        m1.high()
        sleep(5.0)
        m2.low()    
#Define the IR receiver pin and motor pins
ir = NEC_16(Pin(0, Pin.IN), ir_callback)
m1 = Pin(21, Pin.OUT)
m2 = Pin(22, Pin.OUT)

m1.low()
m2.low()

Up = 24
Left = 8
Right = 90
Stop = 28
ir_data = 0
Circle = 69
#ir = NEC_8(pin_ir, callback)  # Instantiate receiver
#ir.error_function(print_error)  # Show debug information

try:
    while True:
        pass
except KeyboardInterrupt:
    ir.close()