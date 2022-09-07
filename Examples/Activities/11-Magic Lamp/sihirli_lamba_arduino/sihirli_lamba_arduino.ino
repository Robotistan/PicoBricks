int x=0; 

void setup() {
  // put your setup code here, to run once:
  pinMode(16,INPUT);
  pinMode(12,OUTPUT);
  digitalWrite(12,LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(16)==0){
    digitalWrite(12,HIGH);
    x=1;
  } else{
    digitalWrite(12,LOW);
    x=0;
  }


}
