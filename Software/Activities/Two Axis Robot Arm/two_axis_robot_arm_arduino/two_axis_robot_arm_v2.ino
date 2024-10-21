#include <Adafruit_NeoPixel.h>
#include <Wire.h>

#define PIN        6
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500

int angleupdown;

void servo(int servonumber,int angle){
  Wire.beginTransmission(0x22);
  Wire.write(0x26);   
  Wire.write(servonumber + 2); 
  Wire.write(0x00);   
  Wire.write(angle);   
  int cs = (servonumber + 2) ^ angle;
  Wire.write(cs); 
  Wire.endTransmission();
}

void setup() {
  pinMode(20,OUTPUT);
  pinMode(27,INPUT);

  pixels.begin();
  pixels.clear();

  Open();
  angleupdown=180;
  servo(2,angleupdown);
}

void loop() {
  if(analogRead(27)>150){
    pixels.setPixelColor(0, pixels.Color(255, 0, 0));
    pixels.show();
    delay(1000);
    tone(20,700);
    delay(1000);
    noTone(20);

    Open();
    delay(500);
    Down();
    delay(500);
    Close();
    delay(500);
    Up();
    pixels.setPixelColor(0, pixels.Color(0, 255, 0));
    pixels.show();
    delay(10000);
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.show();
    Open();
    angleupdown=180;
    servo(2,angleupdown);
    // If the LDR data is greater than the specified limit, the buzzer will sound, the RGB will turn red and servo motors will work
    // The RGB will turn green when the movement is complete
  }
}

void Open(){
  servo(1,180);
}

void Close(){
  servo(1,30);
}

void Up(){
  for (int i=0;i<45;i++){
    angleupdown = angleupdown+2;
    servo(2,angleupdown);
    delay(30);
  }
}

void Down(){
  for (int i=0;i<45;i++){
    angleupdown = angleupdown-2;
    servo(2,angleupdown);
    delay(30);
  }
}
