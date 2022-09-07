from machine import Pin
sensor=Pin(16,Pin.IN)
relay=Pin(12,Pin.OUT)
x=0
while True:
    if sensor.value()==0:
        if x==0:
            relay.value(1)
            x=1
        else:
            relay.value(0)
            x=0
