void setup() {
  // put your setup code here, to run once:
  pinMode (7,OUTPUT);
  pinMode (26,INPUT);
  Serial.begin(9600);


}

void loop() {
  // put your main code here, to run repeatedly:
  int pot_val = analogRead(26);
  int led_val = map(pot_val, 0, 1023, 0, 255);
  digitalWrite(7, led_val);
  Serial.println(led_val);
  delay(100);


}
