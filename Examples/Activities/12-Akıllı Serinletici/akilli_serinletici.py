from machine import Pin
from dht import DHT11
from utime import sleep
dht_sensor = DHT11(11)
m1 = Pin(21, Pin.OUT)
m1.low()

while True:
    sleep(1) # It was used for DHT11 to measure.
    dht_sensor.measure() # Use the sleep() command before this line.
    temp=dht_sensor.temperature()
    print(temp)
    if temp>=28.0:
        m1.high()
    else:
        m1.low()