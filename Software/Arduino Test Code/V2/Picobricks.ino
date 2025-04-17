// Include libraries
#include <picobricks.h>
#include <IRremote.h>
#include <WiFi.h>

// Define hardware pins
#define IR_PIN 0
#define RGB_PIN 6
#define LED_PIN 7
#define BUTTON_PIN 10
#define RELAY_PIN 12
#define BUZZER_PIN 20
#define POT_PIN 26
#define LDR_PIN 27

#define DECODE_NEC

// OLED screen configuration
#define SCREEN_WIDTH 128    // OLED display width, in pixels
#define SCREEN_HEIGHT 64    // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C // I2C address of the OLED display

#define RGB_COUNT 1         // Number of RGB LEDs

// Global variables
volatile int buttonState = 0;      // State of the user button
volatile int music_stt = 0;        // Music play status
float temperature;                 // Measured temperature
float humidity;                    // Measured humidity
float potantiometer;               // Potentiometer voltage
int ldr;                           // Light level percentage
char str[10];                      // String buffer for display
float noteDuration;                // Duration of a musical note
int WiFiStatus = 0;                // Status of WiFi connection

// Replace with your network credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";

// Function Declaration
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);  // OLED screen
NeoPixel strip (RGB_PIN, RGB_COUNT);  // RGB LED strip
SHTC3 shtc(0x70);   // SHTC3 sensor
motorDriver motor;  // Motor driver

// Interrupt service routine for the button
void buttonInterruptHandler() {
  buttonState = digitalRead(BUTTON_PIN);
  if (buttonState == HIGH) {
    music_stt = 1;  // Flag to start playing music
  }
}

// Generate sound on buzzer
void playNote(int frequency, int duration) {
  long period = 1000000L / frequency;
  long cycles = (long)frequency * duration / 1000;

  for (long i = 0; i < cycles; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delayMicroseconds(period / 2);
    digitalWrite(BUZZER_PIN, LOW);
    delayMicroseconds(period / 2);
  }
}

// Play melody when button is pressed
void play_music() {
  buttonState = digitalRead(BUTTON_PIN);
  if (buttonState == HIGH) {
    OLED.clear();
    OLED.drawBitmap(0, 0, music_bmp, 128, 64);  // Show music icon
    OLED.show();
    for (int thisNote = 0; thisNote < 95; thisNote++) {
      if (digitalRead(BUTTON_PIN) == LOW) {
        strip.setPixelColor(0, 0, 0, 0);       // Turn off RGB LED
        digitalWrite(BUZZER_PIN, LOW);         // Turn off buzzer
        digitalWrite(LED_PIN, LOW);            // Turn off LED
        OLED.clear();                          // Clear screen
        break;
      }
      else {
        digitalWrite(LED_PIN, HIGH);  // Light up LED
        strip.setPixelColor(0, random(0, 255), random(0, 255), random(0, 255));  // Random RGB color
        noteDuration = 110 * melody[thisNote][1];
        playNote(melody[thisNote][0], noteDuration);  // Play current note
      }
      if (thisNote == 94) {
        thisNote = 0;  // Restart the melody
      }
      delay(noteDuration * 0.2);  // Delay between notes
    }
  }
}

void setup() {
  Serial.begin(115200);  // Start serial communication
  Wire.begin();          // Start I2C communication

  // Setup pin modes
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(POT_PIN, INPUT);

  // Attach interrupt to button
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonInterruptHandler, CHANGE);

  // Attempt to connect to WiFi
  WiFi.begin(ssid, password);
  delay(200);

  if (WiFi.status() != WL_CONNECTED) {
    WiFiStatus = 0;
    Serial.println("network connection failed. Please Check ID and PASSWORD");
  } else {
    WiFiStatus = 1;
    Serial.println("connected");
    Serial.print("ip = ");
    Serial.println(WiFi.localIP());
  }

  // Initialize OLED display
  OLED.init();
  OLED.clear();
  OLED.drawBitmap(0, 0, Picobricks_img, 128, 64);
  OLED.show();

  shtc.begin();   // Start SHTC sensor
  IrReceiver.begin(IR_PIN);  // Start IR receiver

  // Relay on/off
  digitalWrite(RELAY_PIN, HIGH);
  delay(1000);
  digitalWrite(RELAY_PIN, LOW);
  delay(1000);
}

void loop() {
  OLED.clear();  // Clear display before drawing new data
  IrReceiver.decodedIRData.command = 0; // Reset IR command
  if (IrReceiver.decode()) {
    Serial.println(IrReceiver.decodedIRData.command);
    IrReceiver.resume();  // Ready to receive next IR signal
  } 

  if (IrReceiver.decodedIRData.command == number_1) { // RGB LED Walking light effect
    strip.setPixelColor(0, random(0, 255), random(0, 255), random(0, 255));
    delay(1000);
    strip.setPixelColor(0, 0, 0, 0);
  }
  if (IrReceiver.decodedIRData.command == number_2) { // Relay ON
    digitalWrite(RELAY_PIN, HIGH); 
    delay(100); 
  }
  if (IrReceiver.decodedIRData.command == number_3) { // Relay OFF
    digitalWrite(RELAY_PIN, LOW); 
    delay(100);  
  }
  if (IrReceiver.decodedIRData.command == number_4) { // DC Motors On
    motor.dc(1,255,0);
    motor.dc(2,255,0);
  }
  if (IrReceiver.decodedIRData.command == number_5) { // DC Motors Off
    motor.dc(1,0,0);
    motor.dc(2,0,0);
  }
  if (IrReceiver.decodedIRData.command == number_6) { //Buzzer
    for (long i = 0; i < 200; i++) {
      digitalWrite(BUZZER_PIN, HIGH);
      delayMicroseconds(500);
      digitalWrite(BUZZER_PIN, LOW);
      delayMicroseconds(500);
    }
  }
  if (IrReceiver.decodedIRData.command == number_8) { // Servo1 to 0 degrees
      motor.servo(1,0);
  }
  if (IrReceiver.decodedIRData.command == number_9) { // Servo1 to 90 degrees
      motor.servo(1,90);
  }

  // Music player status
  if (music_stt == 1) {
    play_music();
    music_stt = 0;
  }

  // OLED display updates
  OLED.setCursor(30, 0);
  OLED.print("PICOBRICKS");

  // Potentiometer value
  OLED.setCursor(0, 10);
  OLED.print("POT: ");
  OLED.setCursor(85, 10);
  potantiometer = (analogRead(POT_PIN) * 3.3) / 1023;
  sprintf(str, "%.2f", potantiometer);
  OLED.print(str);
  OLED.setCursor(120, 10);
  OLED.print("V");

  // Light Sensor (LDR) value
  OLED.setCursor(0, 20);
  OLED.print("LIGHT: ");
  OLED.setCursor(100, 20);
  ldr = (100 - (analogRead(LDR_PIN) * 100) / 1023);
  sprintf(str, "%d", ldr);
  OLED.print(str);
  OLED.setCursor(120, 20);
  OLED.print("%");

  // Temperature value from SHTC3
  OLED.setCursor(0, 30);
  OLED.print("TEMP: ");
  OLED.setCursor(80, 30);
  temperature = shtc.readTemperature();
  sprintf(str, "%.2f", temperature);
  OLED.print(str);
  OLED.setCursor(120, 30);
  OLED.print("C");

  // Humidity value from SHTC3
  OLED.setCursor(0, 40);
  OLED.print("HUMIDITY: ");
  OLED.setCursor(80, 40);
  humidity = shtc.readHumidity();
  sprintf(str, "%.2f", humidity);
  OLED.print(str);
  OLED.setCursor(120, 40);
  OLED.print("%");

  // IP Address from WiFi
  OLED.setCursor(0, 50);
  OLED.print("IP:");
  OLED.setCursor(70, 50);
  if(WiFiStatus == 1){
    IPAddress localIP = WiFi.localIP();
    String ipAddressString = localIP.toString();
    OLED.print(ipAddressString.c_str());  
  }
  else{
    OLED.print("0.0.0.0");  // Update OLED display
  }
  OLED.show();  // Update OLED display
}
