/*
You must select the "Raspberry Pico W" board from the Arduino IDE board manager for PicoBricks library.
*/

// Include libraries
#include <picobricks.h>
#include <pitches.h>
#include <WiFi.h>   //WifiNINA by Arduino

// Define hardware pins
#define IR_PIN 0
#define RGB_PIN 6
#define LED_PIN 7
#define BUTTON_PIN 10
#define DHT_PIN 11
#define RELAY_PIN 12
#define BUZZER_PIN 20
#define MOTOR_1 21
#define MOTOR_2 22
#define POT_PIN 26
#define LDR_PIN 27

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
int irCode = 0;
volatile bool irReceived = false;

// Replace with your network credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";

// Function Declaration
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);    // OLED screen
NeoPixel strip(RGB_PIN, RGB_COUNT);                           // RGB LED strip
DHT11 dht(DHT_PIN);                                           // DHT11 sensor
ServoSimple Servo(MOTOR_1);                                   // Servo motor
IRPico ir(IR_PIN);                                            // Start IR receiver

// Interrupt service routine for the button
void buttonInterruptHandler() {
  buttonState = digitalRead(BUTTON_PIN);
  if (buttonState == HIGH) {
    music_stt = 1; // Flag to start playing music
  }
}

// Interrupt service routine for IR
void irInterruptHandler() {
  if (ir.decode()) {
    irCode = ir.getCode();
    irReceived = true;
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
    OLED.drawBitmap(0, 0, music_bmp, 128, 64); // Show music icon
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
  pinMode(MOTOR_1, OUTPUT);
  pinMode(MOTOR_2, OUTPUT);

  Servo.begin();  // Initialize servo motor

  // Attach interrupt to button
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonInterruptHandler, CHANGE);
  // Attach interrupt to ir
  attachInterrupt(digitalPinToInterrupt(IR_PIN), irInterruptHandler, FALLING);

  // Attempt to connect to WiFi
  WiFi.begin(ssid, password);
  delay(200);
  if (WiFi.status() != WL_CONNECTED) {
    WiFiStatus = 0;
    Serial.println("network connection failed. Please Check ID and PASSWORD");
  } 
  else {
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

  dht.begin();    // Start DHT11 sensor

  // Relay on/off
  digitalWrite(RELAY_PIN, HIGH);
  delay(1000);
  digitalWrite(RELAY_PIN, LOW);
  delay(1000);
}

void loop() {
  OLED.clear();  // Clear display before drawing new data

  if (irReceived) {
    Serial.println(irCode, HEX);

    if (irCode == number_1) { // RGB LED Walking light effect
      strip.setPixelColor(0, random(0, 255), random(0, 255), random(0, 255));
      delay(1000);
      strip.setPixelColor(0, 0, 0, 0);
    }
    if (irCode == number_2) { // Relay ON
      digitalWrite(RELAY_PIN, HIGH); 
      delay(100); 
    }
    if (irCode == number_3) { // Relay OFF
      digitalWrite(RELAY_PIN, LOW); 
      delay(100);  
    }
    if (irCode == number_4) { // DC Motors On
      digitalWrite(MOTOR_1, HIGH);
      digitalWrite(MOTOR_2, HIGH);
    }
    if (irCode == number_5) { //DC Motors Off
      digitalWrite(MOTOR_1, LOW);
      digitalWrite(MOTOR_2, LOW);
    }
    if (irCode == number_6) { //Buzzer
      for (long i = 0; i < 200; i++) {
        digitalWrite(BUZZER_PIN, HIGH);
        delayMicroseconds(500);
        digitalWrite(BUZZER_PIN, LOW);
        delayMicroseconds(500);
      }
    }
    if (irCode == number_8) { // Servo1 to 0 degrees
      Servo.setAngle(0);
    }
    if (irCode == number_9) { // Servo1 to 90 degrees
      Servo.setAngle(90);
    }
    irReceived = false;
    irCode = 0;
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
  OLED.setCursor(90, 10);
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

  // Temperature value from DHT11 
  OLED.setCursor(0, 30);
  OLED.print("TEMP: ");
  OLED.setCursor(80, 30);
  temperature = dht.readTemperature();
  sprintf(str, "%.2f", temperature);
  OLED.print(str);
  OLED.setCursor(120, 30);
  OLED.print("C");

  // Humidity value from DHT11
  OLED.setCursor(0, 40);
  OLED.print("HUMIDITY: ");
  OLED.setCursor(80, 40);
  humidity = dht.readHumidity();
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
    OLED.print("0.0.0.0");
  }

  OLED.show();  // Update OLED display
}
