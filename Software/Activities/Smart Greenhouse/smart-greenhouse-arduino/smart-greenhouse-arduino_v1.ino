#include <picobricks.h>

// Define pins
#define RX_PIN 0          // Serial RX pin for ESP module
#define TX_PIN 1          // Serial TX pin for ESP module
#define DHT_PIN 11        // DHT11 sensor data pin
#define MOTOR_2 22        // Pin for water pump or irrigation motor
#define LDR_PIN 27        // LDR analog input pin

#define LIMIT_TEMPERATURE 30   // Temperature threshold
#define DEBUG true             // Enable or disable debug output

int connectionId;              // Holds the ID of the incoming client connection

DHT11 dht(DHT_PIN);            // Create DHT sensor object

void setup() {
  Serial1.begin(115200);       // Start communication with ESP WiFi module
  dht.begin();                 // Initialize DHT sensor
  pinMode(LDR_PIN, INPUT);
  pinMode(MOTOR_2, OUTPUT);

  // ESP AT command sequence for WiFi initialization
  sendData("AT+RST\r\n", 2000, DEBUG);                      // Reset the module
  sendData("AT+GMR\r\n", 1000, DEBUG);                      // Get firmware version
  sendData("AT+CIPSERVER=0\r\n", 1000, DEBUG);              // Disable previous server
  sendData("AT+RST\r\n", 1000, DEBUG);                      // Reset again
  sendData("AT+RESTORE\r\n", 1000, DEBUG);                  // Restore default settings
  sendData("AT+CWMODE?\r\n", 1000, DEBUG);                  // Check WiFi mode
  sendData("AT+CWMODE=1\r\n", 1000, DEBUG);                 // Set mode to STA (Station)
  sendData("AT+CWMODE?\r\n", 1000, DEBUG);                  // Confirm mode
  sendData("AT+CWJAP=\"WIFI_ID\",\"WIFI_PASSWORD\"\r\n", 5000, DEBUG); // Connect to WiFi
  delay(3000);
  sendData("AT+CIFSR\r\n", 1000, DEBUG);                    // Get IP address
  delay(3000);
  sendData("AT+CIPMUX=1\r\n", 1000, DEBUG);                 // Enable multiple connections
  delay(1000);
  sendData("AT+CIPSERVER=1,80\r\n", 1000, DEBUG);           // Start server on port 80
  delay(1000);
}

void loop() {
  // Check if ESP has received data from a client
  if (Serial1.find("+IPD,")) {
    delay(300);
    connectionId = Serial1.read() - 48;                     // Get connection ID
    String serialIncoming = Serial1.readStringUntil('\r');  // Read incoming request
    Serial.print("SERIAL_INCOMING:");
    Serial.println(serialIncoming);

    // If client requests watering action
    if (serialIncoming.indexOf("/WATERING") > 0) {
      Serial.println("Irrigation Start");
      digitalWrite(MOTOR_2, HIGH);      // Start water pump
      delay(1000);                      // Run for 1 second
      digitalWrite(MOTOR_2, LOW);       // Stop water pump
      Serial.println("Irrigation Finished");

      // Send webpage response
      String html = "";
      html += "<html><body><center><H1>Irrigation Complete.<br/></H1></center></body></html>";
      espsend(html);
    }

    // If client requests greenhouse status (SERA)
    if (serialIncoming.indexOf("/SERA") > 0) {
      delay(300);

      float smo = analogRead(LDR_PIN);                               // Read LDR value
      float smopercent = (460 - smo) * 100.0 / 115.0;                // Convert to %
      Serial.print("SMO: %");
      Serial.println(smo);

      float temperature = dht.readTemperature();                     // Read temperature
      Serial.print("Temp: ");
      Serial.println(temperature);

      float humidity = dht.readHumidity();                           // Read humidity
      Serial.print("Hum: ");
      Serial.println(humidity);
      
      // Generate HTML response with sensor data
      String html = "";
      html += "<html><body><center><H1>TEMPERATURE<br/></H1></center><center><H2>";
      html += (String)temperature + " C<br/></H2>";
      html += "<center><H1>HUMIDITY<br/></H1></center><center><H2>";
      html += (String)humidity + "%<br/></H2>";
      html += "<center><H1>SMO<br/></H1></center><center><H2>";
      html += (String)smopercent + "%<br/></H2></center></body></html>";
      
      espsend(html);
    }
    else {
      // Default home page
      Serial.println("! Incoming connection - sending MAIN webpage");
      String html = "";
      html += "<html><body><center><H1>CONNECTED.<br/></H1></center>";
      html += "<center><a href='/SERA'><h4>INFO: Get Sensor Data</a></br>";
      html += "<a href='/WATERING'>WATERING: Run Water Pump</a></h4></center>";
      html += "</body></html>";
      espsend(html);
    }

    // Close client connection
    String closeCommand = "AT+CIPCLOSE=";
    closeCommand += connectionId;
    closeCommand += "\r\n";
    sendData(closeCommand, 3000, DEBUG);
  }
}

// Function to send HTML or command strings to ESP via Serial
void espsend(String d)
{
  String cipSend = "AT+CIPSEND=";
  cipSend += connectionId;
  cipSend += ",";
  cipSend += d.length();
  cipSend += "\r\n";

  sendData(cipSend, 1000, DEBUG);  // Send AT+CIPSEND command
  sendData(d, 1000, DEBUG);        // Send the actual data
}

// Function to send AT commands and return ESP response
String sendData(String command, const int timeout, boolean debug)
{
  String response = "";
  Serial1.print(command);          // Send command to ESP
  long int time = millis();
  while ((time + timeout) > millis())
  {
    while (Serial1.available())
    {
      char c = Serial1.read();     // Read characters from ESP response
      response += c;
    }
  }

  if (debug) {
    Serial.print(response);        // Print response to Serial Monitor
  }
  return response;
}
