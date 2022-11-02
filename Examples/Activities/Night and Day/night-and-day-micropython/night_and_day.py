from machine import Pin, I2C, Timer, ADC, PWM
from picobricks import SSD1306_I2C
import utime
import urandom
#define the libraries
WIDTH = 128
HEIGHT = 64
#OLED Screen Settings
sda=machine.Pin(4)
scl=machine.Pin(5)
#initialize digital pin 4 and 5 as an OUTPUT for OLED Communication
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
buzzer = PWM(Pin(20))
buzzer.freq(440)
ldr=ADC(Pin(27))
button=Pin(10,Pin.IN,Pin.PULL_DOWN)
#define the input and output pins
oled.text("NIGHT and DAY", 10, 0)
oled.text("<GAME>", 40, 20)
oled.text("Press the Button", 0, 40)
oled.text("to START!", 40, 55)
oled.show()
#OLED Screen Texts Settings
def changeWord():
    global nightorday
    oled.fill(0)
    oled.show()
    nightorday=round(urandom.uniform(0,1))
    #when data is '0', OLED texts NIGHT
    if nightorday==0:
        oled.text("---NIGHT---", 20, 30)
        oled.show()
    else:
        oled.text("---DAY---", 20, 30)
        oled.show()
    #waits for the button to be pressed to activate
        
while button.value()==0:
    print("Press the Button")
    sleep(0.01)
    
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
    #when LDR's data greater than 2000, gamer reaction '0'
    while utime.ticks_diff(utime.ticks_ms(), startTime)<=2000:
        if ldr.read_u16()>20000:
            gamerReaction=0
        #when LDR's data lower than 2000, gamer reaction '1'
        else:
            gamerReaction=1
        sleep(0.01)
    #buzzer working
    buzzer.duty_u16(2000)
    sleep(0.05)
    buzzer.duty_u16(0)
    if gamerReaction==nightorday:
        score += 10
    #when score is 10, OLED says 'Game Over'
    else:
        oled.fill(0)
        oled.show()
        oled.text("Game Over", 0, 18, 1)
        oled.text("Your score " + str(score), 0,35)
        oled.text("Press RESET",0, 45)
        oled.text("To REPEAT",0,55)
        oled.show()
        buzzer.duty_u16(2000)
        sleep(0.05)
        buzzer.duty_u16(0)
        break;
    if score==100:
        #when score is 10, OLED says 'You Won'
        oled.fill(0)
        oled.show()
        oled.text("Congratulation", 10, 10)
        oled.text("Top Score: 100", 5, 35)
        oled.text("Press Reset", 20, 45)
        oled.text("To REPEAT", 25,55)
        oled.show()
        buzzer.duty_u16(2000)
        sleep(0.1)
        buzzer.duty_u16(0)
        sleep(0.1)
        buzzer.duty_u16(2000)
        sleep(0.1)
        buzzer.duty_u16(0)
        break;
