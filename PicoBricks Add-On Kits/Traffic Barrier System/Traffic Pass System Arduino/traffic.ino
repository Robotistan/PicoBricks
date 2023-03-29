#include <Servo.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN        6
#define NUMPIXELS 1

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Servo myservo;

#define ldr 27
#define buzzer 20

int ldr_stt = analogRead(ldr);
int pos = 0;

void setup() {
  Serial.begin(115200);
  myservo.attach(21);
  pinMode(ldr, INPUT);
  pinMode(buzzer, OUTPUT);
  pixels.begin();
  myservo.write(0);
  pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  pixels.show();

}
void loop() {
  ldr_stt = analogRead(ldr);
  Serial.println(pos);

  if (ldr_stt > 220) {

    while (pos < 180) {
      pos = pos + 1;
      myservo.write(pos);
      alarm();
      pixels.setPixelColor(0, pixels.Color(255, 255, 0));
      pixels.show();
    }
    pixels.setPixelColor(0, pixels.Color(0, 255, 0));
    pixels.show();
    delay(2000);
  }
  else {
    while (pos > 0) {
      pos = pos - 1;
      myservo.write(pos);
      alarm();
      pixels.setPixelColor(0, pixels.Color(255, 0, 0));
      pixels.show();
    }
  }
}

void alarm() {
  tone(buzzer,1000);
  delay(5);
  noTone(buzzer);
}
