import time
from machine import Pin, I2C, PWM, ADC
from picobricks import SSD1306_I2C
import framebuf
import random               #random, neopixelin rastgele çalışmasını sağlıyor.
from picobricks import WS2812#ws8212 library
from crazyfrog_imgs import bar_0, bar_20, bar_50, bar_70, bar_90, bar_100, maskot_1, maskot_2, maskot_3, maskot_4 #imgs, kütüphanesini çalıştırıyoruz ve görselleri kütüphaneden kullanıyoruz.


WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height


i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)                  # Init oled display

bar1 = framebuf.FrameBuffer(bar_0, 128,64 , framebuf.MONO_HLSB)
bar2 = framebuf.FrameBuffer(bar_20, 128,64 , framebuf.MONO_HLSB)
bar3 = framebuf.FrameBuffer(bar_50, 128,64 , framebuf.MONO_HLSB)
bar4 = framebuf.FrameBuffer(bar_70, 128,64 , framebuf.MONO_HLSB)
bar5 = framebuf.FrameBuffer(bar_90, 128,64 , framebuf.MONO_HLSB)
bar6 = framebuf.FrameBuffer(bar_100, 128,64 , framebuf.MONO_HLSB)
maskot1 = framebuf.FrameBuffer(maskot_1, 128,64 , framebuf.MONO_HLSB)
maskot2 = framebuf.FrameBuffer(maskot_2, 128,64 , framebuf.MONO_HLSB)
maskot3 = framebuf.FrameBuffer(maskot_3, 128,64 , framebuf.MONO_HLSB)
maskot4 = framebuf.FrameBuffer(maskot_4, 128,64 , framebuf.MONO_HLSB)

notes = { 
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}

crazy_frog_melody = [
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'], 
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'], 
	notes['A4'],0,
	
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'], 
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'], 
	notes['A4'],0,
	
	
	notes['A3'], notes['G3'], notes['E3'], notes['D3'],
	
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'], 
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'], 
	notes['A4'],
]

crazy_frog_tempo = [
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,4,
	
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,4,
	
	8,4,4,4,
	
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,
]

oled.blit(bar1, 0, 0)
oled.show()
time.sleep(1)
oled.blit(bar2, 0, 0)
oled.show()
time.sleep(1)
oled.blit(bar3, 0, 0)
oled.show()
time.sleep(1)
oled.blit(bar4, 0, 0)
oled.show()
time.sleep(1)
oled.blit(bar5, 0, 0)
oled.show()
time.sleep(1)
oled.blit(bar6, 0, 0)
oled.show()
time.sleep(1)

buzzer = PWM(Pin(20))
buzzer.duty_u16(0)

neo = WS2812(6, brightness=0.4)

maskot_position = 0

def buzz(frequency, length): #create the function "buzz" and feed it the pitch and duration)

    if(frequency==0):
        time.sleep(length)
        return
    buzzer.duty_u16(4000)
    buzzer.freq(frequency)
    time.sleep(length)
    buzzer.duty_u16(0)

def play(melody,tempo,pause,pace=0.7):
    global maskot_position
    for i in range(0, len(melody)): # Play song
        
        noteDuration = pace/tempo[i]
        buzz(melody[i],noteDuration)    # Change the frequency along the song note
        pauseBetweenNotes = noteDuration * pause
        time.sleep(pauseBetweenNotes)
        neo.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        neo.pixels_show()
        if maskot_position == 0:
            oled.blit(maskot1, 0, 0)
            maskot_position = 1
        elif maskot_position == 1:
            oled.blit(maskot2, 0, 0)
            maskot_position = 2
        elif maskot_position == 2:
            oled.blit(maskot3, 0, 0)
            maskot_position = 3
        elif maskot_position == 3:
            oled.blit(maskot4, 0, 0)
            maskot_position = 0
        oled.show()
play(crazy_frog_melody, crazy_frog_tempo, 0.1)