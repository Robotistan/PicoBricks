from machine import Pin, I2C, Timer, ADC, PWM #to access the hardware on the pico
from ssd1306 import SSD1306_I2C #OLED Screen Library
from utime import sleep#Time Library
import utime
import urandom

#OLED Screen Settings
WIDTH  = 128                                            
HEIGHT = 64                                          
sda=machine.Pin(4)#initialize digital pin 4 and 5 as an OUTPUT for OLED Communication
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(128, 64, i2c)

buzzer = PWM(Pin(20))#initialize digital PWM pin 20 as an OUTPUT for Buzzer
buzzer.freq(440)
ldr=ADC(27)#initialize digital pin 27  
button=Pin(10,Pin.IN,Pin.PULL_DOWN) #initialize digital 10 as an INPUT for BUTTON

#OLED Screen Texts Settings
oled.text("NIGHT and DAY", 10, 0)
oled.text("<GAME>", 40, 20)
oled.text("Press the Button", 0, 40)
oled.text("to START!", 40, 55)
oled.show()

def changeWord():
    global nightorday
    oled.fill(0)
    oled.show()
    nightorday=round(urandom.uniform(0,1))
    #When data is '0' ,OLED texts NIGHT
        oled.text("---NIGHT---", 20, 30)
        oled.show()
    #When data is '1' ,OLED texts DAY
    else:
        oled.text("---DAY---", 20, 30)
        oled.show()
# waits for the button to be pressed to activate 
while button.value()==0:
    print("Press the Button")
    sleep(0.01)#delay
    
oled.fill(0)
oled.show()
start=1
global score
score=0
while start==1:
    global gamerReaction
    global score
    changeWord()
    startTime=utime.ticks_ms()
    
    #When LDR's data greater than 2000 ,gamer reaction '0'
    while utime.ticks_diff(utime.ticks_ms(), startTime)<=2000:
        if ldr.read_u16()>20000:
            gamerReaction=0
    #When LDR's data lower than 2000 ,gamer reaction '1'
        else:
            gamerReaction=1
        sleep(0.01)#delay
    
    #buzzer working
    buzzer.duty_u16(2000)
    sleep(0.05)
    buzzer.duty_u16(0)
    if gamerReaction==nightorday:
        score += 10
     #When Score is 10 ,OLED says 'Game Over'

    else:
        oled.fill(0)
        oled.show()
        oled.text("Game Over", 0, 18, 1)
        oled.text("Your score " + str(score), 0,35)
        oled.text("Press RESET",0, 45)
        oled.text("To REPEAT",0,55)
        oled.show()
        #buzzer working
        buzzer.duty_u16(2000)
        sleep(0.05)
        buzzer.duty_u16(0)
        break;
    if score==100:
    #When Score is 10 ,OLED says 'You won'

        oled.fill(0)
        oled.show()
        oled.text("Congratulations", 10, 10)
        oled.text("Top Score: 100", 5, 35)
        oled.text("Press Reset", 20, 45)
        oled.text("To REPEAT", 25,55)
        oled.show()
        
        #buzzer working
        buzzer.duty_u16(2000)
        sleep(0.1)
        buzzer.duty_u16(0)
        sleep(0.1)
        buzzer.duty_u16(2000)
        sleep(0.1)
        buzzer.duty_u16(0)
        break;