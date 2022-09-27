#include <Wire.h>
#include <DHT.h>
#include "ACROBOTIC_SSD1306.h"
#define DHTPIN 11
#define DHTTYPE DHT11
//define the library

DHT dht(DHTPIN, DHTTYPE);
float temperature;
//define the temperature veriable

void setup() {
  //define dht sensor and Oled screen
  Serial.begin(115200);
  dht.begin();
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 
}

void loop() {
  temperature = dht.readTemperature();
  Serial.print("Temp: ");
  Serial.println(temperature);
  oled.setTextXY(3,1);              
  oled.putString("Temperature: ");
  //print "Temperature: " on the OLED at x=3 y=1
  oled.setTextXY(4,3);              
  oled.putString(String(temperature));
  //print the value from the temperature sensor to the oled screen at x=4 y=3
  Serial.println(temperature);
  delay(100);
}
