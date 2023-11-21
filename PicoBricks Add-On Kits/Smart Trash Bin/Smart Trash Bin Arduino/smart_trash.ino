#include <Servo.h>
#define trigPin 15
#define echoPin 14

int state = 0;
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
  distance = (duration/2) / 29.1; //cm
  if (distance < 20) {
    state = 1;
    Serial.print(distance);
    Serial.println(" cm");
    for(int i=100; i<179; i++){
      servo.write(i); 
      delay(25);
    }
    delay(2000);
  }
  else{
    Serial.print(distance);
    Serial.println(" cm");
    if(state == 1){
      state = 0;
      for(int i=179; i>100; i=i-5){
        servo.write(i); 
        delay(50);
      }
    }
  }
}
