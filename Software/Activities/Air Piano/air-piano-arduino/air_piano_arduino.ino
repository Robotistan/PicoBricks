#include <Wire.h>
#include <picobricks.h>

//Define Pin
#define BUZZER 20

// Define the pins for the ultrasonic sensor
#define TRIGGER_PIN  15     // Trigger pin of HC-SR04
#define ECHO_PIN     14     // Echo pin of HC-SR04
#define MAX_DISTANCE 400    // Maximum measurable distance (not used in this example)

// OLED screen configuration
#define SCREEN_WIDTH 128    // OLED display width, in pixels
#define SCREEN_HEIGHT 64    // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C // I2C address of the OLED display

// Note frequencies (in Hz) corresponding to musical notes
#define T_C 262  // Do (C)
#define T_D 294  // Re (D)
#define T_E 330  // Mi (E)
#define T_F 349  // Fa (F)
#define T_G 392  // Sol (G)
#define T_A 440  // La (A)
#define T_B 493  // Si (B)

// Create an instance of the OLED display
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

// Buffer for converting distance to string for OLED display
char str[10];

// Variables for distance measurement
long duration, cm;

// Measure distance using the ultrasonic sensor
void measureDistance() {
  delay(40);
  digitalWrite(TRIGGER_PIN, LOW);       // Ensure trigger pin is LOW
  delayMicroseconds(5);

  digitalWrite(TRIGGER_PIN, HIGH);      // Send 10µs pulse to trigger measurement
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);   // Read the time of the echo pulse
  cm = (duration / 2) / 29.1;           // Convert duration to centimeters
}

void setup() {
  pinMode(BUZZER, OUTPUT);         // Set buzzer pin as output
  pinMode(TRIGGER_PIN, OUTPUT);    // Set ultrasonic trigger pin as output
  pinMode(ECHO_PIN, INPUT);        // Set ultrasonic echo pin as input

  Wire.begin();                    // Start I2C communication
  OLED.init();                     // Initialize OLED
  OLED.clear();                    // Clear the screen
}

void loop() {
  delay(50);
  measureDistance();         // Measure distance
  int distance = cm;         // Store the result

  // Play different tones based on the distance range
  if (distance > 5 && distance < 11)
    tone(Buzzer, T_C);
  else if (distance > 10 && distance < 16)
    tone(Buzzer, T_D);
  else if (distance > 15 && distance < 21)
    tone(Buzzer, T_E);
  else if (distance > 20 && distance < 26)
    tone(Buzzer, T_F);
  else if (distance > 25 && distance < 31)
    tone(Buzzer, T_G);
  else if (distance > 30 && distance < 36)
    tone(Buzzer, T_A);
  else if (distance > 35 && distance < 41)
    tone(Buzzer, T_B);
  else
    noTone(Buzzer); // Stop playing tone if distance is outside all ranges

  // Display the distance on the OLED screen
  OLED.clear();                   // Clear the previous content

  OLED.setCursor(0, 20);          // Move cursor to left for the label
  OLED.print("Distance:");

  OLED.setCursor(80, 20);         // Move cursor to middle to print value
  sprintf(str, "%d", distance);   // Convert distance to string
  OLED.print(str);

  OLED.setCursor(110, 20);        // Move cursor to right for unit
  OLED.print("cm");

  OLED.show();                    // Update OLED display with new values
}
