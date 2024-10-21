#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_ADDRESS 0x3D

Adafruit_SSD1306 oled(128, 64, &Wire);
float temp;

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
  Wire.begin();  
  shtc_init();
  oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  oled.clearDisplay();
  oled.setTextColor(WHITE);
}

void loop() {
  oled.clearDisplay();
  temp = temperature();
  Serial.print("Temp: ");
  Serial.println(temp);
  oled.setCursor(0, 0);
  oled.print("Temp: ");
  oled.setCursor(35, 0);
  oled.print(String(temp));
  oled.display();
  delay(100);
}
