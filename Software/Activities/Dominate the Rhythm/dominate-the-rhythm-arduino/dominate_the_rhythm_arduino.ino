#include <Wire.h>              // I2C communication library
#include <picobricks.h>        // PicoBricks hardware library

// Define hardware pins
#define BUTTON_PIN 10          // Button connected to pin 10
#define BUZZER_PIN 20          // Buzzer connected to pin 20
#define POT_PIN 26             // Potentiometer connected to pin 26

// OLED screen configuration
#define SCREEN_WIDTH 128       // OLED display width in pixels
#define SCREEN_HEIGHT 64       // OLED display height in pixels
#define SCREEN_ADDRESS 0x3C    // I2C address of OLED display

// Define musical notes (frequencies in Hz)
int Re = 294;
int Mi = 330;
int Fa = 349;
int La = 440;

char str[10];  // Buffer for displaying numbers as strings

// Create an OLED object
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

void setup()
{
  OLED.init();            // Initialize the OLED display
  OLED.clear();           // Clear the display
  OLED.show();            // Update the display

  pinMode(BUZZER_PIN, OUTPUT);     // Set buzzer pin as output
  pinMode(POT_PIN, INPUT);         // Set potentiometer pin as input
  pinMode(BUTTON_PIN, INPUT);      // Set button pin as input
}

void loop()
{
  int rithm = (analogRead(POT_PIN)) / 146;   // Read potentiometer value and scale it for rhythm

  // Display speed value on OLED
  OLED.setCursor(3, 4);              
  OLED.print("Speed: ");
  OLED.setCursor(3, 10); 
  sprintf(str, "%d", rithm);             
  OLED.print(str);
  OLED.show();

  delay(10); 

  // If button is pressed, start playing melody
  if (digitalRead(BUTTON_PIN) == 1) {

    OLED.clear(); 
    OLED.show();
    OLED.setCursor(3, 2);              
    OLED.print("Now playing...");
    OLED.show();

    // Play a simple melody using the buzzer
    tone(BUZZER_PIN, La); delay(1000 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Fa); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Re); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Fa); delay(500 / (rithm + 1));
    tone(BUZZER_PIN, Mi); delay(1000 / (rithm + 1));

    OLED.clear();         // Clear display after playing
    OLED.show();
  }

  noTone(BUZZER_PIN);     // Stop buzzer after melody
}
