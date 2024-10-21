#include <Wire.h>

#define trigPin 15
#define echoPin 14

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
  //calculate distance
  if (distance < 5) {    //if the distance variable is less than 5
    Serial.print(distance);
    Serial.println(" cm");
    servo(1,180);
  }
  else if (distance>5) {   // if the distance variable is greater than 5
    Serial.print(distance);
    Serial.println(" cm");
    servo(1,100);
  }
}
