#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Adafruit_NeoPixel.h>
//Define libraries.


#define RST_PIN    26
#define SS_PIN     17
#define servoPin   22
#define PIN        6 
#define NUMPIXELS  1
#define buzzer     20
//define pins of servo,buzzer,neopixel and rfid.

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Servo motor;
MFRC522 rfid(SS_PIN, RST_PIN);

byte ID[4] = {"Write your own ID."};

void setup() { 
  pixels.begin();
  motor.attach(servoPin);
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(buzzer, OUTPUT);
  
}
 
void loop()
{
  pixels.clear();
  
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  if 
  (
    rfid.uid.uidByte[0] == ID[0] &&
    rfid.uid.uidByte[1] == ID[1] &&
    rfid.uid.uidByte[2] == ID[2] &&
    rfid.uid.uidByte[3] == ID[3] ) 
  {
        Serial.println("Door Opened.");
        printid();
        tone(buzzer,523);
        delay(200);
        noTone(buzzer);
        delay(100);
        tone(buzzer,523);
        delay(200);
        noTone(buzzer);
        pixels.setPixelColor(0, pixels.Color(0, 250, 0));
        delay(200);
        pixels.show();
        pixels.setPixelColor(0, pixels.Color(0, 0, 0));
        delay(200);
        pixels.show();
        motor.write(180);
        delay(2000);
        motor.write(0);
        delay(1000);
     //RGB LED turns green and the door opens thanks to the servo motor if the correct card is read to the sensor.
    }
    else
    {
      Serial.println("Unknown Card.");
      printid();
      tone(buzzer,494);
      delay(200);
      noTone(buzzer);
      delay(100);
      tone(buzzer,494);
      delay(200);
      noTone(buzzer);
      pixels.setPixelColor(0, pixels.Color(250, 0, 0));
      delay(100);
      pixels.show();
      pixels.setPixelColor(0, pixels.Color(0, 0, 0));
      delay(100);
      pixels.show();
      //RGB LED turns red and the door does not open if the wrong card is read to the sensor
    }
  rfid.PICC_HaltA();
}
void printid()
{
  Serial.print("ID Number: ");
  for(int x = 0; x < 4; x++){
    Serial.print(rfid.uid.uidByte[x]);
    Serial.print(" ");
  }
  Serial.println("");
}
