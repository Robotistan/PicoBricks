void actived (){
  digitalWrite(7,1);
  while(!(digitalRead(14) == 1))
  {
    _loop();
  }
  motion_detected();
}

void motion_detected (){
  while(1) {
      // buzzer settings 
      tone(20,262,0.25*1000);
      delay(0.25*1000);
      tone(20,330,0.25*1000);
      delay(0.25*1000);
      tone(20,262,0.25*1000);
      delay(0.25*1000);
      tone(20,349,0.25*1000);
      delay(0.25*1000);
// sound the buzzer when PIR detected a motion 
      _loop();
  }
}

void _delay(float seconds) {
  long endTime = millis() + seconds * 1000;
  while(millis() < endTime) _loop();
}

void _loop() {
}

void loop() {
  _loop();
}

void setup() {
  
  pinMode(10,INPUT);
  pinMode(1,INPUT);
  pinMode(20,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(14,INPUT);
  // define input and output pins
  
  while(1) {
      if(digitalRead(10) == 1){
          _delay(3);
          actived();
      }
      if(digitalRead(1) == 1){
          while(!(digitalRead(10) == 1))
          {
            _loop();
            tone(20,349,0.5*1000);
            delay(0.5*1000);
            digitalWrite(7,1);
            _delay(0.5);
            tone(20,392,0.5*1000);
            delay(0.5*1000);
            digitalWrite(7,0);
            _delay(0.5);
          }
      }
      _loop();
  }
}
