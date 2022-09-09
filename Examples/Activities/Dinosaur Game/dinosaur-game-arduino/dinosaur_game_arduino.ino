#include <Servo.h>
Servo myservo;

void setup() {
  // put your setup code here, to run once:
  myservo.attach(22);
  myservo.write(20);
  pinMode(27,INPUT);

  

}

void loop() {
  // put your main code here, to run repeatedly:
  int light_sensor=analogRead(27);

  if(light_sensor>100){

    int x=45;
    int y=20;
    
    myservo.write(x);
    delay(100);
    myservo.write(y);
    delay(500);
  }


}
