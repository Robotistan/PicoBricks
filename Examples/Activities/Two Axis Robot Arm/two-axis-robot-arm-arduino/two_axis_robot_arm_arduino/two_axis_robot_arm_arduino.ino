#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN        6 
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500

#include <Servo.h>
Servo myservo1;
Servo myservo2;

int angleupdown;

void setup() {

  pinMode(20,OUTPUT);
  pinMode(27,INPUT);
  
  pixels.begin();
  pixels.clear(); 

  myservo1.attach(21);
  myservo2.attach(22);
  Open();
  angleupdown=180;
  myservo2.write(angleupdown);

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
    myservo2.write(angleupdown);
  }
}

void Open(){
  myservo1.write(180);
}

void Close(){
  myservo1.write(30);
}

void Up(){
 
  for (int i=0;i<45;i++){
    
    angleupdown = angleupdown+2;
    myservo2.write(angleupdown);
    delay(30);
    }
}

void Down(){
 
  for (int i=0;i<45;i++){
    
    angleupdown = angleupdown-2;
    myservo2.write(angleupdown);
    delay(30);
    }
}
