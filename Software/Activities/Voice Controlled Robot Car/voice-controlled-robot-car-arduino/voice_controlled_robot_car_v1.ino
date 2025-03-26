#include <Arduino.h>

// Define control pins for the motors
#define MOTOR1 21
#define MOTOR2 22

// Setup motor pins as outputs
void setup() {
  pinMode(MOTOR1, OUTPUT);
  pinMode(MOTOR2, OUTPUT);
  Serial1.begin(9600);
}

// Implement primitive move sequences
void Forward() {
  digitalWrite(MOTOR1,HIGH);
  digitalWrite(MOTOR1,HIGH);
  delay(1000);
  digitalWrite(MOTOR1,LOW);
  digitalWrite(MOTOR2,LOW);
}

void Left() {
  digitalWrite(MOTOR1,LOW);
  digitalWrite(MOTOR2,HIGH);
  delay(500);
  digitalWrite(MOTOR1,LOW);
  digitalWrite(MOTOR2,LOW);
}

void Right() {
  digitalWrite(MOTOR1,HIGH);
  digitalWrite(MOTOR2,LOW);
  delay(500);
  digitalWrite(MOTOR1,LOW);
  digitalWrite(MOTOR2,LOW);
}

void Stop() {
  digitalWrite(MOTOR1,LOW);
  digitalWrite(MOTOR2,LOW);
  delay(1000);
}

// Read commands from the serial 
void loop() {
  if (Serial1.available() > 0) {
 
      char command = Serial1.read();
      Serial.println(command);
      
    if (command == 'f') {
      Forward();
    } else if(command == 'r') {
      Right();
    } else if(command == 'l') {
      Left();
    } else if(command == 's') {
      Stop();
    }
  }
}
