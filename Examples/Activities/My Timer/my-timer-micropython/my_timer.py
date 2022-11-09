from machine import Pin, I2C, ADC, Timer #to acces the hardware picobricks
from picobricks import SSD1306_I2C #oled library
import utime #time library

WIDTH  = 128                                            
HEIGHT = 64
#define the width and height values

sda=machine.Pin(4)
scl=machine.Pin(5)
#we define sda ​​and scl pins for inter-path communication
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)#determine the frequency values

oled = SSD1306_I2C(128, 64, i2c)
pot = ADC(Pin(26))
button = Pin(10,Pin.IN,Pin.PULL_DOWN)
#determine our input and output pins

oled.fill(0)
oled.show()
#Show on OLED

time=Timer()
time2=Timer()
time3=Timer()
#define timers

def minute(timer):
    global setTimer
    setTimer -=1
    
def second(timer):
    global sec
    sec-=1
    if sec==-1:
        sec=59
        
def msecond(timer):
    global msec
    msec-=1
    if msec==-1:
        msec=99
#We determine the increments of the minute-second and millisecond values.
sec=59
msec=99

global setTimer

while button.value()==0:
    setTimer=int((pot.read_u16()*60)/65536)+1
    oled.text("Set timer:" + str(setTimer) + " min",0,12)
    oled.show()
    utime.sleep(0.1)
    oled.fill(0)
    oled.show()
#If the button is not pressed, the value determined by the potentiometer is printed on the OLED screen.
    
setTimer-=1

time.init(mode=Timer.PERIODIC,period=60000, callback=minute)
time2.init(mode=Timer.PERIODIC,period=1000, callback=second)
time3.init(mode=Timer.PERIODIC,period=10, callback=msecond)
#We determine the periods of minutes, seconds and milliseconds.
utime.sleep(0.2)#wait for 0.2 second

while button.value()==0:
    oled.text("min:" + str(setTimer),50,10)
    oled.text("sec:" + str(sec),50,20)
    oled.text("ms:" + str(msec),50,30)
    oled.show()
    utime.sleep(0.008)
    oled.fill(0)
    oled.show()
    if(setTimer==0 and sec==0 and msec==99):
        utime.sleep(0.1)
        msec=0
        break;
#When the button is pressed, it prints the min-sec-ms values ​​to the OLED screen in the determined x and y coordinates.
    
oled.text(str(setTimer),60,10)
oled.text(str(sec),60,20)
oled.text(str(msec),60,30)
oled.text("Time is Over!",10,48)
oled.show()
#Print the minutes, seconds, milliseconds and "Time is Over" values ​​to the X and Y coordinates determi
