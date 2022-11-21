from machine import I2C, Pin, SPI, PWM
from mfrc522 import MFRC522
from ws2812 import NeoPixel
from utime import sleep 

servo = PWM(Pin(21))
servo.freq(50)
servo.duty_u16(1350) #servo set 0 angle 8200 for 180.

buzzer = PWM(Pin(20, Pin.OUT))
buzzer.freq(440)

neo = NeoPixel(6, n=1, brightness=0.3, autowrite=False)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

sck = Pin(18, Pin.OUT)
mosi = Pin(19, Pin.OUT)
miso = Pin(16, Pin.OUT)
sda = Pin(17, Pin.OUT)
rst = Pin(15, Pin.OUT)
spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
homeowner = "0x734762a3"
rdr = MFRC522(spi, sda, rst)

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
                neo.fill(GREEN)
                neo.show()
                servo.duty_u16(6000)
                sleep(3)
                servo.duty_u16(1350)
                neo.fill(BLACK)
                neo.show()
               
            else:
                neo.fill(RED)
                neo.show()
                sleep(3)
                neo.fill(BLACK)
                neo.show()
                servo.duty_u16(1350)
