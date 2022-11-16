from machine import Pin #to access the hardware on the pico
sensor=Pin(1,Pin.IN) #initialize digital pin 1 as an INPUT for Sensor
led=Pin(7,Pin.OUT)#initialize digital pin 7 as an OUTPUT for LED
while True:
    #When sensor value is '0', the relay will be '1'
    print(sensor.value())
    if sensor.value()==1:  
        led.value(1)  
    else:
        led.value(0)
           
