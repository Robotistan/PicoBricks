#include <picobricks.h>  // Include PicoBricks hardware library

// Define hardware pins
#define RGB_PIN 6         // Pin connected to RGB NeoPixel
#define BUZZER_PIN 20     // Pin connected to passive buzzer
#define MOTOR_1 21        // Pin for servo motor 1 (door mechanism)
#define MOTOR_2 22        // Pin for servo motor 2 (up/down mechanism)
#define LDR_PIN 27        // Pin connected to LDR (light sensor)

#define RGB_COUNT 1       // Number of RGB LEDs in the strip

int angleupdown;          // Variable to keep track of current angle of Servo2

// Create objects for RGB and Servo control
NeoPixel strip(RGB_PIN, RGB_COUNT);         // Initialize NeoPixel object
ServoSimple Servo1(MOTOR_1);                // Servo1 controls opening/closing
ServoSimple Servo2(MOTOR_2);                // Servo2 controls up/down motion

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);              // Set buzzer pin as output
  pinMode(LDR_PIN, INPUT);                  // Set LDR pin as input

  Servo1.begin();                           // Initialize Servo1
  Servo2.begin();                           // Initialize Servo2

  strip.setPixelColor(0, 0, 0, 0);          // Turn off NeoPixel LED

  Open();                                   // Start by opening the servo-controlled mechanism
  angleupdown = 180;                        // Set initial angle
  Servo2.setAngle(angleupdown);             // Move Servo2 to default position
}

void loop() {
  // Check if light level is above threshold
  if (analogRead(LDR_PIN) > 150) {
    strip.setPixelColor(0, 255, 0, 0);      // Turn RGB LED red
    delay(1000);

    tone(BUZZER_PIN, 700);                  // Sound buzzer
    delay(1000);
    noTone(BUZZER_PIN);                     // Stop buzzer

    Open();                                 // Open the mechanism
    delay(500);
    Down();                                 // Move downward
    delay(500);
    Close();                                // Close the mechanism
    delay(500);
    Up();                                   // Move upward

    strip.setPixelColor(0, 0, 255, 0);      // Turn RGB LED green
    delay(10000);

    strip.setPixelColor(0, 0, 0, 0);        // Turn off RGB LED

    Open();                                 // Re-open the mechanism
    angleupdown = 180;                      // Reset angle
    Servo2.setAngle(angleupdown);           // Reset servo position
  }
}

// Function to open the door (servo at 180 degrees)
void Open() {
  Servo1.setAngle(180);
}

// Function to close the door (servo at 30 degrees)
void Close() {
  Servo1.setAngle(30);
}

// Function to raise the mechanism slowly
void Up() {
  for (int i = 0; i < 45; i++) {
    angleupdown = angleupdown + 2;
    Servo2.setAngle(angleupdown);
    delay(30);
  }
}

// Function to lower the mechanism slowly
void Down() {
  for (int i = 0; i < 45; i++) {
    angleupdown = angleupdown - 2;
    Servo2.setAngle(angleupdown);
    delay(30);
  }
}
