#include <Wire.h>

#define trigPin 14
#define echoPin 15

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
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  servo(1,110);
}

void loop() {
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1; 
  if (distance < 80) {
    Serial.print(distance);
    Serial.println(" cm");
    servo(1,179);
  }
  else if (distance<180) {
    Serial.print(distance);
    Serial.println(" cm");
    servo(1,110);
  }
}
