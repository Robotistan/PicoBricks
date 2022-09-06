from machine import Pin #to access the hardware on the pico
import utime #time library
led = Pin(7,Pin.OUT)#initialize digital pin 7 as an output for LED
while True: #while loop
    led.toggle()# LED on&off status
    utime.sleep(0.5)#wait for a half second