from machine import Pin, I2C #to acces the hardware picobricks
from picobricks import SSD1306_I2C, SHTC3 #oled library
import utime #time library
#to acces the hardware picobricks
WIDTH=128
HEIGHT=64
#define the weight and height picobricks

i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
shtc_sensor = SHTC3(i2c)

while True:
	oled.fill(0)#clear OLED
	oled.show()
	temperature = shtc_sensor.temperature()
	humidity = shtc_sensor.humidity()
	oled.text("Temperature: ",15,10)#print "Temperature: " on the OLED at x=15 y=10
	oled.text(str(int(temperature)),55,25)
	oled.text("Humidty: ", 30,40)
	oled.text(str(int(humidity)),55,55)
	oled.show()#show on OLED
	utime.sleep(0.5)#wait for a half second
