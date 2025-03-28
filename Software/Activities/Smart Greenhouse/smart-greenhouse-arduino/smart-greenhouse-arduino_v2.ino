#include <Wire.h>

#define RX 0
#define TX 1

#define LIMIT_TEMPERATURE     30
#define smo_sensor            27
#define DEBUG true

int connectionId;

void dc(int dcNumber, int speed, int direction){
  Wire.beginTransmission(0x22);
  Wire.write(0x26);   
  Wire.write(dcNumber); 
  Wire.write(speed);   
  Wire.write(direction);   
  int cs = dcNumber ^ speed ^ direction;
  Wire.write(cs); 
  Wire.endTransmission();
}

void shtc_init(){
  Wire.beginTransmission(0x70);
  Wire.write(0x35);   
  Wire.write(0x17); 
  Wire.endTransmission();
  delay(500);
  Wire.beginTransmission(0x70);
  Wire.write(0xEF);   
  Wire.write(0xC8); 
  Wire.endTransmission();
  delay(500);
  Wire.requestFrom(0x70, 3);  
}

float temperature(){
  int rcv1 = 0;
  int rcv2 = 0;
  Wire.beginTransmission(0x70);
  Wire.write(0x78);   
  Wire.write(0x66); 
  Wire.endTransmission();
  delay(100);
  Wire.requestFrom(0x70, 2); 
  while(Wire.available()) {
    rcv1 = Wire.read();
    rcv2 = Wire.read();
  }
  delay(100);
  float temp = (((4375 * ((rcv1 << 8) | rcv2)) >> 14) - 4500) / 100;
  return temp;
}

float humidity(){
  int rcv1 = 0;
  int rcv2 = 0;
  Wire.beginTransmission(0x70);
  Wire.write(0x78);   
  Wire.write(0x66); 
  Wire.endTransmission();
  delay(100);
  Wire.requestFrom(0x70, 2); 
  while(Wire.available()) {
    rcv1 = Wire.read();
    rcv2 = Wire.read();
  }
  delay(100);
  return (((4375 * ((rcv1 << 8) | rcv2)) >> 14) - 4500) / 100;
}

void setup() {
  Serial1.begin(115200);
  pinMode(smo_sensor, INPUT);
  shtc_init();

  sendData("AT+RST\r\n", 2000, DEBUG); // reset module
  sendData("AT+GMR\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+CIPSERVER=0\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+RST\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+RESTORE\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+CWMODE?\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+CWMODE=1\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+CWMODE?\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+CWJAP=\"WIFI_ID\",\"WIFI_PASSWORD\"\r\n", 5000, DEBUG); // ADD YOUR OWN WIFI ID AND PASSWORD
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
    String serialIncoming = Serial1.readStringUntil('\r');
    Serial.print("SERIAL_INCOMING:");
    Serial.println(serialIncoming);

    if (serialIncoming.indexOf("/WATERING") > 0) {
      Serial.println("Irrigation Start");
      dc(1,255,1);
      delay(1000); // 10 sec.
      dc(1,0,1);
      Serial.println("Irrigation Finished");
      Serial.println("! Incoming connection - sending WATERING webpage");
      String html = "";
      html += "<html>";
      html += "<body><center><H1>Irrigation Complete.<br/></H1></center>";
      html += "</body></html>";
      espsend(html);
    }
    if (serialIncoming.indexOf("/SERA") > 0) {
      delay(300);

      float smo = analogRead(smo_sensor);
      float smopercent = (460-smo)*100.0/115.0 ; //min ve max değerleri değişken.
      Serial.print("SMO: %");
      Serial.println(smo);

      float temp = temperature();
      Serial.print("Temp: ");
      Serial.println(temp);

      float hum = humidity();
      Serial.print("Hum: ");
      Serial.println(hum);
      
      Serial.println("! Incoming connection - sending SERA webpage");
      String html = "";
      html += "<html>";
      html += "<body><center><H1>TEMPERATURE<br/></H1></center>";
      html += "<center><H2>";
      html += (String)temp;
      html += " C<br/></H2></center>";

      html += "<body><center><H1>HUMIDITY<br/></H1></center>";
      html += "<center><H2>";
      html += (String)hum;
      html += "%<br/></H2></center>";  
      
      html += "<body><center><H1>SMO<br/></H1></center>";
      html += "<center><H2>";
      html += (String)smopercent;
      html += "%<br/></H2></center>";  
          
      html += "</body></html>";
      espsend(html);
    }
    else
      Serial.println("! Incoming connection - sending MAIN webpage");
    String html = "";
    html += "<html>";
    html += "<body><center><H1>CONNECTED.<br/></H1></center>";
    html += "<center><a href='/SERA'><h4>INFO:Get Sensor Data</a></br><a href='/WATERING'>WATERING:Run Water Pump</a></h4></center>";
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
