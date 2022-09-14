#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"
#include <NewPing.h>  // new png gerek yok

#define TRIGGER_PIN  15
#define ECHO_PIN     14
#define MAX_DISTANCE 400

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // new png gerek yok

#define T_B 493

int distance = 0;
int total = 0;

void setup() {
  pinMode(7,OUTPUT);
  pinMode(20,OUTPUT);
  pinMode(10,INPUT);
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
}

void loop() {

  delay(50);
  if(digitalRead(10) == 1){

    int measure=0;
    digitalWrite(7,HIGH);
    tone(20,T_B);
    delay(500);
    noTone(20);

    for (int i=0;i<20;i++){

      measure=sonar.ping_cm(); // new png gerek yok
      total=total+measure;
      delay(50);      
    }

    distance = total/20+6;
    digitalWrite(7,LOW);

    delay(1000);
    oled.clearDisplay();
    oled.setTextXY(2,1);              
    oled.putString(">Dijital Rule<");
    oled.setTextXY(5,1);              
    oled.putString("Distance: ");
    oled.setTextXY(5,10);              
    String string_distance=String(distance);
    oled.putString(string_distance);
    oled.setTextXY(5,12);              
    oled.putString("cm");

    measure=0;
    distance=0;
    total=0;
  }
}
