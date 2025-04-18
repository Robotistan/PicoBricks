#include <picobricks.h>  // Include PicoBricks hardware library

// Define pins
#define DHT_PIN 11       // Pin connected to DHT11 temperature sensor
#define MOTOR_1 21       // Pin connected to fan or motor

#define LIMIT_TEMPERATURE 27  // Temperature threshold in °C

float temperature;            // Variable to store temperature reading

DHT11 dht(DHT_PIN);           // Create DHT11 sensor object

void setup() {
  Serial.begin(115200);       // Start serial communication for debugging
  dht.begin();                // Initialize DHT11 sensor
  pinMode(MOTOR_1, OUTPUT);   // Set motor pin as output
}

void loop() {
  // Read temperature from DHT11 sensor
  temperature = dht.readTemperature();

  // Print the temperature value to the Serial Monitor
  Serial.print("Temp: ");
  Serial.println(temperature);

  // If the temperature exceeds the limit, turn on the motor (fan)
  if (temperature > LIMIT_TEMPERATURE) {
    digitalWrite(MOTOR_1, HIGH);  // Turn motor ON
  } 
  else {
    digitalWrite(MOTOR_1, LOW);   // Turn motor OFF
  }

  delay(100);  // Small delay before next reading
}
