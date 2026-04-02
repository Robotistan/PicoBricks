from machine import Pin, PWM, ADC, I2C
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import utime
import time
from picobricks import MotorDriver

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

pot = ADC(26)

MAX_LEN = 10
buffer = bytearray()

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
def on_rx(data):
    global buffer

    for b in data:
        buffer.append(b)
        if len(buffer) > MAX_LEN:
            buffer = buffer[1:]

#     print("BUFFER:", buffer)

sp.on_write(on_rx)

while True:
    if sp.is_connected():
        if buffer:
            if (buffer[0] == 72 and buffer[1] == 4):
                pot_val = buffer[2]
                speed = int (convert(pot_val, 200, 65535, 0, 255))
                
                if speed > 30:
                    motor.dc(1,speed,0)
                    motor.dc(2,speed,0)
                else:
                    motor.dc(1,0,0)
                    motor.dc(2,0,0)
            buffer[:] = b''
        time.sleep(0.5)
    else:
        pot_val = pot.read_u16()
        time.sleep(0.2)
        speed = int (convert(pot_val, 200, 65535, 0, 255))
        
        if speed > 30:
            motor.dc(1,speed,0)
            motor.dc(2,speed,0)
        else:
            motor.dc(1,0,0)
            motor.dc(2,0,0)


