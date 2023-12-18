#include <SPI.h>
#include <MFRC522.h>
//define libraries

int RST_PIN = 26;
int SS_PIN = 17;
//define pins

MFRC522 rfid(SS_PIN, RST_PIN);

void setup()
{
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {

  if (!rfid.PICC_IsNewCardPresent())
    return;
  if (!rfid.PICC_ReadCardSerial())
    return;
    rfid.uid.uidByte[0] ;
    rfid.uid.uidByte[1] ;
    rfid.uid.uidByte[2] ;
    rfid.uid.uidByte[3] ; 
    printid();
  rfid.PICC_HaltA();
//Reading your ID.
}
void printid() 
{
  Serial.print("Your ID: ");
  for (int x = 0; x < 4; x++) {
    Serial.print(rfid.uid.uidByte[x]);
    Serial.print(" ");
  }
  Serial.println("");
}
