#include <Servo.h>
#define trigPin 14
#define echoPin 15
Servo servo;
void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  servo.attach(21);
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
    servo.write(179);
  }

  else if (distance<180) {
    Serial.print(distance);
    Serial.println(" cm");
    servo.write(100); 
  }
  

}
