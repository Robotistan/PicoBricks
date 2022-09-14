#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"

int buzzer = 20;
int button = 10;
int led = 7;
int La = 440;

int old_time = 0;
int now_time = 0;
int score = 0;
String string_score ;

void setup() {
  // put your setup code here, to run once:
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay();              

  pinMode(led,OUTPUT);
  pinMode(buzzer,OUTPUT);
  pinMode(button,INPUT);
Serial.begin(9600);


}

void loop() {
  // put your main code here, to run repeatedly:
  oled.setTextXY(3,0);              
  oled.putString("Press the button");
  oled.setTextXY(5,4);              
  oled.putString("TO START");
  
  if (digitalRead(button) == 1){

    for (int i=3;i>0;i--){

      String string_i = String(i);
      oled.clearDisplay(); 
      oled.setTextXY(4,8);  
      oled.putString(string_i);
      delay(1000);
      
    }
      
    oled.clearDisplay();
    oled.setTextXY(4,6);
    oled.putString("GO!!!");

    int random_wait = random(1000, 5000);
    delay(random_wait);

    digitalWrite(led, HIGH);
    old_time=millis();

    while(!(digitalRead(button) == 1)){

      now_time=millis();
      
      score = now_time-old_time;
      string_score = String(score);

    }
      digitalWrite(led, HIGH);
      tone(buzzer, La); 
      delay (200);
      noTone(buzzer);

      oled.clearDisplay();
      oled.setTextXY(1,4);
      oled.putString("Press the");
      oled.setTextXY(2,3);
      oled.putString("RESET BUTON");
      oled.setTextXY(3,3);
      oled.putString("to Repeat!");

      oled.setTextXY(6,3);
      oled.putString("Score: ");
      oled.setTextXY(6,9);
      oled.putString(string_score);
      oled.setTextXY(6,13);
      oled.putString(" ms");
      Serial.println(score);
      delay(10000);
      oled.clearDisplay();
  }


}
