from machine import Pin, I2C, ADC #to acces the hardware picobricks
from ssd1306 import SSD1306_I2C #oled library
import utime #time library
#to acces the hardware picobricks
WIDTH  = 128                                            
HEIGHT = 64
#define the width and height values
sda=machine.Pin(4)
scl=machine.Pin(5)
#we define sda ​​and scl pins for inter-path communication
i2c=machine.I2C(0,sda=sda, scl=scl, freq=2000000) #determine the frequency values
oled = SSD1306_I2C(128, 64, i2c)

pico_temp = ADC(4)
conversion_factor=3.3 / (65536) #enter the conversion factor value

while True:
    oled.fill(0)
    oled.show()
    #Show on OLED
    reading =pico_temp.read_u16()*conversion_factor
    temperature= 27 - (reading - 0.706)/0.001721
    #calculate the temperature value
    oled.text("Temperature:",15,10)#print "temperature" on the OLED at x=15 y=10
    oled.text(str(int(temperature)),55,30)
    oled.show()#Show on OLED
    utime.sleep(0.5)#wait for a half second
