#include <Wire.h>

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

void setup() {
  Serial1.begin(9600);
}

void loop() {
  if (Serial1.available() > 0) {
      char sread = Serial1.read();
      Serial.println(sread);
      
    if (sread == 'f') {
      Forward();
    } else if(sread == 'r'){
      Right();
    } else if(sread == 'l'){
      Left();
    } else if(sread == 's'){
      Stop();
    }
  }
}

void Forward(){
  dc(1,255,1);
  dc(2,255,1);
  delay(1000);
  dc(1,0,1);
  dc(2,0,1);
}

void Left(){
  dc(1,0,1);
  dc(2,255,1);
  delay(500);
  dc(1,0,1);
  dc(2,0,1);
}

void Right(){
  dc(1,255,1);
  dc(2,0,1);
  delay(500);
  dc(1,0,1);
  dc(2,0,1);
}

void Stop(){
  dc(1,0,1);
  dc(2,0,1);
  delay(1000);
}
