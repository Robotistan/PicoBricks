from machine import Pin, I2C, ADC, Timer, PWM #to acces the hardware picobricks
from picobricks import SSD1306_I2C #oled library
import utime #time library

WIDTH  = 128
HEIGHT = 64
#define the width and height values

LIGHT_THRESHOLD = 55000
OPEN_POSITION = 1920
CLOSED_POSITION = 5500
servo =PWM(Pin(21,Pin.OUT))
servo.freq(50)
servo.duty_u16(CLOSED_POSITION)

button = Pin(10, Pin.IN)

ldr = ADC(Pin(27))

led = Pin(7,Pin.OUT)

sda=machine.Pin(4)
scl=machine.Pin(5)
#we define sda and scl pins for inter-path communication
i2c=machine.I2C(0,sda=sda, scl=scl)

oled = SSD1306_I2C(128, 64, i2c)
pot = ADC(Pin(26))

# Define the correct password
correct_password = [1, 2, 3, 4]

# Define a list to store the password
password = [0,0,0,0]
oled.text("Safe Box",30,12)
oled.text("Press the button:",0,45)
oled.show()
utime.sleep(0.1)
oled.fill(0)

digit = int((pot.read_u16()*10)/65536)
oldDigit = 0

lock_state = 0   # 0 is locked, 1 is unlocked    count=int((pot.read_u16()*10)/65536)

buttonReleased = 1
passIndex = 0

def lockTheSafe():
    oled.fill(0)
    oled.text("Locking...",30,12)
    oled.show()
    utime.sleep(0.3)
    servo.duty_u16(CLOSED_POSITION)
    oled.fill(0)
    oldDigit = 0
    
def unlockTheSafe():
    oled.fill(0)
    oled.text("Opening...",30,20)
    oled.show()
    utime.sleep(0.3)
    servo.duty_u16(OPEN_POSITION)
    utime.sleep(5)

def passwordCheck(definedPassword, enteredPassword):
    for i in range(len(definedPassword)):
        if definedPassword[i] != enteredPassword[i]:
            return False
    return True

digitCounter = 1

while True:
    if lock_state:
        if ldr.read_u16() > LIGHT_THRESHOLD:
            lockTheSafe()
            lock_state = 0
            utime.sleep(2)
    else:
        digit = int((pot.read_u16()*10)/65536)
        
        if digit != oldDigit:
            oldDigit = digit
            oled.fill(0)
            oled.text("Password",30,10)
            oled.hline(25, 40, 9, 0xffff)
            oled.hline(50, 40, 9, 0xffff)
            oled.hline(75, 40, 9, 0xffff)
            oled.hline(100, 40, 9, 0xffff)
            for c in range (digitCounter-1):
                oled.text(str(password[c]),25*(c+1),30)
            
            oled.text(str(digit),25*digitCounter,30)
            
            oled.show()
            
            print(ldr.read_u16())
        if button.value() == 0 and buttonReleased == 0:		# button released  (for latch detection)
            print("button RELEASED")
            buttonReleased = 1
            led.value(0)
        if button.value() == 1 and buttonReleased == 1:		# button pressed (for latch detection)
            print("button preseed")
            buttonReleased = 0
            led.value(1)
            utime.sleep(0.3)
            password[passIndex] = digit
            digitCounter += 1
            oldDigit = 0
            if passIndex >= 3:
                passIndex = 0
                digitCounter = 1
                if (passwordCheck(correct_password, password)):
                    unlockTheSafe()
                    lock_state = 1
                else:
                    oled.fill(0)
                    oled.text("Try Again",30,20)
                    oled.show()
                    utime.sleep(1.5)
            else:
                passIndex += 1        
