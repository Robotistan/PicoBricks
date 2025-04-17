#include <picobricks.h>

#define trigPin 15       // Define trigger pin for ultrasonic sensor
#define echoPin 14       // Define echo pin for ultrasonic sensor
#define MOTOR_A 21       // Define motor pin
 
// Create a ServoSimple object for a servo motor
ServoSimple servo(MOTOR_A);

void setup() {
  Serial.begin(9600);              // Initialize serial communication at 9600 baud
  pinMode(trigPin, OUTPUT);        // Set trigger pin as output
  pinMode(echoPin, INPUT);         // Set echo pin as input
  servo.begin();                   // Initialize the servo motor
}

void loop() {
  long duration, distance;         // Variables to store ultrasonic timing and distance

  // Trigger the ultrasonic pulse
  digitalWrite(trigPin, LOW);      
  delayMicroseconds(2);            
  digitalWrite(trigPin, HIGH);     
  delayMicroseconds(10);           
  digitalWrite(trigPin, LOW);      

  // Measure the duration of echo pulse
  duration = pulseIn(echoPin, HIGH);
  
  // Convert duration to distance in cm
  distance = (duration / 2) / 29.1;

  if (distance < 80) {
    Serial.print(distance);         
    Serial.println(" cm");         
    servo.setAngle(179);           // Open the lid (move servo to open position)
  }
  else if (distance < 180) {
    Serial.print(distance);        
    Serial.println(" cm");        
    servo.setAngle(100);           // Close the lid (move servo to closed position)
  }
}
