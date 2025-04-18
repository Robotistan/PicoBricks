#include <Wire.h>             // Include library for I2C communication
#include <picobricks.h>       // Include the main PicoBricks library

#define DHT_PIN 11            // Define the GPIO pin where the DHT11 sensor is connected

// OLED screen configuration
#define SCREEN_WIDTH 128      // OLED display width in pixels
#define SCREEN_HEIGHT 64      // OLED display height in pixels
#define SCREEN_ADDRESS 0x3C   // I2C address of the OLED display

float temperature;            // Variable to hold the temperature value
char str[10];                 // Character buffer for converting temperature to string

DHT11 dht(DHT_PIN);           // Create DHT11 object
SSD1306 OLED(SCREEN_ADDRESS, SCREEN_WIDTH, SCREEN_HEIGHT);  // Create OLED object

void setup() {
  Serial.begin(115200);       // Initialize serial communication for debugging
  Wire.begin();               // Start I2C communication
  dht.begin();                // Initialize the DHT11 sensor
  OLED.init();                // Initialize the OLED display
  OLED.clear();               // Clear any previous display content
  OLED.show();                // Show the cleared screen
}

void loop() {
  temperature = dht.readTemperature();     // Read the temperature from the DHT11 sensor
  Serial.print("Temp: ");                  // Print to serial for debugging
  Serial.println(temperature);             // Print the temperature value

  OLED.setCursor(0, 0);                    // Set OLED cursor to start of the first line
  OLED.print("Temp: ");                    // Display label on OLED
  OLED.setCursor(35, 0);                   // Move cursor to show temperature value
  sprintf(str, "%d", temperature);         // Convert temperature value to string
  OLED.print(str);                         // Display temperature on OLED
  OLED.show();                             // Update the OLED screen
  delay(100);                              // Delay before the next reading
}
