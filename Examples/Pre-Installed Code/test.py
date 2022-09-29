from utime import sleep
import time
from machine import Pin, I2C, PWM, ADC
from picobricks import SSD1306_I2C, WS2812
import framebuf
import random
from dht import DHT11

WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height

def button_push(event):
    if button.value() == 1:
        oled.text("BUTTON : 1", 0, 10)
        oled.show()        
        motor_1.high()
        motor_2.high()
        time.sleep(0.5)
        motor_1.low()
        motor_2.low()
        
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)   # Init I2C using pins (default I2C0 pins)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display
buzzer = PWM(Pin(20))
buzzer.duty_u16(0)  
relay = Pin(12, Pin.OUT)
button = Pin(10, Pin.IN)
motor_1 = Pin(21, Pin.OUT)
motor_2 = Pin(22, Pin.OUT)
pot = ADC(26)
light_level = ADC(27)
conversion_factor = 3.3 / (65535) 
dht_sensor = DHT11(Pin(11))
led = Pin(7, Pin.OUT)
ws = WS2812(6, n=1, brightness=0.4)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = (RED, GREEN, BLUE)

for color in COLORS:
        ws.fill(color)
        ws.show()
        time.sleep(0.1)
ws.fill((0,0,0))
ws.show()

buzzer.duty_u16(2000)
buzzer.freq(831)
time.sleep(0.5)
buzzer.duty_u16(0)
time.sleep(0.5)
relay.high()
time.sleep(0.5)
relay.low()
time.sleep(0.5)
led.high()
time.sleep(0.5)
led.low()
time.sleep(0.5)


dht_read_time = time.time()
button.irq(trigger=Pin.IRQ_RISING, handler=button_push)

while True:
    if time.time() - dht_read_time >= 3:
        dht_read_time = time.time()
        try:
            dht_sensor.measure()
        except Exception as e:
            print("Warning: could not measure: " + str(e))

    oled.fill(0)
    oled.text("POT:      {0:.2f}V".format(pot.read_u16() * conversion_factor),0,20) # round(pot.read_u16() * conversion_factor, 2)
    oled.text("LIGHT:    {0:.2f}%".format((65535.0 - light_level.read_u16())/650.0),0,30)
    oled.text("TEMP:     {0:.2f}C".format(dht_sensor.temperature()),0,40)
    oled.text("HUMIDITY: {0:.1f}%".format(dht_sensor.humidity()),0,50)
    oled.show()
    time.sleep(1)
    oled.fill(0)