from machine import Pin,PWM,ADC
from utime import sleep

button= Pin(10,Pin.IN,Pin.PULL_DOWN)
pot=ADC(Pin(26))
buzzer= PWM(Pin(20))

global rithm
pressed = False

tones = {
"A3": 220,
"D4": 294,
"E4": 330,
"F4": 349
}

mysong = ["A3","E4","E4","E4","E4","E4","E4","F4","E4","D4","F4","E4"]
noteTime = [1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1]

def playtone(frequency):
    buzzer.duty_u16(6000)
    buzzer.freq(frequency)

def playsong(pin):
    global pressed
    
    if not pressed:
        pressed = True
        for i in range(len(mysong)):
                playtone(tones[mysong[i]])
                sleep(noteTime[i]/rithm+1)
        buzzer.duty_u16(0)
            
button.irq(trigger=Pin.IRQ_RISING, handler=playsong)
while True:
    rithm= pot.read_u16()
    rithm= int(rithm/6400)+1