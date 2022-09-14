from machine import Pin
from picobricks import DHT11
import utime

LIMIT_TEMPERATURE = 27

dht_sensor = DHT11(Pin(11, Pin.IN, Pin.PULL_DOWN))
m1 = Pin(21, Pin.OUT)
m1.low()

dht_read_time = utime.time()

while True:
    if utime.time() - dht_read_time >= 3:
        dht_read_time = utime.time()
        dht_sensor.measure()
        temp= dht_sensor.temperature
        print(temp)
        if temp >= LIMIT_TEMPERATURE:
            m1.high()
        else:
            m1.low()
