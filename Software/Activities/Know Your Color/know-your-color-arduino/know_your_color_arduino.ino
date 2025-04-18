#include <picobricks.h>   // Include the PicoBricks library
#include <Wire.h>         // Include the I2C communication library

// Define pins
#define RGB_PIN 6         // RGB LED pin
#define BUTTON_PIN 10     // Button pin
#define LDR_PIN 27        // LDR sensor pin

#define RGB_COUNT 1       // Number of RGB LEDs

// OLED screen configuration
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define SCREEN_ADDRESS 0x3C

// Create RGB and OLED display objects
NeoPixel strip(RGB_PIN, RGB_COUNT);
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

// Game state variables
int OLED_color;     // The color name shown on OLED
int RGB_color;      // The color shown on the RGB LED
int score = 0;      // Player score
int button = 0;     // Button state
char str[10];       // Character array for displaying numbers

void setup() {
  Wire.begin();  
  OLED.init();         // Initialize OLED
  OLED.clear();        // Clear the display
  OLED.show();         // Show the initial blank screen

  strip.setPixelColor(0, 0, 0, 0);  // Turn off RGB LED initially
  randomSeed(analogRead(LDR_PIN)); // Use LDR to randomize seed for true randomness
}

void loop() {
  // Start screen
  OLED.clear();
  OLED.show();
  OLED.setCursor(3, 1);              
  OLED.print("The game begins");
  strip.setPixelColor(0, 0, 0, 0);  // Turn off LED
  delay(2000);
  OLED.clear();
  OLED.show();
  
  // Run game loop for 10 rounds
  for (int i = 0; i < 10; i++) {
    button = digitalRead(BUTTON_PIN);
    random_color();  // Generate new color round

    // Wait for player input (max 2 seconds)
    unsigned long start_time = millis();
    while (button == 0) {
      button = digitalRead(BUTTON_PIN);
      if (millis() - start_time > 2000)
        break;
    }

    // Check if button was pressed and evaluate result
    if (button == 1) {
      if (OLED_color == RGB_color) {
        score += 10;  // Correct match
      } else {
        score -= 10;  // Wrong match
      }
      delay(200); // Small delay to avoid bouncing
    }

    // Prepare for next round
    OLED.clear();
    OLED.show();
    strip.setPixelColor(0, 0, 0, 0);  // Turn off LED
  }

  // Show final score
  OLED.clear();
  OLED.show();
  OLED.setCursor(2, 5);              
  OLED.print("Score: ");
  OLED.setCursor(4, 7);
  sprintf(str, "%d", score);              
  OLED.print(str);
  OLED.setCursor(6, 5);              
  OLED.print("points");
  OLED.show();
  
  delay(10000); // Show score for 10 seconds
}

// Function to assign and display a random color
void random_color() {
  OLED_color = random(1, 5); // Random color name
  RGB_color = random(1, 5);  // Random RGB color

  // Show the color name on OLED
  if (OLED_color == 1) {
    OLED.setCursor(3, 7);              
    OLED.print("red");
  }
  if (OLED_color == 2) {
    OLED.setCursor(3, 6);              
    OLED.print("green");
  }
  if (OLED_color == 3) {
    OLED.setCursor(3, 6);              
    OLED.print("blue");
  }
  if (OLED_color == 4) {
    OLED.setCursor(3, 6);              
    OLED.print("white");
  }

  // Show the actual color on RGB LED
  if (RGB_color == 1) {
    strip.setPixelColor(0, 255, 0, 0);      // Red
  }
  if (RGB_color == 2) {
    strip.setPixelColor(0, 0, 255, 0);      // Green
  }
  if (RGB_color == 3) {
    strip.setPixelColor(0, 0, 0, 255);      // Blue
  }
  if (RGB_color == 4) {
    strip.setPixelColor(0, 255, 255, 255);  // White
  }
}
