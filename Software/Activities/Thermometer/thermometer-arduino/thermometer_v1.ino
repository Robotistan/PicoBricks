#include <Wire.h>
#include <DHT.h>
#include <Adafruit_SSD1306.h>

#define DHTPIN 11
#define DHTTYPE DHT11
#define SCREEN_ADDRESS 0x3D

DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 oled(128, 64, &Wire);
float temperature;

void setup() {
  Serial.begin(115200);
  Wire.begin();  
  dht.begin();
  oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  oled.clearDisplay();
  oled.setTextColor(WHITE);
}

void loop() {
  temperature = dht.readTemperature();
  Serial.print("Temp: ");
  Serial.println(temperature);
  oled.setCursor(0, 0);
  oled.print("Temp: ");
  oled.setCursor(35, 0);
  oled.print(String(temperature));
  oled.display();
  delay(100);
}
