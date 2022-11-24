#include <Adafruit_NeoPixel.h>
#define PIN            6
#define NUMLEDS        1
#define LIGHT_SENSOR_PIN 27

Adafruit_NeoPixel leds = Adafruit_NeoPixel(NUMLEDS, PIN, NEO_GRB + NEO_KHZ800);
//define the libraries

int delayval = 250; // delay for half a second

void setup() 
{
  leds.begin(); 
}

void loop() 
{
  int analogValue = analogRead(LIGHT_SENSOR_PIN);
  for(int i=0;i < NUMLEDS;i++)
  {
      if (analogValue > 200) {
          // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
          leds.setPixelColor(i, leds.Color(255,255,255));
          leds.show(); // This sends the updated pixel color to the hardware.
          delay(delayval); 
      }
       else {
         leds.setPixelColor(i, leds.Color(0,0,0));  //white color code.
         leds.show(); // This sends the updated pixel color to the hardware.
      }
    }
    delay(10);
}
