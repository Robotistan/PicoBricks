#include "EspDHT.h"
EspDHT dht;
void setup() {
  // put your setup code here, to run once:
  dht.setup(11, EspDHT::DHT11);
  pinMode(21,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
  dht.readSensor();
  float temperature = dht.getTemperature();

  if(temperature>27){
    digitalWrite(21,HIGH);
  } else{
    digitalWrite(21,HIGH);    
  }


}
