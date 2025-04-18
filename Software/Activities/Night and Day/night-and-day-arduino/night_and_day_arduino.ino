#include <Wire.h>
#include <picobricks.h>

// Define hardware pins
#define BUTTON_PIN 10
#define BUZZER_PIN 20
#define LDR_PIN 27
#define RANDOM_SEED_PIN 28

// OLED screen configuration
#define SCREEN_WIDTH 128    
#define SCREEN_HEIGHT 64    
#define SCREEN_ADDRESS 0x3C 

// Game state variables
int Gamer_Reaction = 0;    // Holds player's reaction (0: light, 1: dark)
int Night_or_Day = 0;      // Randomly generated state: 0 = NIGHT, 1 = DAY
int Score = 0;             // Player's score
int counter = 0;           // Used to stop the game after ending
double currentTime = 0;    
double lastTime = 0;       
char str[10];              // Buffer to format strings on OLED

// Create OLED display object
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

// Get the time passed since the last prompt
double getLastTime() {
  return currentTime = millis() / 1000.0 - lastTime;
}

// Custom delay function with loop calls
void _delay(float seconds) {
  long endTime = millis() + seconds * 1000;
  while (millis() < endTime) _loop();
}

// Placeholder for repeated background processes
void _loop() {
}

// Required for compatibility with loop() structure
void loop() {
  _loop();
}

void setup() {
  // Set pin modes
  pinMode(BUTTON_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  randomSeed(RANDOM_SEED_PIN);  // Use a pin to seed randomness

  Wire.begin();           // Initialize I2C
  OLED.init();            // Initialize OLED
  OLED.clear(); OLED.show();

  // Display welcome message
  OLED.setCursor(1, 3); OLED.print("NIGHT and DAY");
  OLED.setCursor(2, 7); OLED.print("GAME");
  OLED.setCursor(5, 2); OLED.print("Press the BUTTON");
  OLED.setCursor(6, 4); OLED.print("to START!");
  OLED.show();

  Score = 0;

  // Wait until button is pressed to start game
  while (!(digitalRead(BUTTON_PIN) == HIGH)) {
    _loop();
  }

  _delay(0.2);  // Small delay after button press

  while (1) {
    if (counter == 0) {
      delay(500);
      Change_Word();  // Show "NIGHT" or "DAY"
      lastTime = millis() / 1000.0;
    }

    // Player has 2 seconds to react
    while (!(getLastTime() > 2)) {
      if (analogRead(LDR_PIN) > 200) {
        Gamer_Reaction = 0;  // Light detected
      } else {
        Gamer_Reaction = 1;  // Darkness detected
      }
    }

    // Sound the buzzer to notify end of reaction time
    digitalWrite(BUZZER_PIN, HIGH);
    delay(250);
    digitalWrite(BUZZER_PIN, LOW);

    // Check if player's reaction matches the expected value
    if (Night_or_Day == Gamer_Reaction) {
      Correct();  // Add score
    } else {
      Wrong();    // End game
    }

    _loop();

    // Check if player reached 100 points and won the game
    if (Score == 100) {
      OLED.clear(); OLED.show();
      OLED.setCursor(1, 1); OLED.print("Congratulation");
      OLED.setCursor(3, 1); OLED.print("Your Score");
      OLED.setCursor(3, 13); sprintf(str, "%d", Score); OLED.print(str);
      OLED.setCursor(5, 3); OLED.print("Press Reset");
      OLED.setCursor(6, 3); OLED.print("To Repeat!");
      OLED.show();

      // Sound buzzer three times
      for (int i = 0; i < 3; i++) {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(500);
        digitalWrite(BUZZER_PIN, LOW);
        delay(500);
      }

      counter = 1;  // End game
    }
  }
}

// Display success message and update score
void Correct() {
  Score += 10;
  OLED.clear(); OLED.show();
  OLED.setCursor(3, 4);
  OLED.print("10 Points");
  OLED.show();
}

// Display "NIGHT" or "DAY" randomly
void Change_Word() {
  OLED.clear(); OLED.show();
  Night_or_Day = random(0, 2);
  if (Night_or_Day == 0) {
    OLED.setCursor(3, 6); OLED.print("NIGHT");
  } else {
    OLED.setCursor(3, 7); OLED.print("DAY");
  }
  OLED.show();
}

// Show game over screen and stop the game
void Wrong() {
  OLED.clear(); OLED.show();
  OLED.setCursor(1, 3); OLED.print("Game Over");
  OLED.setCursor(3, 1); OLED.print("Your Score");
  OLED.setCursor(1, 13); sprintf(str, "%d", Score); OLED.print(str);
  OLED.setCursor(5, 3); OLED.print("Pres Reset");
  OLED.setCursor(6, 3); OLED.print("To Repeat");

  digitalWrite(BUZZER_PIN, HIGH);
  delay(1000);
  digitalWrite(BUZZER_PIN, LOW);
  counter = 1;
}
