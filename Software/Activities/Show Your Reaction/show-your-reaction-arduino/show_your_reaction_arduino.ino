#include <Wire.h>
#include <picobricks.h>

// Define pin connections
#define LED_PIN 7         
#define BUTTON_PIN 10      
#define BUZZER_PIN 20      

// OLED screen configuration
#define SCREEN_WIDTH 128    // OLED display width, in pixels
#define SCREEN_HEIGHT 64    // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C // I2C address of the OLED display

int La = 440;               // Frequency for the La note (used for buzzer)
int old_time = 0;           // Variable to store the start time
int now_time = 0;           // Variable to store the current time
int score = 0;              // Player's reaction time (score)
char str[10];               // Buffer for displaying score as text
String string_score;        // String version of score

SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT); // Initialize OLED object

void setup() {
  Wire.begin();         // Initialize I2C communication
  OLED.init();          // Initialize OLED display
  OLED.clear();
  OLED.show();

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);  // Configure button as input
}

void loop() {
  // Display instructions to start the game
  OLED.setCursor(3, 0);
  OLED.print("Press the button");
  OLED.setCursor(5, 4);
  OLED.print("TO START");

  // Wait for button press to start the game
  if (digitalRead(BUTTON_PIN) == HIGH) {
    // Countdown from 3 to 1
    for (int i = 3; i > 0; i--) {
      String string_i = String(i);
      OLED.clear();
      OLED.show();
      OLED.setCursor(4, 8);
      sprintf(str, "%d", String(i)); // Convert number to string
      OLED.print(str);
      OLED.show();
      delay(1000);  // 1-second delay between each count
    }

    OLED.clear();
    OLED.show();
    OLED.setCursor(4, 6);
    OLED.print("GO!!!");

    // Wait for a random time before lighting up the LED
    int random_wait = random(1000, 5000); // Random delay between 1-5 seconds
    delay(random_wait);

    digitalWrite(LED_PIN, HIGH);  // Turn on LED to signal reaction test start
    old_time = millis();          // Record the start time

    // Wait for player to press the button and calculate reaction time
    while (!(digitalRead(BUTTON_PIN) == HIGH)) {
      now_time = millis();           // Continuously update current time
      score = now_time - old_time;   // Calculate reaction time
      string_score = String(score);  // Store score as string for display
    }

    digitalWrite(LED_PIN, HIGH);     // Keep LED on
    tone(BUZZER_PIN, La);            // Play tone to indicate button was pressed
    delay(200);                      // Tone duration
    noTone(BUZZER_PIN);              // Stop tone

    // Display the result
    OLED.clear();
    OLED.show();
    OLED.setCursor(1, 4);
    OLED.print("Press the");
    OLED.setCursor(2, 3);
    OLED.print("RESET BUTTON");
    OLED.setCursor(3, 3);
    OLED.print("To Repeat!");
    OLED.setCursor(6, 3);
    OLED.print("Score: ");
    OLED.setCursor(6, 9);
    sprintf(str, "%d", string_score);  // Print reaction time
    OLED.print(str);
    OLED.setCursor(6, 13);
    OLED.print(" ms");                // Milliseconds unit
    OLED.show();

    delay(10000);  // Show result for 10 seconds
    OLED.clear();
    OLED.show();
  }
}
