import time
import network
import socket
from machine import Pin, ADC
from picobricks import SSD1306_I2C, DHT11
from time import sleep
WIDTH = 128
HEIGHT = 64
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

motor_1 = Pin(21, Pin.OUT)
motor_2 = Pin(22, Pin.OUT)

smo_sensor=ADC(27)
dht_sensor = DHT11(Pin(11))
dht_read_time = time.time() # Defined a variable to keep last DHT11 read time

#Connect to Wifi
ssid = "WiFi ID"
password = "WiFi Password"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
max_wait = 10
status = wlan.ifconfig()

oled.text("Power On",30,0)
oled.text("Waiting for ",20, 30)
oled.text("Connection",23, 40)
oled.show()

while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -=1
    print("waiting for connection...")
    time.sleep(1)
    
if wlan.status() !=3:
    print('network connection failed. Please Check ID and PASSWORD')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )


oled.fill(0)


html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonBlue { background-color: #0000FF; border: 2px solid #000000;; color: white; padding: 20px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonOrange { background-color: #FFA500; border: 2px solid #000000;; color: Black; padding: 20px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>
<body><center><h1>Smart Green House</h1></center><br><br>
<form><center>
<center> <button class="buttonBlue" name="watering" value="watering" type="submit">WATERING</button>
<br><br>
<center> <button class="buttonOrange" name="check" value="status" type="submit">Check Status</button>
</form>
<br><br>
<br><br>
<p>%s<p></body></html>
"""
html2 = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<body><center></center>
<form></form>

<p>%s<p></body></html>
"""

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
oled.text("IP",50, 0)
oled.text(str(status[0]),20, 20)
oled.text("Connected",25, 40)
oled.show()
# Listen for connections, serve client
tempexp = str()
humexp = str()
soilexp = str()
while True:
    
    if time.time() - dht_read_time >= 3:
        dht_read_time = time.time()
        try:
            dht_sensor.measure()
        except Exception as e:
            pass
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        watering = request.find('watering')
        checkstt = request.find('check')
        
        print( 'watering = ' + str(watering))
        print( 'checkstt = ' + str(checkstt))
        
        if watering == 8: # Sulama
            print("watering")
            motor_1.high()
            motor_2.high()
            sleep(1)
            motor_1.low()
            motor_2.low()
            if watering == 8:
                dhtstt = "Watering for 1 sec..."
        else: # Info
            smo=round((smo_sensor.read_u16()/65535)*100)
            temp=dht_sensor.temperature
            hum=dht_sensor.humidity
            dhtstt = "VALUES"
            soilstt = "Soil Sensor Value: "
            soilexp = str(smo) + "%"
            humexp = "Huminity: " +  str(hum) + "% "
            tempexp = "Temperature: "+ str(temp) + "% "
                   
        # Create and send response
        stateis2 = tempexp + humexp + " Soil: " + soilexp
        stateis = dhtstt
        response2 = html2 % stateis2
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.send(response2)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
