#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"

int Gamer_Reaction = 0;
int Night_or_Day = 0;
int Score = 0;
int Sayac=0;

double currentTime = 0;
double lastTime = 0;
double getLastTime(){
      return currentTime = millis()/1000.0 - lastTime;
}

void _delay(float seconds) {
  long endTime = millis() + seconds * 1000;
  while(millis() < endTime) _loop();
}

void _loop() {
}

void loop() {
  _loop();
}

void setup() {

  pinMode(10,INPUT);
  pinMode(27,INPUT);
  pinMode(20,OUTPUT);

  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  oled.clearDisplay();
  oled.setTextXY(1,3);              
  oled.putString("NIGHT and DAY");
  oled.setTextXY(2,7);              
  oled.putString("GAME");
  oled.setTextXY(5,2);              
  oled.putString("Press BUTTON!");
  oled.setTextXY(6,4);              
  oled.putString("to START!");
  
  Score = 0;

  while(!(digitalRead(10) == 1))
  {
    _loop();
  }
  _delay(0.2); 
  
  while(1){ 
  if (Sayac==0){
    
  delay(500);
  Change_Word();
  lastTime = millis()/1000.0;
  
  while(!(getLastTime() > 2))
  {
    _loop();
    if(analogRead(27) > 500){
        Gamer_Reaction = 0;
    }else{
        Gamer_Reaction = 1;
    }
  }
  digitalWrite(20,HIGH);
  delay(250);
  digitalWrite(20,LOW);
  
  if(Night_or_Day == Gamer_Reaction){
      Correct();

  }else{
      Wrong();

  } _loop();

  if(Score==100){
  oled.clearDisplay();
  oled.setTextXY(1,1);              
  oled.putString("Congratulation");
  oled.setTextXY(3,1);              
  oled.putString("Your Score: ");  
  oled.setTextXY(3,13);              
  String String_Score=String(Score);
  oled.putString(String_Score);
  oled.setTextXY(5,3);              
  oled.putString("Press Reset"); 
  oled.setTextXY(6,3);              
  oled.putString("To Repeat!");   
  
    for(int i=0;i<3;i++){

    digitalWrite(20,HIGH);
    delay(500);
    digitalWrite(20,LOW);
    delay(500); 
    } Sayac=1;
   }
  }
 }
}

void Correct (){
  Score += 10;
  oled.clearDisplay();
  oled.setTextXY(3,4);              
  oled.putString("10 points");  
}

void Change_Word (){
  oled.clearDisplay();
  Night_or_Day=random(0,2);

  if (Night_or_Day==0){
    oled.setTextXY(3,6);              
    oled.putString("NIGHT");
  }else{
    oled.setTextXY(3,7);              
    oled.putString("DAY");
  }
}

void Wrong (){
  oled.clearDisplay();
  oled.setTextXY(1,3);              
  oled.putString("Game Over");
  oled.setTextXY(3,1);              
  oled.putString("Your Score: ");  
  oled.setTextXY(3,13);              
  String String_Score=String(Score);
  oled.putString(String_Score);
  oled.setTextXY(5,3);              
  oled.putString("Press Reset"); 
  oled.setTextXY(6,3);              
  oled.putString("To Repeat!");   
  digitalWrite(20,HIGH);
  delay(1000);
  digitalWrite(20,LOW);
  Sayac=1; 
}
