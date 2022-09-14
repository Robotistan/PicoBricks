#include <NewPing.h>

#define TRIGGER_PIN  15
#define ECHO_PIN     14
#define MAX_DISTANCE 400

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  pinMode(21,OUTPUT);
  pinMode(22,OUTPUT);
}

void loop() {
  
  delay(50);
  int distance=sonar.ping_cm();
  Forward();

  if(distance<5){

    Stop();
    delay(1000);
    Turn_Right();
    delay(500);
    int distance=sonar.ping_cm();

    if(distance<5){

      Stop();
      delay(1000);
      Turn_Left();
      delay(1000);
    }
  }
}

void Forward(){
  digitalWrite(21,HIGH);
  digitalWrite(22,HIGH);
}
void Turn_Left(){
  digitalWrite(21,LOW);
  digitalWrite(22,HIGH);
}
void Turn_Right(){
  digitalWrite(21,HIGH);
  digitalWrite(22,LOW);
}
void Stop(){
  digitalWrite(21,LOW);
  digitalWrite(22,LOW);
}
