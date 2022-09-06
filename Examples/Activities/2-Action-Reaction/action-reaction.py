from machine import Pin#to acces the hardware picobricks
led = Pin(7,Pin.OUT)#initialize digital pin as an output for led
push_button = Pin(10,Pin.IN,Pin.PULL_DOWN)#initialize digital pin 10 as an input
while True:#while loop
    logic_state = push_button.value();#button on&off status
    if logic_state == True:#check the button and if it is on
        led.value(1)#turn on the led
    else:
        led.value(0)#turn off the led