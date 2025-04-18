#include <picobricks.h>  // Include PicoBricks hardware library

// Define pins
#define MOTOR_2 22         // Servo motor connected to pin 22
#define LDR_PIN 27         // Light-dependent resistor (LDR) connected to pin 27

// Create Servo object on specified pin
ServoSimple Servo(MOTOR_2); 

void setup() {
  Servo.setAngle(20);           // Set initial angle of the servo motor
  pinMode(LDR_PIN, INPUT);      // Set LDR pin as input to read light level
}

void loop() {
  int light_sensor = analogRead(LDR_PIN);  // Read analog value from LDR

  // If light level is above threshold
  if (light_sensor > 100) {
    int x = 45;  // Target angle for servo
    int y = 20;  // Return angle for servo
    
    Servo.setAngle(x);  // Move servo to position x
    delay(100);         // Wait for servo to reach position

    Servo.setAngle(y);  // Move servo back to position y
    delay(500);         // Wait before next check
  }
}
