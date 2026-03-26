from machine import Pin, I2C, PWM, ADC, UART
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import utime
import time
from picobricks import SSD1306_I2C, WS2812, SHTC3, MotorDriver
from resources import Note_img, Picobricks_img, Tones, Song

WIDTH  = 128   # OLED display width
HEIGHT = 64    # OLED display height
NOTE_DURATION = 0.11  # Duration multiplier for each musical note

# Initialize I2C communication on the specified pins
i2c = I2C(0, scl=Pin(5), sda=Pin(4))

# Initialize OLED display with I2C
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)

# Initialize motor driver and temperature/humidity sensor
motor = MotorDriver(i2c)
shtc_sensor = SHTC3(i2c)

MAX_LEN = 99           # Maximum BLE buffer length
buffer = bytearray()   # Buffer for received BLE data
ble_data = bytearray(5)  # Buffer for data to send over BLE

# Initialize BLE and simple peripheral
ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

def oled_write(buffer, start=3, finish=100):
    # Extract text bytes from the buffer and convert them to characters
    val = buffer[start:finish]
    word = ''.join(chr(b) for b in val if b != 0)

    # Clear the display before writing new content
    oled.fill(0)

    # Write text to the OLED screen in 16-character chunks per line
    for number, i in enumerate(range(0, len(word), 16)):
        lenght = word[i:i+16]
        oled.text(lenght, 0, number * 8)   # x=0, y=0/8/16/24...
    
    oled.show()

def playtone(frequency):
    # Play a tone at the given frequency
    buzzer.duty_u16(5000)
    buzzer.freq(frequency)
   
def bequiet():
    # Stop the buzzer
    buzzer.duty_u16(0)

def on_rx(data):
    global buffer

    # Append received BLE data to the buffer
    for b in data:
        buffer.append(b)

        # Keep buffer size within maximum limit
        if len(buffer) > MAX_LEN:
            buffer = buffer[1:]

#     print("BUFFER:", buffer)

# Register BLE receive callback
sp.on_write(on_rx)

# ==================== PIN INITIALIZATION ====================

# Initialize buzzer on GP20 as PWM output
buzzer = PWM(Pin(20))
buzzer.duty_u16(0)    # Start with buzzer off

# Initialize relay output pin
relay = Pin(12, Pin.OUT)

# Initialize button input pin
button = Pin(10, Pin.IN)

# Initialize potentiometer and light sensor ADC pins
pot = ADC(26)
light_level = ADC(27)

# Initialize onboard LED and RGB LED
led = Pin(7, Pin.OUT)
ws2812 = WS2812(6, brightness=1)

while True:
    # Check if a BLE client is connected
    if sp.is_connected():
        if buffer:
            print(list(buffer))

            # OLED text display command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 1):
                oled_write(buffer)

            # RGB LED control command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 2):
                ws2812.pixels_fill((buffer[3], buffer[4], buffer[5]))
                ws2812.pixels_show()

            # Single LED control command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 3):
                if(buffer[3] == 1):  # Turn LED on
                    led.high()
                elif(buffer[3] == 0):  # Turn LED off
                    led.low()

            # Temperature and humidity read command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 4 and buffer[3] == 99):
                tempSHTC = int(shtc_sensor.temperature())
                humiditySHTC = int(shtc_sensor.humidity())
                
                ble_data = bytearray([72, 5, 4, tempSHTC, humiditySHTC])
                sp.send(bytes(ble_data))

            # Relay control command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 5):
                if(buffer[3] == 1):  # Turn relay on
                    relay.high()
                elif(buffer[3] == 0):  # Turn relay off
                    relay.low()

            # Motor driver command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 6):
                if(buffer[3] == 1 or buffer[3] == 2 or buffer[3] == 3 or buffer[3] == 4):
                    # Servo motor control
                    motor.servo(buffer[3], buffer[4])
                else:
                    # DC motor control
                    motor.dc(buffer[3] - 4, buffer[4], buffer[5])

            # Button/music command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 7):
                if(buffer[3] == 1):  # Pressed
                    for note in Song:
                        if note[0] == "-":
                            bequiet()
                        else:
                            playtone(Tones[note[0]])
                        time.sleep(NOTE_DURATION * note[1])
                elif(buffer[3] == 0):  # Released
                    bequiet()

            # Buzzer control command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 8):
                if(buffer[3] == 1):  # Active
                    buzzer.duty_u16(2000)
                    buzzer.freq(831)
                elif(buffer[3] == 0):  # Passive
                    buzzer.duty_u16(0)

            # LDR (light sensor) read command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 9 and buffer[3] == 99):
                ldr_val = max(0, min(255, int((65535 - light_level.read_u16()) / 650)))
                ble_data = bytearray([72, 5, 9, ldr_val])
                sp.send(bytes(ble_data))

            # Potentiometer read command
            if (buffer[0] == 72 and buffer[1] == 5 and buffer[2] == 10 and buffer[3] == 99):
                pot_val = max(0, min(255, int(pot.read_u16() * 255 / 65535)))
                ble_data = bytearray([72, 5, 10, pot_val])
                sp.send(bytes(ble_data))

            # Clear buffer after processing
            buffer[:] = b''

        # Small delay to reduce CPU usage
        time.sleep(0.5)
