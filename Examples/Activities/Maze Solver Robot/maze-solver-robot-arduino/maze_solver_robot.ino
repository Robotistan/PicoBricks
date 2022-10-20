#include <NewPing.h>

#define TRIGGER_PIN  15
#define ECHO_PIN     14
#define MAX_DISTANCE 400
//define sensor pins

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  pinMode(21,OUTPUT);
  pinMode(22,OUTPUT); //define dc motor pins
}

void loop() {
  
  delay(50);
  int distance=sonar.ping_cm();
  Forward();

  if(distance<5){

    Stop();
    delay(1000);
    Turn_Right();
    delay(1000);
    int distance=sonar.ping_cm();

    if(distance<5){
      Stop();
      delay(1000);
      Turn_Left();
      delay(500);
      // If the distance is less than 5, wait, turn right; if the distance is less than 5 again, move in the opposite direction
    }
  }
}

void Forward(){
  digitalWrite(21,HIGH);
  digitalWrite(22,HIGH); //if the distance is higher than 5, go straight
}
void Turn_Left(){
  digitalWrite(21,LOW);
  digitalWrite(22,HIGH); //turn left
}
void Turn_Right(){
  digitalWrite(21,HIGH);
  digitalWrite(22,LOW);  //turn right
}
void Stop(){
  digitalWrite(21,LOW);
  digitalWrite(22,LOW); //wait
}
