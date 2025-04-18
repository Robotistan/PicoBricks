#include <Wire.h>
#include <picobricks.h>

// Define pin numbers for connected components
#define LED_PIN 7             // LED pin
#define BUTTON_PIN 10         // Button pin
#define ECHO_PIN 14           // Echo pin of ultrasonic sensor
#define TRIGGER_PIN 15        // Trigger pin of ultrasonic sensor
#define BUZZER_PIN 20         // Buzzer pin

#define MAX_DISTANCE 400      // Maximum measurable distance in cm

// OLED screen configuration
#define SCREEN_WIDTH 128      // OLED width in pixels
#define SCREEN_HEIGHT 64      // OLED height in pixels
#define SCREEN_ADDRESS 0x3C   // I2C address for OLED

// Variables for ultrasonic measurement
long duration = 0;            // Pulse duration
long cm = 0;                  // Measured distance in cm
int distance = 0;             // Averaged distance result
int total = 0;                // Total value for averaging
char str[10];                 // Buffer to format distance as string

// Initialize OLED display object
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

// Function to measure distance using ultrasonic sensor
void measureDistance() {
  delay(40);
  digitalWrite(TRIGGER_PIN, LOW);       // Start with LOW
  delayMicroseconds(5);

  digitalWrite(TRIGGER_PIN, HIGH);      // Trigger a 10µs pulse
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);   // Read echo time
  cm = (duration / 2) / 29.1;           // Convert echo time to distance in cm
}

void setup() {
  // Set pin modes
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  // Initialize I2C and OLED display
  Wire.begin();  
  OLED.init();
  OLED.clear();
  OLED.show();
}

void loop() {
  delay(50);  // Short delay between loops

  // Wait for button press to start measurement
  if (digitalRead(BUTTON_PIN) == HIGH) {

    int measure = 0;
    digitalWrite(LED_PIN, HIGH);      // Turn on LED for visual feedback
    tone(BUZZER_PIN, 493);            // Play a tone (B note) to signal start
    delay(500);
    noTone(BUZZER_PIN);               // Stop the buzzer

    // Take 20 distance measurements and sum them
    for (int i = 0; i < 20; i++) {
      measureDistance();              // Call ultrasonic function
      measure = cm;                   // Get current distance
      total = total + measure;        // Add to total for averaging
      delay(50);                      // Wait between samples
    }

    distance = (total / 20) + 6;      // Average the total, +6 for offset correction
    digitalWrite(LED_PIN, LOW);       // Turn off LED

    delay(1000);                      // Pause before showing result

    // Display result on OLED screen
    OLED.clear();
    OLED.setCursor(2, 1);              
    OLED.print(">Digital Ruler<");     // Title
    OLED.setCursor(5, 1);              
    OLED.print("Distance: ");
    OLED.setCursor(5, 10);              
    sprintf(str, "%d", distance);      // Format distance to string
    OLED.print(str);
    OLED.setCursor(5, 12);              
    OLED.print("cm");
    OLED.show();                       // Display content

    // Reset values for next measurement
    measure = 0;
    distance = 0;
    total = 0;
  }
}
