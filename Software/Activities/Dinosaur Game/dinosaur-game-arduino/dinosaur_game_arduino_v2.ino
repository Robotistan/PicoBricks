#include <Wire.h>

void servo(int servonumber,int angle){
  Wire.beginTransmission(0x22);
  Wire.write(0x26);   
  Wire.write(servonumber + 2); 
  Wire.write(0x00);   
  Wire.write(angle);   
  int cs = (servonumber + 2) ^ angle;
  Wire.write(cs); 
  Wire.endTransmission();
}

void setup() {
  pinMode(27,INPUT);
  servo(1,0);
}

void loop() {
  int light_sensor=analogRead(27);

  if(light_sensor>100){
    servo(1,180);
    delay(100);
    servo(1,0);
    delay(500);
  }
}
