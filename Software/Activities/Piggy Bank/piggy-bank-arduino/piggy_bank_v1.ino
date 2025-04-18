#include <picobricks.h>

// Define ultrasonic sensor pins
#define echoPin 14           // Echo pin of the ultrasonic sensor (HC-SR04)
#define trigPin 15           // Trigger pin of the ultrasonic sensor

// Define the pin connected to the servo motor
#define MOTOR_1 21

// Create a ServoSimple object to control the servo on pin 21
ServoSimple Servo(MOTOR_1);

void setup() {
  pinMode(trigPin, OUTPUT);  // Set trigger pin as output
  pinMode(echoPin, INPUT);   // Set echo pin as input
  Servo.begin();             // Initialize the servo motor
}

void loop() {
  long duration, distance;

  // Trigger the ultrasonic sensor by sending a 10µs pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the duration of the echo pulse
  duration = pulseIn(echoPin, HIGH);

  // Convert the time into a distance in centimeters
  distance = (duration / 2) / 29.1;

  // If an object is detected closer than 5 cm
  if (distance < 5) {
    Servo.setAngle(179);  // Open or move servo to max angle
  }
  else {
    Servo.setAngle(100);  // Set servo to default position
  }
}
