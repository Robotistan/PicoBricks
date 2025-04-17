void setup() {
  pinMode(7,OUTPUT);//initialize digital pin 7 as an output
  pinMode(10,INPUT);//initialize digital pin 10 as an input
}

void loop() {
  if(digitalRead(10)==1){//check the button and if it is on
    digitalWrite(7,HIGH);//turn the LED on by making the voltage HIGH
  }
  else{
    digitalWrite(7,LOW);//turn the LED off by making the voltage LOW 
  }
  delay(10);//wait for half second
}
