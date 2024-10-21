#include <Wire.h>

#define trigPin  15
#define echoPin     14
#define MAX_DISTANCE 400

long distance = 0;
long duration = 0;

int hcsr(){
  long dis, dur;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  dur = pulseIn(echoPin, HIGH);
  dis = (dur/2) / 29.1;
  return dis;
}

void setup() {

}

void loop() {
  delay(50);
  distance = hcsr();
  Forward();
  if(distance<5){
    Stop();
    delay(1000);
    Right();
    delay(1000);
    distance = hcsr();
    if(distance < 5){
      Stop();
      delay(1000);
      Left();
      delay(500);
      // If the distance is less than 5, wait, turn right; if the distance is less than 5 again, move in the opposite direction
    }
  }
}

void dc(int dcNumber, int speed, int direction){
  Wire.beginTransmission(0x22);
  Wire.write(0x26);   
  Wire.write(dcNumber); 
  Wire.write(speed);   
  Wire.write(direction);   
  int cs = dcNumber ^ speed ^ direction;
  Wire.write(cs); 
  Wire.endTransmission();
}

void Forward(){   //if the distance is higher than 5, go straight
  dc(1,255,1);
  dc(2,255,1);
}

void Left(){   //turn left
  dc(1,0,1);
  dc(2,255,1);
}

void Right(){   //turn right
  dc(1,255,1);
  dc(2,0,1);
}

void Stop(){
  dc(1,0,1);
  dc(2,0,1);
}
