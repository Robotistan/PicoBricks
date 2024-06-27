import time
from machine import Pin, I2C, PWM, ADC, UART
from picobricks import SSD1306_I2C, WS2812, NEC_16, IR_RX, SHTC3, MotorDriver
from resources import Note_img, Picobricks_img, Tones, Song
import framebuf
import random
import network
WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height
NOTE_DURATION = 0.11

uart = UART(0,9600) #RX-->GP0; TX-->GP01

#IR Data
ir_data = 0
data_rcvd = False

#Connect to Wifi
ssid = "SSID"
password = "PASSWORD"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
max_wait = 10

status = wlan.ifconfig()
i2c = I2C(0, scl=Pin(5), sda=Pin(4))   # Init I2C using pins
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)   # Init oled display
fb1 = framebuf.FrameBuffer(Picobricks_img, 128,64 , framebuf.MONO_HLSB) # Creating framebuffer for PicoBricks Logo
fb2 = framebuf.FrameBuffer(Note_img, 128,64, framebuf.MONO_HLSB)        # Creating framebuffer for music note
motor = MotorDriver(i2c)
shtc_sensor = SHTC3(i2c)

# Function declaration
def playtone(frequency):
    buzzer.duty_u16(5000)
    buzzer.freq(frequency)
   
def bequiet():
    buzzer.duty_u16(0)
    
def ir_callback(data, addr, ctrl):
    global ir_data
    global ir_addr, data_rcvd
    if data > 0:
        ir_data = data
        ir_addr = addr
        print('Data {:02x} Addr {:04x}'.format(data, addr))
        data_rcvd = True

def buttonInterruptHandler(event):    # Interrupt event, that will work when button is pressed
    if button.value() == 1:
        oled.fill(0)
        oled.blit(fb2, 0, 0)
        oled.show()
        for note in Song:
            if button.value() == 0:  # if button is released then reset ws2812, oled, buzzer and return
                ws2812.pixels_fill((0,0,0))
                ws2812.pixels_show()
                bequiet()
                oled.fill(0)
                #oled.show()
                break
            if note[0] == "-":
                bequiet()
            else:
                playtone(Tones[note[0]])
                ws2812.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                ws2812.pixels_show()
            time.sleep(NOTE_DURATION*note[1])
            
def scroll_in_screen(screen):
  for i in range (0, WIDTH+1, 2):
    for line in screen:
      oled.text(line[2], -WIDTH+i, line[1])
    oled.show()
    if i!= WIDTH:
      oled.fill(0)
def scroll_out_screen(speed):
  for i in range ((WIDTH+1)/speed):
    for j in range (WIDTH):
      oled.pixel(i, j, 0)
    oled.scroll(speed,0)
    oled.show()
    
# Pin Initialization
buzzer = PWM(Pin(20)) # setting GP20 as PWM pin
buzzer.duty_u16(0)    # setting duty cycle to 0
relay = Pin(12, Pin.OUT)
button = Pin(10, Pin.IN) # setting GP10 PIN as input
pot = ADC(26)
light_level = ADC(27)
conversion_factor = 3.3 / (65535)
led = Pin(7, Pin.OUT)
ws2812 = WS2812(6,brightness=1)
ir = NEC_16(Pin(0, Pin.IN), ir_callback)
button.irq(trigger=Pin.IRQ_RISING, handler=buttonInterruptHandler)  # Button 1 pressed interrupt is set. buttonInterruptHandler function will run when button is pressed
oled.fill(0)
oled.blit(fb1, 0, 0)
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
    
screen1 = [[0, 0 , 'ip = ' + status[0]]]    
# Testing LED and Relay
relay.high()
time.sleep(0.5)
relay.low()
time.sleep(0.5)
led.high()
time.sleep(0.5)
led.low()
time.sleep(2)

while True:
    if uart.any():
        command = uart.readline()
        print(command)
        if command==b'\x31': #Text '1' = chr(0x31)
            led.high()
            print("ON")
        elif command==b'\x30': #Text '0' = chr(0x30)
            led.low()
            print("OFF")
    if data_rcvd == True:
        data_rcvd = False
        if ir_data == IR_RX.number_1:
            ws2812.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            ws2812.pixels_show()
            time.sleep(1)
            ws2812.pixels_fill((0,0,0))
            ws2812.pixels_show()
        if ir_data == IR_RX.number_2:
            led.toggle()
        if ir_data == IR_RX.number_3:
            relay.toggle()
        if ir_data == IR_RX.number_4:
            motor.dc(1,255,1)
        if ir_data == IR_RX.number_5:
            motor.dc(2,255,1)
        if ir_data == IR_RX.number_6:   
            buzzer.duty_u16(2000)
            buzzer.freq(831)
            time.sleep(0.5)
            buzzer.duty_u16(0)
        if ir_data == IR_RX.number_7:
            oled.fill(0)
            oled.blit(fb2, 0, 0)
            oled.show()
            for note in Song:
                if ir_data == IR_RX.number_ok:  # if button is released then reset ws2812, oled, buzzer and return
                    ws2812.pixels_fill((0,0,0))
                    ws2812.pixels_show()
                    bequiet()
                    oled.fill(0)
                    oled.show()
                    break
                if note[0] == "-":
                    bequiet()
                else:
                    playtone(Tones[note[0]])
                    ws2812.pixels_fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                    ws2812.pixels_show()
                time.sleep(NOTE_DURATION*note[1])
        if ir_data == IR_RX.number_8:
            motor.servo(1,90)
        if ir_data == IR_RX.number_9:
            motor.servo(1,0)    
        if ir_data == IR_RX.number_ok:
            relay.low()
            motor.dc(1,0,1)
            time.sleep(1)
            motor.dc(1,0,1)
            led.low()
        if ir_data == IR_RX.number_up:
            scroll_in_screen(screen1)
            scroll_out_screen(4)
            
    tempSHTC = shtc_sensor.temperature()
    humiditySHTC = shtc_sensor.humidity()
    oled.fill(0)
    oled.text("PICOBRICKS",30, 0)
    oled.text("POT:      {0:.2f}V".format(pot.read_u16() * conversion_factor),0,10)
    oled.text("LIGHT:    {0:.2f}%".format((65535.0 - light_level.read_u16())/650.0),0,20)
    oled.text("TEMP:     {0:.2f}C".format(tempSHTC),0,30)
    oled.text("HUMIDITY: {0:.1f}%".format(humiditySHTC),0,40)
    oled.text("IP:" + status[0],0,50)
    oled.show()
    time.sleep(1)
    oled.fill(0)
