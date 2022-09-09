from machine import Pin,PWM,ADC #to acces the hardware picobricks
from utime import sleep #time library

button= Pin(10,Pin.IN,Pin.PULL_DOWN)
pot=ADC(Pin(26))
buzzer= PWM(Pin(20))
#determine our input and output pins
global rithm
pressed = False

tones = {
"A3": 220,
"D4": 294,
"E4": 330,
"F4": 349
}
#define the tones

mysong = ["A3","E4","E4","E4","E4","E4","E4","F4","E4","D4","F4","E4"]#let's define the tones required for our song in the correct order into a sequence
noteTime = [1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1]#define wait times between tones into an array

def playtone(frequency):
    buzzer.duty_u16(6000)
    buzzer.freq(frequency)
#define the frequencies of the buzzer
def playsong(pin):
    global pressed
    
    if not pressed:
        pressed = True
        for i in range(len(mysong)):
                playtone(tones[mysong[i]])
                sleep(noteTime[i]/rithm+1)
        buzzer.duty_u16(0)
#play the tones with the right cooldowns
#An finally we need to tell the pins when to trigger, and the function to call when they detect an event:       
button.irq(trigger=Pin.IRQ_RISING, handler=playsong)
while True:
    rithm= pot.read_u16()
    rithm= int(rithm/6400)+1
