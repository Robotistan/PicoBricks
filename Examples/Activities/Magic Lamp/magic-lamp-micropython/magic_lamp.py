from machine import Pin #to access the hardware on the pico
sensor=Pin(16,Pin.IN) #initialize digital pin 16 as an INPUT for Sensor
relay=Pin(12,Pin.OUT)#initialize digital pin 12 as an OUTPUT for Relay
x=0
while True:
    #When sensor value is '0', the relay will be '1'
    if sensor.value()==0:
        if x==0:
            relay.value(1)
            x=1
        else:
            relay.value(0)
            x=0
