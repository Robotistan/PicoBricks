#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"

int buzzer = 20;
int pot =26;
int button= 10;
//define the buzzer, pot and button 

int Re = 294;
int Mi = 330;
int Fa = 349;
int La = 440;
//DEFİNE THE TONES
void setup()
{
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay();              

  pinMode(buzzer,OUTPUT);
  pinMode(26,INPUT);
  pinMode(button,INPUT);
//determine our input and output pins
}

void loop()
{
  int rithm = (analogRead(pot))/146;
  String char_rithm = String(rithm);
  oled.setTextXY(3,4);              
  oled.putString("Speed: ");
  oled.setTextXY(3,10);              
  oled.putString(char_rithm);
  
  //print "Speed: "  and speed value on the OLED at x=3 y=4

  delay(10); 

  if (digitalRead(button) == 1){

    oled.clearDisplay(); 
    oled.setTextXY(3,2);              
    oled.putString("Now playing...");
    //print "Speed: "  and speed value on the OLED at x=3 y=4
    tone(buzzer, La); delay (1000/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Fa); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Re); delay (500/(rithm+1));
    tone(buzzer, Fa); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (1000/(rithm+1));
    
    //play the notes in the correct order and time when the button is pressed

    oled.clearDisplay();
    //clear the screen
  }
  noTone(buzzer);
  //stop the buzzer
}
