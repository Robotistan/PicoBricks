#include <NewPing.h>
#include <Servo.h>
Servo myservo;

#define TRIGGER_PIN  15
#define ECHO_PIN     14
#define MAX_DISTANCE 400

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  myservo.attach(21);
  myservo.write(20);
}

void loop() {
  
  delay(50);
  int distance=sonar.ping_cm();

  if(distance<10){

    int x=100;
    int y=20;
    delay(2000);
    myservo.write(x);
    delay(300);
    myservo.write(y);
  }
}
