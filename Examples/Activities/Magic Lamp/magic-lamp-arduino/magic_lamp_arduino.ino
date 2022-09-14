int x=0; 

void setup() {
  // put your setup code here, to run once:
  pinMode(16,INPUT);//to access the hardware on the pico
  pinMode(12,OUTPUT);//initialize digital pin 16 as an INPUT for Sensor
  digitalWrite(12,LOW);//initialize digital pin 12 as an OUTPUT for Relay

}

void loop() {
  // put your main code here, to run repeatedly:
  
  //When sensor value is '0', the relay will be '1'
  if (digitalRead(16)==0){
    digitalWrite(12,HIGH);
    x=1;
  } else{
    digitalWrite(12,LOW);
    x=0;
  }


}
