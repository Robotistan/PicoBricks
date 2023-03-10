/*Ferris Wheel*/
#define pot 26
#define motor 21

void setup() {
  Serial.begin(115200);
  pinMode(motor, OUTPUT);
  pinMode(pot, INPUT);
}

void loop() {
  int pot_value = analogRead(pot);

  if (pot_value > 150) {
    analogWrite(motor, pot_value);
  }
  else {
    analogWrite(motor, LOW);
  }
Serial.println(pot_value);
}
