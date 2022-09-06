#include <Wire.h>
#include "ACROBOTIC_SSD1306.h"

int temperature;
int reading;
int conversion_factor=3.3 / (65536);

void setup() {
  pinMode(4,INPUT);
  Serial.begin(115200);
  Wire.begin();  
  oled.init();                      
  oled.clearDisplay(); 

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
}

void loop() {
  reading = analogRead(4)*conversion_factor;
  temperature = 27 - (reading - 0.706)/0.001721;
  //String string_temperature = String(temperature);

  oled.setTextXY(3,1);              
  oled.putString("Sicaklik: ");
  oled.setTextXY(3,1);              
  //oled.putString(string_temperature);
  Serial.println(temperature);
  delay(10);
}
