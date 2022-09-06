from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from utime import sleep

WIDTH  = 128                                            
HEIGHT = 64

sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(128, 64, i2c)

wire=Pin(1,Pin.OUT)
led = Pin(7,Pin.OUT)
buzzer=Pin(20, Pin.OUT)
button=Pin(10,Pin.IN,Pin.PULL_DOWN)
endtime=0
while True:
    led.low()
    oled.fill(0)
    oled.show()
    oled.text("<BUZZ WIRE GAME>",0,0)
    oled.text("Press the button",0,17)
    oled.text("TO START!",25,35)
    oled.show()
    while button.value()==0:
        print("press the button")
    oled.fill(0)
    oled.show()
    oled.text("GAME",25,35)
    oled.text("STARTED",25,45)
    oled.show()
    wire.high()
    timer_start=utime.ticks_ms()
    while wire.value()==1:
        print("Started")
    endtime=utime.ticks_diff(utime.ticks_ms(), timer_start)
    print(endtime)
    oled.fill(0)
    oled.show()
    oled.text("GAME OVER!",25,35)
    oled.text(endtime + "ms" ,25,45)
    oled.show()
    led.high()
    buzzer.high()
    sleep(5)