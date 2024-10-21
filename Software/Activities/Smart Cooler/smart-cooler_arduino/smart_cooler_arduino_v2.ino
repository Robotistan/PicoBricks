#include <Wire.h>

#define LIMIT_TEMPERATURE     27

float temp;

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

void shtc_init(){
  Wire.beginTransmission(0x70);
  Wire.write(0x35);   
  Wire.write(0x17); 
  Wire.endTransmission();
  delay(500);
  Wire.beginTransmission(0x70);
  Wire.write(0xEF);   
  Wire.write(0xC8); 
  Wire.endTransmission();
  delay(500);
  Wire.requestFrom(0x70, 3);  
}

float temperature(){
  int rcv1 = 0;
  int rcv2 = 0;
  Wire.beginTransmission(0x70);
  Wire.write(0x78);   
  Wire.write(0x66); 
  Wire.endTransmission();
  delay(100);
  Wire.requestFrom(0x70, 2); 
  while(Wire.available()) {
    rcv1 = Wire.read();
    rcv2 = Wire.read();
  }
  delay(100);
  float temp = (((4375 * ((rcv1 << 8) | rcv2)) >> 14) - 4500) / 100;
  return temp;
}

void setup() {
  Serial.begin(115200);
  shtc_init();
}

void loop() {
  delay(100);
  temp = temperature();
  Serial.println(temp);
  if(temp > LIMIT_TEMPERATURE){
    dc(1,255,1);
  } 
  else{
    dc(1,0,1);   
  }
}
