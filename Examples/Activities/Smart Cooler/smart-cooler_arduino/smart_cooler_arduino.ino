#include <DHT.h>

#define LIMIT_TEMPERATURE     27
#define DHTPIN 11
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
float temperature;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  dht.begin();
  pinMode(21,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
  temperature = dht.readTemperature();
  Serial.print("Temp: ");
  Serial.println(temperature);
  if(temperature > LIMIT_TEMPERATURE){
    digitalWrite(21,HIGH);
  } else{
    digitalWrite(21,LOW);    
  }


}
