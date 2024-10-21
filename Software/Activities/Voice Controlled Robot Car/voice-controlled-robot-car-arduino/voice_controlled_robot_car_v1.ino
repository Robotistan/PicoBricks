void setup() {
  Serial1.begin(9600);
}

void loop() {
  if (Serial1.available() > 0) {
 
      char sread = Serial1.read();
      Serial.println(sread);
      
    if (sread == 'f') {
      Forward();
    } else if(sread == 'r'){
      Right();
    } else if(sread == 'l'){
      Left();
    } else if(sread == 's'){
      Stop();
    }
  }
}

void Forward(){
  digitalWrite(21,HIGH);
  digitalWrite(22,HIGH);
  delay(1000);
  digitalWrite(21,LOW);
  digitalWrite(22,LOW);
}

void Left(){
  digitalWrite(21,LOW);
  digitalWrite(22,HIGH);
  delay(500);
  digitalWrite(21,LOW);
  digitalWrite(22,LOW);
}

void Right(){
  digitalWrite(21,HIGH);
  digitalWrite(22,LOW);
  delay(500);
  digitalWrite(21,LOW);
  digitalWrite(22,LOW);
}

void Stop(){
  digitalWrite(21,LOW);
  digitalWrite(22,LOW);
  delay(1000);
}
