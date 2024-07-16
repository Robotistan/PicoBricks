from machine import Pin, PWM, I2C
from picobricks import MFRC522, WS2812, MotorDriver
from time import sleep

reader = MFRC522(spi_id=0,sck=18,miso=16,mosi=19,cs=17,rst=0)

buzzer = PWM(Pin(20, Pin.OUT))
buzzer.freq(1000)

ws2812 = WS2812(6,brightness=1)

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
motor = MotorDriver(i2c)

def activated():
        print("Card ID: "+ str(card)+" PASS: Activated")
        ws2812.pixels_fill((0, 255, 0))
        ws2812.pixels_show()
        
        buzzer.freq(2000)
        
        buzzer.duty_u16(2000)
        sleep(0.05)
        buzzer.duty_u16(0)
        sleep(0.05)
        
        buzzer.duty_u16(2000)
        sleep(0.05)
        buzzer.duty_u16(0)
        sleep(0.05)
        
        motor.servo(1,0)

        sleep(3)
        motor.servo(1,180)
        ws2812.pixels_fill((255, 0, 0))
        ws2812.pixels_show()
        
def unknown_card():
    print("Card ID: "+ str(card)+" UNKNOWN CARD! ")
    buzzer.freq(1000)
    buzzer.duty_u16(2000)
    sleep(0.1)
    buzzer.duty_u16(0)
    sleep(0.1)
    
id_list=[562956160,2309304334,2903577093] # add your card number in list
    
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    ws2812.pixels_fill((255, 0, 0))
    ws2812.pixels_show()  
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
                            
            if card in id_list:
                activated()                    
            else:
                unknown_card()
