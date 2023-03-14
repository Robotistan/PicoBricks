#include <DHT.h>
#include <Wire.h>
#define LIMIT_TEMPERATURE     27
#define DHTPIN 11
#define DHTTYPE DHT11
#include "ACROBOTIC_SSD1306.h" // v1.0.0

DHT dht(DHTPIN, DHTTYPE);
float temperature;

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(21, OUTPUT);
  Wire.begin();
  oled.init();
  oled.clearDisplay();
}

void loop() {
  temperature = dht.readTemperature();
  Serial.print("Temp: ");
  Serial.println(temperature);
  
  oled.setTextXY(3, 1);
  oled.putString("Temperature: ");
  //print "Temperature: " on the OLED at x=3 y=1
  
  oled.setTextXY(4, 3);
  oled.putString(String(temperature));
  //print the value from the temperature sensor to the oled screen at x=4 y=3

  delay(100);
  temperature = dht.readTemperature();

  if (temperature > LIMIT_TEMPERATURE) {
    digitalWrite(21, HIGH);
  } else {
    digitalWrite(21, LOW);
  }

}
