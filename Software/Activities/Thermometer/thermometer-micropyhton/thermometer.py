from machine import Pin,I2C,ADC #to acces the hardware picobricks
from picobricks import SSD1306_I2C, DHT11 #oled library
import utime #time library
#to acces the hardware picobricks
WIDTH=128
HEIGHT=64
#define the weight and height picobricks

sda=machine.Pin(4)
scl=machine.Pin(5)
#we define sda and scl pins for inter-path communication
i2c=machine.I2C(0, sda=sda, scl=scl, freq=2000000)#determine the frequency values
oled=SSD1306_I2C(WIDTH, HEIGHT, i2c)
pico_temp=DHT11(Pin(11))
current_time=utime.time()
while True:
    if(utime.time() - current_time > 2):
        current_time = utime.time()
        pico_temp.measure()
        oled.fill(0)#clear OLED
        oled.show()
        temperature=pico_temp.temperature
        humidity=pico_temp.humidity
        oled.text("Temperature: ",15,10)#print "Temperature: " on the OLED at x=15 y=10
        oled.text(str(int(temperature)),55,25)
        oled.text("Humidty: ", 30,40)
        oled.text(str(int(humidity)),55,55)
        oled.show()#show on OLED
        utime.sleep(0.5)#wait for a half second
