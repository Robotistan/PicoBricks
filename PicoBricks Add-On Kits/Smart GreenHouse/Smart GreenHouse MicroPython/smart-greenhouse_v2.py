import time
from machine import Pin, I2C, ADC
from picobricks import SSD1306_I2C, NEC_16, IR_RX, SHTC3, MotorDriver
from resources import Picobricks_img,
import framebuf

WIDTH  = 128   # oled display width
HEIGHT = 64    # oled display height

soil_min = 40000
soil_max = 64000

user_soil_value = 0
counter = 0

soil_values = bytearray(5)

ir_data = 0
data_rcvd = False

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=200000)   # Init I2C using pins
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c,0)   # Init oled display
fb1 = framebuf.FrameBuffer(Picobricks_img, 128,64 , framebuf.MONO_HLSB) # Creating framebuffer for PicoBricks Logo
motor = MotorDriver(i2c)
shtc_sensor = SHTC3(i2c)

def ir_callback(data, addr, ctrl):
    global ir_data
    global ir_addr, data_rcvd
    if data > 0:
        ir_data = data
        ir_addr = addr
        #print('Data {:02x} Addr {:04x}'.format(data, addr))
        data_rcvd = True
        
def buttonInterruptHandler(event):
    while True:
        if button.value() == 1:
            motor.dc(1,200,1)
            led.high()
        else:
            motor.dc(1,0,1)
            led.low()
            break
        
def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
def soil_screen(value):
    global user_soil_value
    
    user_soil_value *= 10
    user_soil_value += value
    oled.fill(0)
    oled.text("User Soil:", 0, 0)
    oled.text(str(user_soil_value), 90, 0)
    if user_soil_value <= 9:
        oled.text("Press Two Numbers", 0, 10)
        oled.text("From Remote ",0,20)
        oled.text("Controller",0,30)
    else:
        oled.text("Press OK Button From Remote Controller For Exit Menu", 0, 20)
    oled.show()
    time.sleep(1)

# Pin Initialization
soil_pin = ADC(Pin(28))
button = Pin(10, Pin.IN)
led = Pin(7, Pin.OUT)
light_level = ADC(27)
ir = NEC_16(Pin(0, Pin.IN), ir_callback)

oled.blit(fb1, 0, 0)
oled.show()

button.irq(trigger=Pin.IRQ_RISING, handler=buttonInterruptHandler)

while True:
    time.sleep(0.5)
    soil = soil_pin.read_u16()
    print(soil)
        
    if soil >= soil_max:
        soil = 64000
    elif soil <= soil_min:
        soil = 40000
        
    soil_value = 100 - (convert(soil, soil_min, soil_max, 0, 100))
    
    if counter >= 5:
        counter = 0
    else:
        soil_values[counter] = soil_value
        
    if data_rcvd == True:
        data_rcvd = False
        if ir_data == IR_RX.number_star:
            user_soil_value = 0
            oled.fill(0)
            oled.show()
            oled.text("User Soil:", 0, 0)
            oled.text("Press Two Numbers", 0, 10)
            oled.text("From Remote ",0,20)
            oled.text("Controller",0,30)
            oled.show()
            while True:
                if data_rcvd == True:
                    data_rcvd = False
                    if ir_data == IR_RX.number_0:
                        soil_screen(0)
                    if ir_data == IR_RX.number_1:
                        soil_screen(1)
                    if ir_data == IR_RX.number_2:
                        soil_screen(2)
                    if ir_data == IR_RX.number_3:
                        soil_screen(3)
                    if ir_data == IR_RX.number_4:
                        soil_screen(4)
                    if ir_data == IR_RX.number_5:
                        soil_screen(5)
                    if ir_data == IR_RX.number_6:
                        soil_screen(6)
                    if ir_data == IR_RX.number_7:
                        soil_screen(7) 
                    if ir_data == IR_RX.number_8:
                        soil_screen(8)
                    if ir_data == IR_RX.number_9:
                        soil_screen(9)
                    if ir_data == IR_RX.number_ok:
                        if user_soil_value > 100:
                            user_soil_value = 0
                            soil_screen(0)
                        else:
                            oled.fill(0)
                            oled.text("User Soil Value",0,0)
                            oled.text("Saved",0,10)
                            oled.show()
                            time.sleep(1.5)
                            break
                    
    avr_soil_value = (soil_values[0] + soil_values[1] + soil_values[2] + soil_values[3] + soil_values[4]) / 5
        
    oled.fill(0)
    oled.text("LIGHT:    {0:.2f}%".format((65535.0 - light_level.read_u16())/650.0),0,0)
	oled.text("TEMP:     {0:.2f}C".format(tempSHTC),0,10)
	oled.text("HUMIDITY: {0:.1f}%".format(humiditySHTC),0,20)
    oled.text("SOIL:     {0:.1f}%".format(avr_soil_value),0,30)
    oled.text("USER SOIL:{0:.0}%".format(user_soil_value),0,40)
    oled.text("* For Set Soil",0,50)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    counter += 1
    
    if ((soil_value <= user_soil_value) and (user_soil_value != 0)):
        start = time.time()
        while time.time() < start + 5:
            motor.dc(1,200,1)
            led.high()
        motor.dc(1,0,1)
        led.low()
