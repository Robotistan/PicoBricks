#include <Wire.h>
#include <picobricks.h>

// Define hardware pins
#define GPIO_PIN 1         // Wire loop pin (game circuit detection)
#define LED_PIN 7          // Game status LED
#define BUTTON_PIN 10      // Start button
#define BUZZER_PIN 20      // Buzzer pin for game over sound

// OLED screen configuration
#define SCREEN_WIDTH 128   // OLED display width in pixels
#define SCREEN_HEIGHT 64   // OLED display height in pixels
#define SCREEN_ADDRESS 0x3C // OLED I2C address

int Time = 0;               // Variable to store elapsed time
unsigned long Old_Time = 0; // Variable to store start time
char str[10];               // String buffer to display time on screen

// Create an OLED display object
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);   // Set buzzer pin as output
  pinMode(LED_PIN, OUTPUT);      // Set LED pin as output
  pinMode(GPIO_PIN, OUTPUT);     // Set wire loop pin as output
  pinMode(BUTTON_PIN, INPUT);    // Set start button pin as input

  Wire.begin();                  // Initialize I2C communication
  OLED.init();                   // Initialize OLED display
  OLED.clear();                  // Clear display buffer
  OLED.show();                   // Show cleared screen
}

void loop() {
  digitalWrite(LED_PIN, LOW);    // Turn off LED at start

  // Show game title and prompt to start
  OLED.setCursor(2, 1);              
  OLED.print("BUZZ WIRE GAME"); 
  OLED.setCursor(4, 2);              
  OLED.print("Press Button"); 
  OLED.setCursor(5, 3);              
  OLED.print("TO START!");
  OLED.show();

  // Wait for button press to start the game
  while (!(digitalRead(BUTTON_PIN) == 1)) {}

  // Display "Game Started" message
  OLED.clear();
  OLED.setCursor(3, 6);              
  OLED.print("GAME"); 
  OLED.setCursor(5, 4);              
  OLED.print("STARTED");
  OLED.show();

  digitalWrite(GPIO_PIN, HIGH);      // Enable wire loop circuit
  Old_Time = millis();               // Record the start time

  // Wait until the player touches the wire (GPIO goes LOW)
  while (!(digitalRead(GPIO_PIN) == 0)) {
    Time = millis() - Old_Time;      // Continuously update elapsed time
  }

  // Show "Game Over" and elapsed time
  OLED.clear();
  OLED.setCursor(3, 4);              
  OLED.print("GAME OVER"); 
  OLED.setCursor(5, 4); 
  sprintf(str, "%d", Time);              
  OLED.print(str);
  OLED.setCursor(5, 10);              
  OLED.print("ms"); 
  OLED.show();

  // Flash LED and buzz to indicate game over
  digitalWrite(LED_PIN, HIGH);
  digitalWrite(BUZZER_PIN, HIGH);
  delay(500);
  digitalWrite(BUZZER_PIN, LOW);
  delay(5000);

  // Reset for next round
  Time = 0;
  Old_Time = 0;
  OLED.clear();
  OLED.show();
}
