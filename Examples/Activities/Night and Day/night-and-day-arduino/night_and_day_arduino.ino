#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"
//define the library


#define RANDOM_SEED_PIN     28
int Gamer_Reaction=0;
int Night_or_Day=0;
int Score=0;
int counter=0;

double currentTime=0;
double lastTime=0;
double getLastTime(){
  return currentTime=millis()/1000.0-lastTime;
}

void _delay(float seconds){
  long endTime=millis()+seconds*1000;
  while (millis()<endTime) _loop();
}

void _loop(){
}

void loop(){
  _loop();
}
//define variable

void setup() {
  // put your setup code here, to run once:
  pinMode(10,INPUT);
  pinMode(27, INPUT);
  pinMode(20,OUTPUT);
  randomSeed(RANDOM_SEED_PIN);
  Wire.begin();
  oled.init();
  oled.clearDisplay();
  //define the input and output pins

  oled.clearDisplay();
  oled.setTextXY(1,3);
  oled.putString("NIGHT and DAY");
  oled.setTextXY(2,7);
  oled.putString("GAME");
  oled.setTextXY(5,2);
  oled.putString("Press the BUTTON");
  oled.setTextXY(6,4);
  oled.putString("to START!");
  //write "NIGHT an DAY, GAME, Press the BUTTON, to START" on the x and y coordinates determined on the OLED screen

  Score=0;
  //define the score variable

  while(!(digitalRead(10)==1))  //until the button is pressed
  {
    _loop();
  }
  _delay(0.2);

  while(1){  //while loop
    if(counter==0){
      delay(500);
      Change_Word();
      lastTime=millis()/1000.0;
    }
    while(!(getLastTime()>2)){
      Serial.println(analogRead(27));
      if(analogRead(27)>200){
        Gamer_Reaction=0;

      }
      else{
        Gamer_Reaction=1;
      }
    }
   //determine the gamer reaction based on the value of the LDR sensor
   digitalWrite(20,HIGH);   //turn on the buzzer
   delay(250);  //wait
   digitalWrite(20,LOW);  //turn off the buzzer

   if(Night_or_Day==Gamer_Reaction){  //if the user's reaction and the Night_or_Day variable are the same
    Correct();
   
   }
   else{
    Wrong();
   }
   _loop();

   if(Score==100){
      oled.clearDisplay();
      oled.setTextXY(1,1);
      oled.putString("Congratulation");
      oled.setTextXY(3,1);
      oled.putString("Your Score");
      oled.setTextXY(3,13);
      String String_Score=String(Score);
      oled.putString(String_Score);
      oled.setTextXY(5,3);
      oled.putString("Press Reset");
      oled.setTextXY(6,3);
      oled.putString("To Repeat!");
      //write the "Congratulation, Your Score, press Reset, To Repeat!" and score variable on the x and y coordinates determined on the OLED screen
      for(int i=0;i<3;i++){
        digitalWrite(20,HIGH);
        delay(500);
        digitalWrite(20,LOW);
        delay(500);
     
    }
    //turn the buzzer on and off three times
    counter=1;

   }
  }
}

void Correct(){
  Score+=10;
  oled.clearDisplay();
  oled.setTextXY(3,4);
  oled.putString("10 Points");
  //increase the score by 10 when the gamer answers correctly
}

void Change_Word(){
  
  oled.clearDisplay();
  Night_or_Day=random(0,2);
  if(Night_or_Day==0){
    oled.setTextXY(3,6);
    oled.putString("NIGHT");

  }
  else{
    oled.setTextXY(3,7);
    oled.putString("DAY");
  }
 
}
//write "NIGHT" or "DAY" on random OLED screen

void Wrong(){
  oled.clearDisplay();
  oled.setTextXY(1,3);
  oled.putString("Game Over");
  oled.setTextXY(3,1);
  oled.putString("Your Score");
  oled.setTextXY(1,13);
  String String_Score=String(Score);
  oled.putString(String_Score);
  oled.setTextXY(5,3);
  oled.putString("Pres Reset");
  oled.setTextXY(6,3);
  oled.putString("To Repeat");
  // write the score variable and the expressions is quotation marks to the coordinates determined on the OLED screen.

  digitalWrite(20,HIGH);  //turn on the buzzer
  delay(1000);   //wait
  digitalWrite(20,LOW); //turn off the buzzer
  counter=1;
}
