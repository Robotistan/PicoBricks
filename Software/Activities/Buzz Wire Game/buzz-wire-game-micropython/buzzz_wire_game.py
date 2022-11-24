from machine import Pin, I2C, Timer #to access the hardware on the pico
from picobricks import SSD1306_I2C #OLED Screen Library
from utime import sleep # time library

#OLED Screen Settings
WIDTH  = 128                                            
HEIGHT = 64

sda=machine.Pin(4)#initialize digital pin 4 and 5 as an OUTPUT for OLED Communication
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

wire=Pin(1,Pin.OUT)#initialize digital pin 1 as an OUTPUT 
led = Pin(7,Pin.OUT)#initialize digital pin 7 and 5 as an OUTPUT for LED
buzzer=Pin(20, Pin.OUT)#initialize digital pin 20 as an OUTPUT for Buzzer
button=Pin(10,Pin.IN,Pin.PULL_DOWN)#initialize digital pin 10 as an INPUT for button
endtime=0


while True:
    led.low()
    oled.fill(0)
    oled.show()
    oled.text("<BUZZ WIRE GAME>",0,0)
    oled.text("Press the button",0,17)
    oled.text("TO START!",25,35)
    oled.show()
    #When button is '0', OLED says 'GAME STARTED'
    while button.value()==0:
        print("press the button")
    oled.fill(0)
    oled.show()
    oled.text("GAME",25,35)
    oled.text("STARTED",25,45)
    oled.show()
    wire.high()
    timer_start=utime.ticks_ms()
     #When wire is '1', OLED says 'GAME OVER'
    while wire.value()==1:
        print("Started")
    endtime=utime.ticks_diff(utime.ticks_ms(), timer_start)
    print(endtime)
    oled.fill(0)
    oled.show()
    oled.text("GAME OVER!",25,35)
    oled.text(endtime + "ms" ,25,45)
    oled.show()
    led.high()#LED On
    buzzer.high()#Buzzer On
    sleep(5)#Delay
