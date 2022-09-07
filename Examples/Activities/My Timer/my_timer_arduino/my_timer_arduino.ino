#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"

int minute;
int second = 59;
int milisecond = 9;
int setTimer;

void setup() {
  // put your setup code here, to run once:
  pinMode(10,INPUT);
  pinMode(26,INPUT);

  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 


}

void loop() {
  // put your main code here, to run repeatedly:
  oled.setTextXY(1,2);              
  oled.putString("<<My Timer>>");
  oled.setTextXY(3,1);              
  oled.putString("Please use the");
  oled.setTextXY(4,1);              
  oled.putString("Potantiometer");
  oled.setTextXY(5,0);              
  oled.putString("to set the Timer");
  delay(3000);
  oled.clearDisplay(); 
  
    while(!(digitalRead(10) == 1))
  {
    setTimer = (analogRead(26)*60)/1023;
    oled.setTextXY(3,1);              
    oled.putString("set to:");
    oled.setTextXY(3,8);              
    oled.putString(String(setTimer));
    oled.setTextXY(3,11);              
    oled.putString("min.");
  }
    oled.clearDisplay(); 
    oled.setTextXY(1,1);              
    oled.putString("The Countdown");
    oled.setTextXY(2,3);              
    oled.putString("has begin!");
    
    while(!(digitalRead(10) == 1))
  {
    milisecond = 9- (millis()%100)/10;
    second = 59-(millis()%60000)/1000;
    minute = (setTimer-1)-((millis()%360000)/60000);
    
    oled.setTextXY(5,3);              
    oled.putString(String(minute));
    oled.setTextXY(5,8);              
    oled.putString(String(second));
    oled.setTextXY(5,13);              
    oled.putString(String(milisecond));
    oled.setTextXY(5,6);              
    oled.putString(":");
    oled.setTextXY(5,11);              
    oled.putString(":");
  }
    oled.setTextXY(5,3);              
    oled.putString(String(minute));
    oled.setTextXY(5,8);              
    oled.putString(String(second));
    oled.setTextXY(5,13);              
    oled.putString(String(milisecond));
    oled.setTextXY(5,6);              
    oled.putString(":");
    oled.setTextXY(5,11);              
    oled.putString(":");
    delay(10000);

    if (minute==0 & second==0 & milisecond==0){

    oled.setTextXY(5,3);              
    oled.putString(String(minute));
    oled.setTextXY(5,8);              
    oled.putString(String(second));
    oled.setTextXY(5,13);              
    oled.putString(String(milisecond));
    oled.setTextXY(5,6);              
    oled.putString(":");
    oled.setTextXY(5,11);              
    oled.putString(":");  
    oled.putString("-finished-");
    oled.setTextXY(7,5); 
    delay(10000);
    }


}
