#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"
//define the library

int buzzer=20;
int button=10;
int led=7;
int La=440;

int old_time=0;
int now_time=0;
int score=0;
String string_score;
//define our integer and string veriables


void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  oled.init();
  oled.clearDisplay();

  pinMode(led,OUTPUT);
  pinMode(buzzer,OUTPUT);
  pinMode(button,INPUT);
  Serial.begin(9600);
  //define the input and output pins

}

void loop() {
  // put your main code here, to run repeatedly:
  oled.setTextXY(3,0);
  oled.putString("Press the button");
  oled.setTextXY(5,4);
  oled.putString("TO START");

  if(digitalRead(button)==1){
    for(int i=3; i>0; i--){

      String string_i=String(i);
      oled.clearDisplay();
      oled.setTextXY(4,8);
      oled.putString(string_i);
      delay(1000);
      
    }
    //count backwards from three

    oled.clearDisplay();
    oled.setTextXY(4,6);
    oled.putString("GO!!!");
    //print "GO!!" on the OLED at x=4 y=6

    int random_wait= random(1000, 5000);
    delay(random_wait);
    //wait for a random second between 1 and 5

    digitalWrite(led, HIGH);
    old_time=millis();
    //turn on LED
    while(!(digitalRead(button)==1)){

      now_time=millis();
      score=now_time-old_time;
      string_score= String(score);
      //save score as string on button press
      
    }
    digitalWrite(led, HIGH);
    tone(buzzer, La);
    delay(200);
    noTone(buzzer);
    //turn on LED and buzzer

    oled.clearDisplay();
    oled.setTextXY(1,4);
    oled.putString("Press the");
    //print "Press the" on the OLED at x=1 Y=4

    oled.setTextXY(2,3);
    oled.putString("RESET BUTTON");
    //print "RESET BUTTON" on the OLED at X=1 Y=4

    oled.setTextXY(3,3);
    oled.putString("To Repeat!");
    //print "To Repeat!" on the OLED at X=3 Y=3

    oled.setTextXY(6,3);
    oled.putString("Score: ");
    oled.setTextXY(6,9);
    oled.putString(string_score);
    oled.setTextXY(6,13);
    oled.putString(" ms");
    Serial.println(score);
    //print score value to screen

    delay(10000);
    oled.clearDisplay();
    //wait ten seconds and clear the screen
  }

}
