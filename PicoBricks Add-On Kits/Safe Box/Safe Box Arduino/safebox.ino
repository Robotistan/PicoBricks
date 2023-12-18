#include <Wire.h>
#include "ACROBOTIC_SSD1306.h" // v1.0.0
#include <Servo.h>

#define pot 26
#define led 7
#define ldr 27
#define button1 10


char correct_password[] = {1, 1, 1, 1};
char password[] = {0, 0, 0, 0};
int oldDigit = 0;
int lock_state = 0;// 0 is locked, 1 is unlocked    count=int((pot.read_u16()*10)/65536)
int buttonReleased = 1;
int passIndex = 0;
int digit = (analogRead(pot) * 9 / 1023);
Servo servo;

int LIGHT_THRESHOLD = 500 ;
int OPEN_POSITION = 150 ;
int CLOSED_POSITION = 0 ;

int digitCounter = 1;

void lockTheSafe() {
  oled.clearDisplay();
  oled.setTextXY(2, 2);
  oled.putString("Locking...");
  delay(300);
  servo.write(CLOSED_POSITION);
  oldDigit = 0;
  oled.clearDisplay();
}

void unlockTheSafe() {
  oled.clearDisplay();
  oled.setTextXY(2, 2);
  oled.putString("Opening...");
  delay(300);
  servo.write(OPEN_POSITION);
  delay(5000);
  oled.clearDisplay();
}

bool passwordCheck(char* definedPassword, char* enteredPassword) {
  for (int i = 0; i < 4 ; i++) {
    if (definedPassword[i] != enteredPassword[i])
      return false ;
  }
  return true ;
}


void setup() {
  servo.attach(21);
  Serial.begin(115200);
  servo.write(CLOSED_POSITION);
  Wire.begin();
  oled.init();
  oled.clearDisplay();
  pinMode(pot, INPUT);
  pinMode(ldr, INPUT);
  pinMode(button1, INPUT);
  pinMode(led, OUTPUT);
  oled.setTextXY(0, 4);
  oled.putString("Safe Box");
}

void loop() {
  if (lock_state) {
    if (analogRead(ldr) > LIGHT_THRESHOLD) {
      lockTheSafe();
      lock_state = 0;
      delay(2000);
    }
  }
  else {
    int digit = (analogRead(pot) * 9 / 1023);
    if (digit != oldDigit) {
      oldDigit = digit;
      oled.setTextXY(2, 4);
      oled.putString("Password");
      oled.setTextXY(4, 7);
      oled.putString(String(digit));

    }
    if (digitalRead(button1) == 0 and buttonReleased == 0) {
      Serial.println("Button RELEASED.");
      buttonReleased = 1;
      digitalWrite(led, LOW);
    }
    if (digitalRead(button1) == 1 and buttonReleased == 1) {
      Serial.println("Button PRESSED.");
      buttonReleased = 0;
      digitalWrite(led, HIGH);
      delay(300);
      password[passIndex] = digit;
      digitCounter += 1;
      oldDigit = 0;
      if (passIndex >= 3) {
        passIndex = 0;
        digitCounter = 1;
        if (passwordCheck(&correct_password[0], &password[0])) {
          unlockTheSafe();
          lock_state = 1;
        }
        else {
          oled.clearDisplay();
          oled.setTextXY(2, 2);
          oled.putString("Try Again");
          delay(1500);
          oled.clearDisplay();
        }
      }
      else {
        passIndex += 1;
      }
    }
  }
}
