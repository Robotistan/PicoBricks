from machine import Pin
from dht import DHT11
from utime import sleep
dht_sensor = DHT11(11)

while True:
    sleep(1) # It was used for DHT11 to measure.
    dht_sensor.measure() # Use the sleep() command before this line.
    temp=dht_sensor.temperature()
    print(temp)
