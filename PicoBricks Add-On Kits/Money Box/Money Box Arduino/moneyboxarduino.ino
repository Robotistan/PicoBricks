#include<Servo.h>
#define trigPin 15
#define echoPin 14

Servo servo ;

float distance,duration;

void setup() { 
  // servo.write(0) set servos angle motion
  // servo.attach(pin) attachs servo

  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
  servo.attach(21); 
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin,LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin,LOW);
  duration=pulseIn(echoPin,HIGH);
  distance=(duration/2)/29.1;
  if(distance<9 ){
    Serial.print(distance);
    Serial.println("mm");
    // servo opened
      
      for(int j=180;j>0;j=j-3)
       {
       servo.write(j);
       delay(0.02);
       }
     
    
  } else {
      
      Serial.print(distance);
      Serial.println("mm");
   
     // servo closed
      for(int i=0;i<180;i=i+3)
      {
      servo.write(i);
      delay(0.02);
      }
    
  }
  delay(1000);
 
}