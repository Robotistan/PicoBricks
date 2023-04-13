# Control an LED and read a Button using a web browser
import time
import network
import socket
from machine import Pin,PWM,ADC
from picobricks import SSD1306_I2C,WS2812, DHT11,NEC_16, IR_RX
from utime import sleep
import utime
#from time import sleep
WIDTH = 128
HEIGHT = 64
#IR Data
ir_data = 0
data_rcvd = False

sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
light = ADC(Pin(27))
ws = WS2812(6, brightness=0.4)
led = Pin(7, Pin.OUT)
ledState = 'LED State Unknown'
"""
oledState = 'LED State Unknown'
rgbState = 'LED State Unknown'
dhtState = 'LED State Unknown'
relayState = 'LED State Unknown'
motordriverState = 'LED State Unknown'
irState = 'LED State Unknown'
buzzerState = 'LED State Unknown'
ldrState = 'LED State Unknown'
potState = 'LED State Unknown'
"""
pico_temp=DHT11(Pin(11, Pin.IN, Pin.PULL_UP))
current_time=utime.time()
utime.sleep(1)
button = Pin(10, Pin.IN, Pin.PULL_DOWN)
#define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = (RED, GREEN, BLUE)
pot=ADC(Pin(26))
pot_val = 0
pico_temp=DHT11(Pin(11))
current_time=utime.time()

ssid = "Wifi_name"
password = "Wifi_password"

servo1=PWM(Pin(21))
servo2=PWM(Pin(22))
servo1.freq(50)
servo2.freq(50)

relay = Pin(12, Pin.OUT)

motor_1 = Pin(21, Pin.OUT)
motor_2 = Pin(22, Pin.OUT)

buzzer = PWM(Pin(20))
buzzer.duty_u16(0)

def ir_callback(data, addr, ctrl):
    global ir_data
    global ir_addr, data_rcvd
    if data > 0:
        ir_data = data
        ir_addr = addr
        print('Data {:02x} Addr {:04x}'.format(data, addr))
        data_rcvd = True

ir = NEC_16(Pin(0, Pin.IN), ir_callback)

angleupdown=4770
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #D11D53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
button{background-color:#f8b332; border-radius:10px; width:150px; height:50px; color:white;}
.body_div{display:flex; flex-direction:row; justify-content:center; align-items: center; }
.left_div{display:flex; flex-direction:column; margin-right:10px;}
.right_div{display:flex; flex-direction:column;}
.center_div{display:flex; margin-bottom:5px; justify-content: center; align-items: center;}
.one_div{display:flex; flex-direction:row; margin:auto; width:200px; height:100px; justify-content:center; background-color:#228e73; align-items: center; border-radius:10px; box-shadow: 5px 10px 18px #888888; margin-bottom:5px;}
.one_div2{display:flex; flex-direction:row; margin:auto; width:200px; height:100px; justify-content:center; background-color:#ee7131; align-items: center; border-radius:10px; box-shadow: 5px 10px 18px #888888; margin-bottom:5px;}
.buttonOLED_off{background-color:#e62b2b;}
.buttonLED_off{background-color:#e62b2b;}
.buttonRGB_off{background-color:#e62b2b;}
.buttonDHT_off{background-color:#e62b2b;}
.buttonrelay_off{background-color:#e62b2b;}
.buttonmotordriver_off{background-color:#e62b2b;}
.buttonir_off{background-color:#e62b2b;}
.buttonbuzzer_off{background-color:#e62b2b;}
.buttonldr_off{background-color:#e62b2b;}
.buttonpot_off{background-color:#e62b2b;}
body{background-color:white;}
</style></head>
<body><center><h1>Control Panel</h1></center>

<form>
<div class="body_div">
    <div class="left_div">
        <div class="center_div">
            <div class="one_div">
                <button class="buttonOLED" name="oled" value="on" type="submit">OLED ON</button>
                <button class="buttonOLED_off" name="oled" value="off" type="submit">OLED OFF</button>
            </div>
        </div>
        <div class="center_div">
            <div class="one_div2">
                <button class="buttonRGB" name="RGBled" value="on" type="submit">RGBLED ON</button>
                <button class="buttonRGB_off" name="RGBled" value="off" type="submit">RGBLED OFF</button>
            </div>
        </div>

        <div class="center_div">
            <div class="one_div">
                <button class="buttonLED" name="led" value="on" type="submit">LED ON</button>
                <button class="buttonLED_off" name="led" value="off" type="submit">LED OFF</button>
            </div>
        </div>


        <div class="center_div">
            <div class="one_div2">
                <button class="buttonDHT" name="DHT" value="on" type="submit">DHT ON</button>
                <button class="buttonDHT_off" name="DHT" value="off" type="submit">DHT OFF</button>
            </div>
        </div>

        <div class="center_div">
            <div class="one_div">
                <button class="buttonrelay" name="relay" value="on" type="submit">RELAY ON</button>
                <button class="buttonrelay_off" name="relay" value="off" type="submit">RELAY OFF</button>
            </div>
        </div>
    
    </div>
    <div class="right_div">
        <div class="center_div">
            <div class="one_div2">
                <button class="buttonmotordriver" name="motordriver" value="on" type="submit">Motor Driver ON</button>
                <button class="buttonmotordriver_off" name="motordriver" value="off" type="submit">Motor Driver OFF</button>
            </div>
        </div>

        <div class="center_div">
            <div class="one_div">
                <button class="buttonir" name="ir" value="on" type="submit">IR ON</button>
                <button class="buttonir_off" name="ir" value="off" type="submit">IR OFF</button>
            </div>
        </div>

        <div class="center_div">
            <div class="one_div2">
                <button class="buttonbuzzer" name="buzzer" value="on" type="submit">BUZZER ON</button>
                <button class="buttonbuzzer_off" name="buzzer" value="off" type="submit">BUZZER OFF</button>
            </div>
        </div>

        <div class="center_div">
            <div class="one_div">
                <button class="buttonldr" name="ldr" value="on" type="submit">LDR ON</button>
                <button class="buttonldr_off" name="ldr" value="off" type="submit">LDR OFF</button>
            </div>
        </div>

        <div class="center_div">
            <div class="one_div2">
                <button class="buttonpot" name="pot" value="on" type="submit">POT ON</button>
                <button class="buttonpot_off" name="pot" value="off" type="submit">POT OFF</button>
            </div>
        </div>
    </div>
</div>





</form>

<p>%s<p></body></html>
"""
oled.text("Power On",30,0)
oled.text("Waiting for ",20, 30)
oled.text("Connection",23, 40)
oled.show()
time.sleep(2)
oled.fill(0)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
oled.text("IP",50, 0)
oled.text(str(status[0]),20, 10)
oled.text("Connected",25, 20)
oled.show()
# Listen for connections, serve client
#Servo

if(utime.time() - current_time > 2):
    current_time = utime.time()
    try:
        pico_temp.measure()
    except:
        print("measurement failed, will try again soon")

temperature=pico_temp.temperature
humidity=pico_temp.humidity
   
while True:
    sleep(0.1)  
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        oled_on = request.find('oled=on')
        oled_off = request.find('oled=off')
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        RGBled_on = request.find('RGBled=on')
        RGBled_off = request.find('RGBled=off')
        DHT_on = request.find('DHT=on')
        DHT_off = request.find('DHT=off')
        relay_on = request.find('relay=on')
        relay_off = request.find('relay=off')
        motordriver_on = request.find('motordriver=on')
        motordriver_off = request.find('motordriver=off')
        ir_on = request.find('ir=on')
        ir_off = request.find('ir=off')
        buzzer_on = request.find('buzzer=on')
        buzzer_off = request.find('buzzer=off')
        ldr_on = request.find('ldr=on')
        ldr_off = request.find('ldr=off')
        pot_on = request.find('pot=on')
        pot_off = request.find('pot=off')
        
        print( 'oled on = ' + str(oled_on))
        print( 'oled off = ' + str(oled_off))
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        print( 'RGBled on = ' + str(RGBled_on))
        print( 'RGBled off = ' + str(RGBled_off))
        print( 'DHT on = ' + str(DHT_on))
        print( 'DHT off = ' + str(DHT_off))
        print( 'relay on = ' + str(relay_on))
        print( 'relay off = ' + str(relay_off))
        print( 'motordriver on = ' + str(motordriver_on))
        print( 'motordriver off = ' + str(motordriver_off))
        print( 'ir on = ' + str(ir_on))
        print( 'ir off = ' + str(ir_off))
        print( 'buzzer on = ' + str(buzzer_on))
        print( 'buzzer off = ' + str(buzzer_off))
        print( 'ldr on = ' + str(ldr_on))
        print( 'ldr off = ' + str(ldr_off))
        print( 'pot on = ' + str(pot_on))
        print( 'pot off = ' + str(pot_off))
        
        
            
        if oled_on == 8:
            print("oled on")
            oled.fill(0)#clear OLED
            oled.text("Hello World",15,0)
            oled.text("My name is",15,10)
            oled.text("PicoBricks",15,20)
            oled.show()
            
        if oled_off == 8:
            print("oled off")
            oled.fill(0)#clear OLED
            oled.show()
            
            
        if led_on == 8:
            print("led on")
            led.value(1)
            
           
           
        if led_off == 8:
            print("led off")
            led.value(0)
            
            
        if RGBled_on == 8:
            print("RGBled on")
            for color in COLORS:
            #turn on the LDR
                ws.pixels_fill(color)
                ws.pixels_show()
        
        if RGBled_off == 8:
            print("RGBled off")
            ws.pixels_fill((0,0,0))  #turn off the RGB
            ws.pixels_show()
        
        if relay_on == 8:
            print("RELAY on")
            relay.high()
            time.sleep(0.5)
        
        if relay_off == 8:
            print("RELAY off")
            relay.low()
            time.sleep(0.5)
            
        if motordriver_on == 8:
            print("Motor Driver on")
            motor_1.high()
            motor_2.high()
            servo1.duty_u16(4010) #180 degree
            sleep(0.3)
            servo1.duty_u16(8000) #180 degree
            sleep(0.3)
            servo2.duty_u16(4010) #180 degree
            sleep(0.3)
            servo2.duty_u16(8000) #180 degree
            sleep(0.3)
        
        if motordriver_off == 8:
            print("Motor Driver off")
            motor_1.low()
            motor_2.low()
            servo1.duty_u16(4010) #180 degree
            sleep(0.3)
            servo2.duty_u16(4010) #180 degree
            sleep(0.3)
        if ir_on == 8:
            if data_rcvd == True:
                data_rcvd = False
                print("IR on")
                print(ir_data)
                if ir_data == IR_RX.number_1:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Number 1 ",10,20)
                    oled.show()
                if ir_data == IR_RX.number_2:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Number 2 ",10,20)
                    oled.show()
                if ir_data == IR_RX.number_3:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Number 3 ",10,20)
                    oled.show()
                    
                if ir_data == IR_RX.number_4:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Number 4 ",10,20)
                    oled.show()
                
                if ir_data == IR_RX.number_5:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Number 5 ",10,20)
                    oled.show()
                if ir_data == IR_RX.number_6:   
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Number 6 ",10,20)
                    oled.show()
                if ir_data == IR_RX.number_ok:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("OK Button ",10,20)
                    oled.show()
                if ir_data == IR_RX.number_up:
                    oled.show()
                    oled.fill(0)
                    
                    oled.text("Up Button",10,20)
                    oled.show()
        if ir_off == 8:
            print("IR off")
            oled.show()
            oled.fill(0)
               
        if buzzer_on == 8:
            print("BUZZER on")
            buzzer.duty_u16(2000)
            buzzer.freq(831)
        
        if buzzer_off == 8:
            print("BUZZER off")
            buzzer.duty_u16(0)
            time.sleep(0.5)
            
        if pot_on == 8:
            print("POT on")   
            pot_val=((pot.read_u16()/65535.0)*20) +1
            oled.fill(0)
            oled.show()
            oled.text("POT: ",15,40)
            oled.text(str(int(pot_val)),55,40)
            oled.show()
        
        if pot_off == 8:
            print("POT off")
            oled.fill(0)#clear OLED
            oled.show()
            
        if ldr_on == 8:
            print("LDR on")
            oled.fill(0)#clear OLED
            print(light.read_u16()) #print the value of the LDR sensor to the screen.
            oled.show()
            oled.text("LDR: ",15,30)#print "Temperature: " on the OLED at x=15 y=10
            oled.text(str(light.read_u16()),55,30)
            oled.show()
            #if(light.read_u16()>50000):#let's check the ldr sensor
                #for color in COLORS:
                        
                        #turn on the LDR
                    #ws.pixels_fill(color)
                    #ws.pixels_show()
                            
            #else:
                #ws.pixels_fill((0,0,0))  #turn off the RGB
                #ws.pixels_show()
        
        if ldr_off == 8:
            print("LDR off")
            #ws.pixels_fill((0,0,0))  #turn off the RGB
            #ws.pixels_show()
            oled.fill(0)#clear OLED
            oled.show()
            
        if DHT_on == 8:
            print("DHT on")
            
            if(utime.time() - current_time > 2):
                current_time = utime.time()
                try:
                    pico_temp.measure()
                except:
                    print("measurement failed, will try again soon")
            
            oled.fill(0)#clear OLED
            oled.show()
            
            
            temperature=pico_temp.temperature
            humidity=pico_temp.humidity
            
            oled.text("Temp: ",15,0)#print "Temperature: " on the OLED at x=15 y=10
            oled.text(str(int(temperature)),55,0)
            oled.text("Hum: ", 15,10)
            oled.text(str(int(humidity)),55,10)
            oled.show()#show on OLED
            utime.sleep(0.5)#wait for a half second
        
        if DHT_off == 8:
            print("DHT off")
            oled.fill(0)#clear OLED
            oled.show()
        
        ledState = "" if led.value() == 0 else "" # a compact if-else statement
        """
        oledState = "OLED is OFF" if oled.value() == 0 else "OLED is ON" # a compact if-else statement
        rgbState = "RGB LED is OFF" if RGBled.value() == 0 else "RGB LED is ON" # a compact if-else statement
        dhtState = "DHT is OFF" if DHT.value() == 0 else "DHT is ON" # a compact if-else statement
        relayState = "RELAY is OFF" if relay.value() == 0 else "RELAY is ON" # a compact if-else statement
        motordriverState = "Motor Driver is OFF" if motordriver.value() == 0 else "Motor Driver is ON" # a compact if-else statement
        irState = "Infrared is OFF" if ir.value() == 0 else "Infrared is ON" # a compact if-else statement
        buzzerState = "Buzzer is OFF" if buzzer.value() == 0 else "Buzzer is ON" # a compact if-else statement
        ldrState = "LDR is OFF" if ldr.value() == 0 else "LDR is ON" # a compact if-else statement
        potState = "Potentiometer is OFF" if pot.value() == 0 else "Potentiometer is ON" # a compact if-else statement
        """
        if button.value() == 0: # button not pressed
            print("button NOT pressed")
            buttonState = ""
            
        else:
            print("button pressed")
            buttonState = ""
            
        # Create and send response
        
        stateis = ledState + "" + buttonState
        
        """if oled.value() == 0:
            stateis = oledState + " and " + buttonState
        
        if RGBled.value() == 0:
            stateis = rgbState + " and " + buttonState
        
        if DHT.value() == 0:
            stateis = dhtState + " and " + buttonState
        
        if relay.value() == 0:
            stateis = relayState + " and " + buttonState
        
        if motordriver.value() == 0:
            stateis = motordriverState + " and " + buttonState
        
        if ir.value() == 0:
            stateis = irState + " and " + buttonState
        
        if buzzer.value() == 0:
            stateis = buzzerState + " and " + buttonState
        
        if ldr.value() == 0:
            stateis = ldrState + " and " + buttonState
        
        if pot.value() == 0:
            stateis = potState + " and " + buttonState"""
        
        
        
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')


