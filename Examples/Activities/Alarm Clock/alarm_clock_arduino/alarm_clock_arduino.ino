#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> 
#endif
#define PIN        6 

#define NUMPIXELS 1 
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"
int button;
void setup() {
  // put your setup code here, to run once:
   Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 
  
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  pinMode(10,INPUT);
  pinMode(27,INPUT);
  pinMode(20,OUTPUT);
  
  pixels.begin();
  pixels.setPixelColor(0, pixels.Color(0, 0, 0));
  pixels.show();

}

void loop() {
  // put your main code here, to run repeatedly:
  oled.setTextXY(4,3);              
    oled.putString("Good night");
    
    if (analogRead(27)<200){

      while(!(button == 1)){
        
        button=digitalRead(10);
       
        oled.setTextXY(4,2);              
        oled.putString("Good morning");
        pixels.setPixelColor(0, pixels.Color(255, 255, 255));
        pixels.show();
        tone(20,494);
      }
        oled.clearDisplay();
        oled.setTextXY(4,1);              
        oled.putString("Have a nice day");
        noTone(20);
        pixels.setPixelColor(0, pixels.Color(0, 0, 0));
        pixels.show();
        delay(10000);
    }


}
