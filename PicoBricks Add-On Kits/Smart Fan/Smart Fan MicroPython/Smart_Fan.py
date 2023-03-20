from machine import Pin, I2C, PWM, ADC
from picobricks import SSD1306_I2C, DHT11
import time

#OLED
WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display

motor_pin = machine.Pin(21, machine.Pin.OUT)


dht_pin = machine.Pin(11)
d = DHT11(Pin(11, Pin.OUT, Pin.PULL_DOWN))

red_led = machine.Pin(7, machine.Pin.OUT)

def display_temp_hum():
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    oled.fill(0)
    oled.text('Temp: %d C' % temp, 0, 0)
    oled.text('Hum: %d %%' % hum, 0, 10)
    oled.show()

def start_motor():
    motor_pin.value(1)
    red_led.value(1)
    print("Start")

# Motoru durduran fonksiyon
def stop_motor():
    motor_pin.value(0)
    red_led.value(0)
    print("Stop")
    
dht_read_time = time.time()

system_status = False
target_temp = 25

while True:
    target_temp = int(machine.ADC(26).read_u16() / 65535 * 50)
    
    if time.time() - dht_read_time >= 3:
        dht_read_time = time.time()
        d.measure()
        current_temperature = d.temperature
        print(current_temperature)

    
    if machine.Pin(10, machine.Pin.IN).value() == 1:
        system_status = ~system_status
    
    if (system_status):
        current_temperature = d.temperature
        target_temp = int(machine.ADC(26).read_u16() / 65535 * 50)
        oled.fill(0)
        oled.text('Target temp: %d C' % target_temp, 0, 40)
        oled.text('Current temp:%d C' % current_temperature, 0, 20)
        oled.show()
        if d.temperature > target_temp:
            start_motor()
        else:
            stop_motor()
    
    else:
        stop_motor()
        oled.fill(0)
        oled.text('Turned Off', 20, 30)
        oled.show()

    time.sleep(0.5)