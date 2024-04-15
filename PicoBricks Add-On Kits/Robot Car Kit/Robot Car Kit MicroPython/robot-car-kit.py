from time import sleep
from machine import Pin,PWM,ADC
import utime
import time
from picobricks import NEC_16,IR_RX

#HC-SR04 
trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)

def getDistance():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
      signaloff = utime.ticks_us()
   while echo.value() == 1:
      signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("The distance from object is ",distance,"cm")
   return distance

def ir_callback(data, addr, ctrl):
    global ir_data
    global ir_addr, data_rcvd
    if data > 0:
        ir_data = data
        ir_addr = addr
        print('Data {:02x} Addr {:04x}'.format(data, addr))
        data_rcvd = True
ir = NEC_16(Pin(0, Pin.IN), ir_callback)
ir_data = 0
data_rcvd = False

motor_1 = PWM(Pin(21))
motor_1.freq(50)
motor_1.duty_u16(0)
motor_2 = PWM(Pin(22))
motor_2.freq(50)
motor_2.duty_u16(0)

def forward():
    motor_1.duty_u16(100 * 650)
    motor_2.duty_u16(100 * 650)

def stop():
    motor_1.duty_u16(0 * 650)
    motor_2.duty_u16(0 * 650)

def backward():
    left()
    time.sleep((2.5))
    stop()

def right():
    motor_1.duty_u16(100 * 650)
    motor_2.duty_u16(0 * 650)

def left():
    motor_1.duty_u16(0 * 650)
    motor_2.duty_u16(100 * 650)
    
while True:
    print(getDistance())
    if data_rcvd == True:
        data_rcvd = False
        if ir_data == IR_RX.number_up:
            forward()
        elif ir_data == IR_RX.number_down:
            backward()
        elif ir_data == IR_RX.number_left:
            left()
        elif ir_data == IR_RX.number_right:
            right()
        elif ir_data == IR_RX.number_ok:
            stop()
    if (getDistance()) < (10):
        stop()
        time.sleep((1))
        backward()
