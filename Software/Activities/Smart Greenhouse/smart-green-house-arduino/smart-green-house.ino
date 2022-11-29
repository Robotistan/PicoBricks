#include <DHT.h>
#define RX 0
#define TX 1

#define LIMIT_TEMPERATURE     30 // will be change
#define DHTPIN                11
#define DHTTYPE               DHT11
#define smo_sensor            27
#define motor                 22
#define DEBUG true

DHT dht(DHTPIN, DHTTYPE);
float temperature;

int connectionId;

void setup() {
  // Connect wifi gibi bir kere calisacak kodlari buraya alabilirsiniz

  Serial1.begin(115200);
  dht.begin();
  pinMode(smo_sensor, INPUT);
  pinMode(motor, OUTPUT);

  sendData("AT+RST\r\n", 2000, DEBUG); // reset module
  sendData("AT+GMR\r\n", 2000, DEBUG); // configure as access point
  sendData("AT+CIPSERVER=0\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+RST\r\n", 2000, DEBUG); // configure as access point
  sendData("AT+RESTORE\r\n", 2000, DEBUG); // configure as access point
  sendData("AT+CWMODE?\r\n", 2000, DEBUG); // configure as access point
  sendData("AT+CWMODE=1\r\n", 2000, DEBUG); // configure as access point
  sendData("AT+CWMODE?\r\n", 2000, DEBUG); // configure as access point
  sendData("AT+CWJAP=\"MSI\",\"11223344\"\r\n", 5000, DEBUG); // configure as access point
  delay(3000);
  sendData("AT+CIFSR\r\n", 1000, DEBUG); // get ip address
  delay(3000);
  sendData("AT+CIPMUX=1\r\n", 1000, DEBUG); // configure for multiple connections
  delay(1000);
  sendData("AT+CIPSERVER=1,80\r\n", 1000, DEBUG); // turn on server on port 80
  delay(1000);

}

void loop() {

  if (Serial1.find("+IPD,")) {
    delay(300);
    connectionId = Serial1.read() - 48;
    if (Serial1.find("/WATERING")) {
      Serial.println("Irrigation Start");
      digitalWrite(motor, HIGH);
      delay(10000); // 10 sec.
      digitalWrite(motor, LOW);
      Serial.println("Irrigation Finished");

      Serial.println("! Incoming connection - sending webpage");
      String html = "";
      html += "<html>";
      html += "<body><center><H1>Irrigation Complete.<br/></H1></center>";
      html += "</body></html>";
      espsend(html);
    }
    if (Serial1.find("/SERA")) {
      //delay(1000);
      temperature = dht.readTemperature();
      Serial.print("Temp: ");
      Serial.println(temperature);

      Serial.println("! Incoming connection - sending webpage");
      String html = "";
      html += "<html>";
      html += "<body><center><H1>TEMPERATURE<br/></H1></center>";
      html += "<center><H2>";
      html += (String)temperature;
      html += "<br/></H2></center>";
      html += "</body></html>";
      espsend(html);
    }

    Serial.println("! Incoming connection - sending webpage");
    String html = "";
    html += "<html>";
    html += "<body><center><H1>CONNECTED.<br/></H1></center>";
    html += "<center><h4>INFO:Get Sensor Data</br>WATERING:Run Water Pump</h4></center>";
    html += "</body></html>";
    espsend(html);

    String closeCommand = "AT+CIPCLOSE=";  ////////////////close the socket connection////esp command
    closeCommand += connectionId; // append connection id
    closeCommand += "\r\n";
    sendData(closeCommand, 3000, DEBUG);
  }

}


//////////////////////////////sends data from ESP to webpage///////////////////////////

void espsend(String d)
{
  String cipSend = " AT+CIPSEND=";
  cipSend += connectionId;
  cipSend += ",";
  cipSend += d.length();
  cipSend += "\r\n";
  sendData(cipSend, 1000, DEBUG);
  sendData(d, 1000, DEBUG);
}

//////////////gets the data from esp and displays in serial monitor///////////////////////
String sendData(String command, const int timeout, boolean debug)
{
  String response = "";
  Serial1.print(command);
  long int time = millis();
  while ( (time + timeout) > millis())
  {
    while (Serial1.available())
    {
      char c = Serial1.read(); // read the next character.
      response += c;
    }
  }

  if (debug)
  {
    Serial.print(response); //displays the esp response messages in arduino Serial monitor
  }
  return response;
}
