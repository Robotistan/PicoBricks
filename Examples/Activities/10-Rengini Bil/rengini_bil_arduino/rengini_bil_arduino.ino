#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN        6 
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500
#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"
int OLED_color;
int RGB_color;
int score = 0;
int x = 0;
int button;


void setup() {
  // put your setup code here, to run once:
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin();
  pixels.clear(); 

}

void loop() {
  // put your main code here, to run repeatedly:
  oled.clearDisplay();
  oled.setTextXY(3,1);              
  oled.putString("The game begins");
  pixels.setPixelColor(0, pixels.Color(0, 0, 0));
  pixels.show();
  delay(2000);
  oled.clearDisplay();
  
  for (int i=0;i<10;i++){
    
    random_color();
    pixels.show();
    
    button = digitalRead(10);
    if (button == 1){

      if(OLED_color==RGB_color & x==0){
        score=score+10;
        x=1;
      }
      if(OLED_color!=RGB_color & x==0){
        score=score-10;
        x=1;
      }
    }
    delay(2000);
    oled.clearDisplay();
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
    x=0;
  }

  String string_scrore=String(score);
  oled.clearDisplay();
  oled.setTextXY(2,5);              
  oled.putString("Score: ");
  oled.setTextXY(4,7);              
  oled.putString(string_scrore);
  oled.setTextXY(6,5);              
  oled.putString("points");

  delay(10000);
}

void random_color(){

  OLED_color = random(1,5);
  RGB_color = random(1,5);

    if (OLED_color == 1){
      oled.setTextXY(3,7);              
      oled.putString("red");
  }
    if (OLED_color == 2){
      oled.setTextXY(3,6);              
      oled.putString("green");
  }
    if (OLED_color == 3){
      oled.setTextXY(3,6);              
      oled.putString("blue");
  }
    if (OLED_color == 4){
      oled.setTextXY(3,6);              
      oled.putString("white");
  } 
    if (RGB_color == 1){
      pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  }
    if (RGB_color == 2){
      pixels.setPixelColor(0, pixels.Color(0, 255, 0));
  }
    if (RGB_color == 3){
      pixels.setPixelColor(0, pixels.Color(0, 0, 255));
  }
    if (RGB_color == 4){
      pixels.setPixelColor(0, pixels.Color(255, 255, 255));
  }


}
