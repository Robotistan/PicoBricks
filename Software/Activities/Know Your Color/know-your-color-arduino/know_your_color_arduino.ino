#include <Adafruit_NeoPixel.h>
#define PIN        6 
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500
#include <Wire.h>
#include "ACROBOTIC_SSD1306.h" //define libraries
int OLED_color;
int RGB_color;
int score = 0;
int button = 0;



void setup() {
  // put your setup code here, to run once:
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 


  pixels.begin();
  pixels.clear(); 
  randomSeed(analogRead(27));

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
    button = digitalRead(10);
    random_color();
    pixels.show();
    unsigned long start_time = millis();
    while (button == 0) {
        button = digitalRead(10);
        if (millis() - start_time > 2000)
          break;
    }
    if (button == 1){
  
        if(OLED_color==RGB_color){
          score=score+10;
        }
        if(OLED_color!=RGB_color){
          score=score-10;
        }
        delay(200);
    }
    oled.clearDisplay();
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
  }

  String string_scrore=String(score);
  oled.clearDisplay();
  oled.setTextXY(2,5);              
  oled.putString("Score: ");
  oled.setTextXY(4,7);              
  oled.putString(string_scrore);
  oled.setTextXY(6,5);              
  oled.putString("points");
  // print final score on OLED screen
  
  delay(10000);
}

void random_color(){

  OLED_color = random(1,5);
  RGB_color = random(1,5); 
  // generate numbers between 1 and 5 randomly and print them on the screen
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
