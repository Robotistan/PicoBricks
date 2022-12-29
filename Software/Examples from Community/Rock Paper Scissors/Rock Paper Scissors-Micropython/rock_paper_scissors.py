#Rock-Paper-Scissors Game

from machine import I2C, Pin, SPI, PWM, ADC
from utime import sleep 
from picobricks import SSD1306_I2C, WS2812
import framebuf
import random
from rps_images import rock,paper,scissors,start, Tones, win_song, time_song, loading

WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height

servo = PWM(Pin(21))

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)   # Init I2C using pins (default I2C0 pins)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display
ws2812 = WS2812(13,6,brightness=1)

fb1 = framebuf.FrameBuffer(rock, 128,64 , framebuf.MONO_HLSB)
fb2 = framebuf.FrameBuffer(paper, 128,64, framebuf.MONO_HLSB)       
fb3 = framebuf.FrameBuffer(scissors, 128,64, framebuf.MONO_HLSB)
loading = framebuf.FrameBuffer(loading, 128,64, framebuf.MONO_HLSB)
start = framebuf.FrameBuffer(start, 128,64, framebuf.MONO_HLSB)

buzzer = PWM(Pin(20))
buzzer.duty_u16(0)

button = Pin(10, Pin.IN)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display

oledVisuals = [fb1, fb2, fb3]

servoPositions = [8500, 5500, 3500]

RED = (255, 0, 0)
BLUE =(0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 100, 0)
resultColors = [RED, BLUE, GREEN]
analog_value = ADC(28)


def neo():
    for i in range(0,13):
        ws2812.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        sleep(0.05)
        ws2812.pixels_show()
def winningSound():
    for note, duration in win_song:
        buzzer.freq(Tones[note])
        buzzer.duty_u16(5000)
        sleep(duration*0.1)
        buzzer.duty_u16(0)
        sleep(duration*0.1)
        
def timesong():
    for note, duration in time_song:
        buzzer.freq(Tones[note])
        buzzer.duty_u16(5000)
        sleep(duration*0.07)
        buzzer.duty_u16(0)
        sleep(duration*0.07)

def Sweep(i):
    servo.freq(50)
    ws2812.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    ws2812.pixels_show()   
    for position in range(4000,8000,500):
        servo.duty_u16(position)
        sleep(0.01)
    for position in range(8000,4000,-500):
        servo.duty_u16(position)
        sleep(0.01)
    oled.fill(0)
    oled.blit(oledVisuals[i], 0, 0)
    oled.show()
    timesong()

random.seed(analog_value.read_u16())

while True:

    if  button.value() == 1:
        servo.freq(50)
        servo.duty_u16(5500)
        sleep(0.01)
        oled.blit(loading, 0, 0)
        oled.show()
        sleep(1)
        oled.fill(0)
        result = random.randint(0,2)

        for i in range(3):
            Sweep(i)
            sleep(0.1)

        servo.freq(50)
        servo.duty_u16(servoPositions[result])
        oled.blit(oledVisuals[result], 0, 0)
        oled.show()
        ws2812.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        ws2812.pixels_show()
        winningSound()
        sleep(2)
        print(servoPositions[result])
        print(result)
    else:
        servo.freq(50)
        servo.duty_u16(2000)
        oled.blit(start, 0, 0)
        oled.show()
        ws2812.pixels_fill(ORANGE)
        ws2812.pixels_show()


