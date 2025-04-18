#include <Wire.h>
#include <picobricks.h>

// Define hardware pins
#define BUTTON_PIN 10       // Button input to start/stop the timer
#define POT_PIN 26          // Potentiometer input to set timer value

// OLED screen configuration
#define SCREEN_WIDTH 128    
#define SCREEN_HEIGHT 64    
#define SCREEN_ADDRESS 0x3C 

// Timer variables
int minute;
int second = 59;
int milisecond = 9;
int setTimer;               // Timer duration set by potentiometer
char str[10];               // Buffer for string formatting

// Create OLED object
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);

void setup() {
  pinMode(BUTTON_PIN, INPUT);  // Set button pin as input
  pinMode(POT_PIN, INPUT);     // Set potentiometer pin as input

  Wire.begin();                // Initialize I2C communication
  OLED.init();                 // Initialize OLED
  OLED.clear();                // Clear display
  OLED.show();                 // Show initial screen
}

void loop() {
  // Display instruction on OLED
  OLED.setCursor(1, 2);              
  OLED.print("<<My Timer>>");
  OLED.setCursor(3, 1);              
  OLED.print("Please use the");
  OLED.setCursor(4, 1);              
  OLED.print("Potentiometer");
  OLED.setCursor(5, 0);              
  OLED.print("to set the Timer");
  OLED.show();
  delay(3000);
  OLED.clear();
  OLED.show(); 
  
  // Allow user to set timer with potentiometer
  while (!(digitalRead(BUTTON_PIN) == 1)) {
    setTimer = (analogRead(POT_PIN) * 60) / 1023;  // Map analog input to 0-60 minutes
    OLED.setCursor(3, 1);              
    OLED.print("set to:");
    OLED.setCursor(3, 8); 
    sprintf(str, "%d", setTimer);             
    OLED.print(str);
    OLED.setCursor(3, 11);              
    OLED.print("min.");
    OLED.show();
  }

  // Display countdown start message
  OLED.clear();
  OLED.show();
  OLED.setCursor(1, 1);              
  OLED.print("The Countdown");
  OLED.setCursor(2, 3);              
  OLED.print("has begun!");

  // Countdown logic until button is pressed
  while (!(digitalRead(BUTTON_PIN) == 1)) {
    milisecond = 9 - (millis() % 100) / 10;
    second = 59 - (millis() % 60000) / 1000;
    minute = (setTimer - 1) - ((millis() % 360000) / 60000);

    OLED.setCursor(5, 3);   
    sprintf(str, "%d", minute); OLED.print(str);           
    OLED.setCursor(5, 8); 
    sprintf(str, "%d", second); OLED.print(str);              
    OLED.setCursor(5, 13);  
    sprintf(str, "%d", milisecond); OLED.print(str);  

    // Print time separators
    OLED.setCursor(5, 6); OLED.print(":");
    OLED.setCursor(5, 11); OLED.print(":");
    OLED.show();
  }

  // After button is pressed, display the stopped time
  OLED.setCursor(5, 3);   sprintf(str, "%d", minute); OLED.print(str);           
  OLED.setCursor(5, 8);   sprintf(str, "%d", second); OLED.print(str);              
  OLED.setCursor(5, 13);  sprintf(str, "%d", milisecond); OLED.print(str);           
  OLED.setCursor(5, 6);   OLED.print(":");
  OLED.setCursor(5, 11);  OLED.print(":");
  OLED.show();
  delay(10000);

  // If the timer reached zero
  if (minute == 0 && second == 0 && milisecond == 0) {
    OLED.setCursor(5, 3);   sprintf(str, "%d", minute); OLED.print(str);           
    OLED.setCursor(5, 8);   sprintf(str, "%d", second); OLED.print(str);            
    OLED.setCursor(5, 13);  sprintf(str, "%d", milisecond); OLED.print(str);             
    OLED.setCursor(5, 6);   OLED.print(":");
    OLED.setCursor(5, 11);  OLED.print(":");  
    OLED.print("-finished-");
    OLED.setCursor(7, 5); 
    OLED.show();
    delay(10000);
  }
}
