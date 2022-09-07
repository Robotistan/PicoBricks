#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"

int Time=0;
unsigned long Old_Time=0;

void setup() {
  // put your setup code here, to run once:
  pinMode(20,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(1,OUTPUT);
  pinMode(10,INPUT);

  Wire.begin();  
  oled.init();                      
  oled.clearDisplay();
   
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif  


}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(7,LOW);

  oled.setTextXY(2,1);              
  oled.putString("BUZZ WIRE GAME"); 
  oled.setTextXY(4,2);              
  oled.putString("Press Button"); 
  oled.setTextXY(5,3);              
  oled.putString("TO START!");

  while (!(digitalRead(10)==1)){
    
  }

  oled.clearDisplay();
  oled.setTextXY(3,6);              
  oled.putString("GAME"); 
  oled.setTextXY(5,4);              
  oled.putString("STARTED");

  digitalWrite(1,HIGH);
  Old_Time=millis();
  
  while(!(digitalRead(1)==0)){

    Time=millis()-Old_Time;   
  }

  String(String_Time)=String(Time);
  
  oled.clearDisplay();
  oled.setTextXY(3,4);              
  oled.putString("GAME OVER"); 
  oled.setTextXY(5,4);              
  oled.putString(String_Time);
  oled.setTextXY(5,10);              
  oled.putString("ms"); 

  digitalWrite(7,HIGH);
  digitalWrite(20,HIGH);
  delay(500);
  digitalWrite(20,LOW);
  delay(5000);
  
  Time=0;
  Old_Time=0;
  oled.clearDisplay();


}
