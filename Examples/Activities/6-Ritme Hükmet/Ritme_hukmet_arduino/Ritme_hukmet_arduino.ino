void setup() {
  // put your setup code here, to run once:
   Wire.begin();  
  oled.init();                      
  oled.clearDisplay();              

  pinMode(buzzer,OUTPUT);
  pinMode(26,INPUT);
  pinMode(button,INPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
  int rithm = (analogRead(pot))/146;
  String char_rithm = String(rithm);
  oled.setTextXY(3,4);              
  oled.putString("Speed: ");
  oled.setTextXY(3,10);              
  oled.putString(char_rithm);

  delay(10);

  if (digitalRead(button) == 1){

    oled.clearDisplay(); 
    oled.setTextXY(3,2);              
    oled.putString("Now playing...");

    tone(buzzer, La); delay (1000/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Fa); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (500/(rithm+1));
    tone(buzzer, Re); delay (500/(rithm+1));
    tone(buzzer, Fa); delay (500/(rithm+1));
    tone(buzzer, Mi); delay (1000/(rithm+1));

    oled.clearDisplay();
  }
  noTone(buzzer);

  

}
