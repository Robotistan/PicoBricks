from machine import Pin, I2C, PWM, ADC, UART
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import utime
import time
from picobricks import SSD1306_I2C, WS2812, SHTC3, MotorDriver
from resources import Note_img, Picobricks_img, Tones, Song

WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height
NOTE_DURATION = 0.11

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display
motor = MotorDriver(i2c)
shtc_sensor = SHTC3(i2c)

MAX_LEN = 99
buffer = bytearray()
ble_data = bytearray(5)

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

def oled_write(buffer, start=3, finish=100):
    val = buffer[start:finish]
    word = ''.join(chr(b) for b in val if b != 0)
    oled.fill(0)
    for number, i in enumerate(range(0, len(word), 16)):
        lenght = word[i:i+16]
        oled.text(lenght, 0, number * 8)   # x=0, y=0/8/16/24...
    
    oled.show()

def playtone(frequency):
    buzzer.duty_u16(5000)
    buzzer.freq(frequency)
   
def bequiet():
    buzzer.duty_u16(0)

def on_rx(data):
    global buffer

    for b in data:
        buffer.append(b)
        if len(buffer) > MAX_LEN:
            buffer = buffer[1:]

#     print("BUFFER:", buffer)

sp.on_write(on_rx)

# Pin Initialization
buzzer = PWM(Pin(20)) # setting GP20 as PWM pin
buzzer.duty_u16(0)    # setting duty cycle to 0
relay = Pin(12, Pin.OUT)
button = Pin(10, Pin.IN) # setting GP10 PIN as input
pot = ADC(26)
light_level = ADC(27)
led = Pin(7, Pin.OUT)
ws2812 = WS2812(6,brightness=1)

while True:
    if sp.is_connected():
        if buffer:
            print(list(buffer))
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 1): #Oled
                oled_write(buffer)
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 2): #RGB
                ws2812.pixels_fill((buffer[3],buffer[4],buffer[5]))
                ws2812.pixels_show()
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 3): #Led
                if(buffer[3] == 1): #Open
                    led.high()
                elif(buffer[3] == 0): #Close
                    led.low()
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 4 and buffer[3] == 99): #Temp & Hum
                tempSHTC = int(shtc_sensor.temperature())
                humiditySHTC = int(shtc_sensor.humidity())
                
                ble_data = bytearray([72, 5, 4, tempSHTC, humiditySHTC])
                sp.send(bytes(ble_data))
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 5): #Relay
                if(buffer[3] == 1): #Open
                    relay.high()
                elif(buffer[3] == 0): #Close
                    relay.low()
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 6): #Motor Driver
                if(buffer[3] == 1 or buffer[3] == 2 or buffer[3] == 3 or buffer[3] == 4): #Servo
                    motor.servo(buffer[3],buffer[4])
                else:
                    motor.dc(buffer[3] - 4,buffer[4],buffer[5])
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 7): #Button
                if(buffer[3] == 1): #Pressed
                    for note in Song:
                        if note[0] == "-":
                            bequiet()
                        else:
                            playtone(Tones[note[0]])
                        time.sleep(NOTE_DURATION*note[1])
                elif(buffer[3] == 0): #Realase
                    bequiet()
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 8): #Buzzer
                if(buffer[3] == 1): #Active
                    buzzer.duty_u16(2000)
                    buzzer.freq(831)
                elif(buffer[3] == 0): #Passive
                    buzzer.duty_u16(0)
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 9 and buffer[3] == 99): #LDR
                ldr_val = max(0, min(255, int((65535 - light_level.read_u16()) / 650)))
                ble_data = bytearray([72, 5, 9, ldr_val])
                sp.send(bytes(ble_data))
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 10 and buffer[3] == 99): #Pot
                pot_val = max(0, min(255, int(pot.read_u16() * 255 / 65535)))
                ble_data = bytearray([72, 5, 10, pot_val])
                sp.send(bytes(ble_data))
            buffer[:] = b''
        time.sleep(0.5)
