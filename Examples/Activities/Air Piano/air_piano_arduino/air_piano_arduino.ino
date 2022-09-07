#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"
#include <NewPing.h>

#define TRIGGER_PIN  15
#define ECHO_PIN     14
#define MAX_DISTANCE 400

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

#define T_C 262
#define T_D 294
#define T_E 330
#define T_F 349
#define T_G 392
#define T_A 440
#define T_B 493

const int Buzzer = 20;

void setup() {
  pinMode(Buzzer,OUTPUT);

  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
}

void loop() {

  delay(50);
  int distance=sonar.ping_cm();

  if(distance>5 & distance<11)
  {
    tone(Buzzer,T_C);
  }

  else if(distance>10 & distance<16)
  {
    tone(Buzzer,T_D);
  }

  else if(distance>15 & distance<21)
  {
    tone(Buzzer,T_E);
  }

  else if(distance>20 & distance<26)
  {
    tone(Buzzer,T_F);
  }

  else if(distance>25 & distance<31)
  {
    tone(Buzzer,T_G);
  }

  else if(distance>30 & distance<36)
  {
    tone(Buzzer,T_A);
  }

  else if(distance>35 & distance<41)
  {
    tone(Buzzer,T_B);
  }

  else 
  {
    noTone(Buzzer);
  }

  oled.clearDisplay();
  oled.setTextXY(2,4);              
  oled.putString("Distance: ");
  oled.setTextXY(4,6);              
  String string_distance=String(distance);
  oled.putString(string_distance);
  oled.setTextXY(4,8);              
  oled.putString("cm");
}
