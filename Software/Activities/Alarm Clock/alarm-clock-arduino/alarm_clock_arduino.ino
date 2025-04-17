#include <Wire.h>               
#include <picobricks.h>         

// Define pins
#define NEOPIXEL   6            
#define BUTTON    10 
#define LDR       27 
#define BUZZER    20

#define NUMPIXELS  1            // Number of NeoPixel LEDs

NeoPixel pixels(NEOPIXEL, NUMPIXELS);  // Create NeoPixel object

// OLED screen configuration
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define SCREEN_ADDRESS 0x3C     // I2C address of the OLED display

SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);  // Create OLED object

int button = 0;  // Variable to store button state

void setup() {
  Wire.begin();             // Start I2C communication
  OLED.init();              // Initialize the OLED display
  OLED.clear();             // Clear the OLED screen
  OLED.show();              // Show the cleared screen

  pinMode(BUTTON, INPUT);       // Set button pin as input
  pinMode(LDR, INPUT);          // Set LDR pin as input
  pinMode(BUZZER, OUTPUT);      // Set buzzer pin as output

  pixels.setPixelColor(0, 0, 0, 0);    // Turn off LED initially
}

void loop() {
  OLED.setCursor(4, 3);                // Set text position on OLED
  OLED.print("Good night");           // Display "Good night" message
  OLED.show();                        // Refresh OLED screen

  // If it is dark (based on LDR reading)
  if (analogRead(LDR) < 200) {
    while (button != 1) {             // Wait for button press
      button = digitalRead(BUTTON);       // Read button state
      
      OLED.setCursor(4, 2);
      OLED.print("Good morning");     // Display "Good morning" message
      OLED.show();

      pixels.setPixelColor(0, 255, 255, 255); // Set LED to white

      tone(BUZZER, 494);                  // Play sound on buzzer (B4 note)
    }

    OLED.clear();                     // Clear OLED screen
    OLED.setCursor(4, 1);
    OLED.print("Have a nice day");    // Display farewell message
    OLED.show();

    noTone(BUZZER);                       // Stop buzzer
    pixels.setPixelColor(0, 0, 0, 0); // Turn off LED

    delay(10000);                     // Wait for 10 seconds before restarting loop
  }
}
