void setup() {
  // put your setup code here, to run once:
  pinMode(1,INPUT);
  pinMode(7,OUTPUT);
  //define the input and output pins
}

void loop() {
  // put your main code here, to run repeatedly:
  
  
  Serial.println(digitalRead(1));

  if(digitalRead(1)==1){
    digitalWrite(7,HIGH);
    delay(3000);
  }
  else{
    digitalWrite(7,LOW);
    delay(1000);
  }
}
