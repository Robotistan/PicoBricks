from machine import Pin, PWM
from utime import sleep
# define libraries
PIR=Pin(14, Pin.IN)
MQ2=Pin(1,Pin.IN)
buzzer=PWM(Pin(20,Pin.OUT))
redLed=Pin(7,Pin.OUT)
button=Pin(10,Pin.IN,Pin.PULL_DOWN)
# define output and input pins

activated=0
gas=0

while True:
    if button.value()==1:
        activated=1
        gas=0 
        sleep(3)
        redLed.value(1)
        buzzer.duty_u16(0)
    if MQ2.value()==1:
        gas=1
    if activated==1:
        if PIR.value()==1:
            buzzer.duty_u16(6000)
            buzzer.freq(440)
            sleep(0.2)
            buzzer.freq(330)
            sleep(0.1)
            buzzer.freq(494)
            sleep(0.15)
            buzzer.freq(523)
            sleep(0.3)
    if gas==1:
        buzzer.duty_u16(6000)
        buzzer.freq(330)
        sleep(0.5)
        redLed.value(1)
        buzzer.freq(523)
        sleep(0.5)
        redLed.value(0)
        # LED will light and buzzer will sound when PIR detects motion or MQ2 detects toxic gas
