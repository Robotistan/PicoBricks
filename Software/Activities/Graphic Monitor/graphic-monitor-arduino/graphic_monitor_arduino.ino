void setup() {
  // put your setup code here, to run once:
  pinMode (7,OUTPUT);//initialize digital pin 7 as an output
  pinMode (26,INPUT);//initialize digital pin 26 as an input
  Serial.begin(9600);//start serial communication


}

void loop() {
  // put your main code here, to run repeatedly:
  int pot_val = analogRead(26);
  int led_val = map(pot_val, 0, 1023, 0, 255);
  analogWrite(7, led_val);
  Serial.println(led_val);
  //trun on the LED according to the value from the potentiometer
  
  delay(100);//wait


}
