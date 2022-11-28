from machine import Pin, SPI
from mfrc522 import MFRC522
import utime
#define libraries
sck = Pin(18, Pin.OUT)
mosi = Pin(19, Pin.OUT)
miso = Pin(16, Pin.OUT)
sda = Pin(17, Pin.OUT)
rst = Pin(15, Pin.OUT)
spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
rdr = MFRC522(spi, sda, rst)
#define MFRC522 pins

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            print(uid)
            utime.sleep(1)
            #read the card and give the serial number of the card
