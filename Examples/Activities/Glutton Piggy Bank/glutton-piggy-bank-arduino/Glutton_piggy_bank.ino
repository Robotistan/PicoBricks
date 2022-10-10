#include <Servo.h>
#define trigPin 15
#define echoPin 14
//define the libraries
Servo servo;
void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  //define the input and output pins
  servo.attach(21); //define the servo pin
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
    servo.write(179);
  }
  else if (distance>5) {   // if the distance variable is greater than 5
    Serial.print(distance);
    Serial.println(" cm");
    servo.write(100);
  }
}
