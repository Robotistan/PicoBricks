import time
from machine import Pin, I2C, PWM, ADC
from picobricks import SSD1306_I2C, WS2812
from resources import Note_img, Picobricks_img, Tones, Song
import framebuf
import random
from dht import DHT11

WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height
NOTE_DURATION = 0.11

# Function declaration
def playtone(frequency):
    buzzer.duty_u16(2000)
    buzzer.freq(frequency)
   
def bequiet():
    buzzer.duty_u16(0)
   
def buttonInterruptHandler(event):    # Interrupt event, that will work when button is pressed
    if button.value() == 1:
        oled.fill(0)
        oled.blit(fb2, 0, 0)
        oled.show()
        for note in Song:
            if button.value() == 0:  # if button is released then reset ws2812, oled, buzzer and return
                ws2812.fill((0,0,0))
                ws2812.show()
                bequiet()
                oled.fill(0)
                oled.show()
                break
            if note[0] == "-":
                bequiet()
            else:
                playtone(Tones[note[0]])
                ws2812.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                ws2812.show()
            time.sleep(NOTE_DURATION*note[1])

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)   # Init I2C using pins
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display
fb1 = framebuf.FrameBuffer(Picobricks_img, 128,64 , framebuf.MONO_HLSB) # Creating framebuffer for PicoBricks Logo
fb2 = framebuf.FrameBuffer(Note_img, 128,64, framebuf.MONO_HLSB)        # Creating framebuffer for music note

# Pin Initialization
buzzer = PWM(Pin(20)) # setting GP20 as PWM pin
buzzer.duty_u16(0)    # setting duty cycle to 0
relay = Pin(12, Pin.OUT)
button = Pin(10, Pin.IN) # setting GP10 PIN as input
pot = ADC(26)
light_level = ADC(27)
conversion_factor = 3.3 / (65535)
dht_sensor = DHT11(Pin(11))
led = Pin(7, Pin.OUT)
ws2812 = WS2812(6,brightness=0.4)

button.irq(trigger=Pin.IRQ_RISING, handler=buttonInterruptHandler)  # Button 1 pressed interrupt is set. buttonInterruptHandler function will run when button is pressed

oled.fill(0)
oled.blit(fb1, 0, 0)
oled.show()

dht_read_time = time.time() # Defined a variable to keep last DHT11 read time

# Testing LED and Relay
relay.high()
time.sleep(0.5)
relay.low()
time.sleep(0.5)
led.high()
time.sleep(0.5)
led.low()
time.sleep(2)

while True:

    if time.time() - dht_read_time >= 3:
        dht_read_time = time.time()
        try:
            dht_sensor.measure()
        except Exception as e:
            print("Warning: could not measure: " + str(e))
   
    oled.fill(0)
    oled.text("PICOBRICKS",30, 0)
    oled.text("POT:      {0:.2f}V".format(pot.read_u16() * conversion_factor),0,20)
    oled.text("LIGHT:    {0:.2f}%".format((65535.0 - light_level.read_u16())/650.0),0,30)
    oled.text("TEMP:     {0:.2f}C".format(dht_sensor.temperature()),0,40)
    oled.text("HUMIDITY: {0:.1f}%".format(dht_sensor.humidity()),0,50)
    oled.show()
    time.sleep(1)
    oled.fill(0)