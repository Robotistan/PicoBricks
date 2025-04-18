#include <picobricks.h>

// Define the pin for the RGB NeoPixel and LDR sensor
#define RGB_PIN  6           
#define LDR_PIN  27          

#define RGB_COUNT 1          // Number of RGB LEDs

int analogValue = 0;         // Variable to store LDR sensor reading

NeoPixel strip(RGB_PIN, RGB_COUNT);  // Initialize NeoPixel strip

void setup() 
{
  pinMode(LDR_PIN, INPUT);  // Set LDR pin as input
}

void loop() 
{
  analogValue = analogRead(LDR_PIN);  // Read light level from LDR sensor

  for (int i = 0; i < RGB_COUNT; i++)  // Loop through each LED (only 1 here)
  {
    if (analogValue > 200) {
      // If it's bright, turn on white light
      strip.setPixelColor(i, 255, 255, 255);  // White light
      delay(250); 
    } 
    else {
      // If it's dark, turn off the LED
      strip.setPixelColor(i, 0, 0, 0);  // Turn off LED
    }
  }

  strip.Show();  // Update the NeoPixel strip to reflect color changes
  delay(10);     // Small delay for stability
}
