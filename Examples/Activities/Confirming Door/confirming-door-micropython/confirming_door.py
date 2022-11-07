from machine import I2C, Pin, SPI, PWM
from mfrc522 import MFRC522
from picobricks import WS2812
from utime import sleep 
#define libraries
servo = PWM(Pin(22))
servo.freq(50)
servo.duty_u16(1350) 

buzzer = PWM(Pin(20, Pin.OUT))
buzzer.freq(440)
#define servo motor and buzzer pins
ws = WS2812(6, brightness=0.3)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
#RGB LED color settings
sck = Pin(18, Pin.OUT)
mosi = Pin(19, Pin.OUT)
miso = Pin(16, Pin.OUT)
sda = Pin(17, Pin.OUT)
rst = Pin(20, Pin.OUT)
spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
homeowner = "0x6a57daa3"
rdr = MFRC522(spi, sda, rst)
#define MFRC522 sensor pins and card serial number

while True:
    
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            buzzer.duty_u16(3000)
            sleep(0.05)
            buzzer.duty_u16(0)
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            print(uid)
            sleep(1)
            if (uid==homeowner):
                ws.pixels_fill(GREEN)
                ws.pixels_show()
                servo.duty_u16(6000)
                sleep(3)
                servo.duty_u16(1350)
                ws.pixels_fill(BLACK)
                ws.pixels_show() #The RGB LED turns green and the door opens thanks to the servo motor, if the correct card is read to the sensor.

               
            else:
                ws.pixels_fill(RED)
                ws.pixels_show()
                sleep(3)
                ws.pixels_fill(BLACK)
                ws.pixels_show()
                servo.duty_u16(1350)
                #The RGB LED turns red and the door does not open, if the wrong card is read to the sensor.
