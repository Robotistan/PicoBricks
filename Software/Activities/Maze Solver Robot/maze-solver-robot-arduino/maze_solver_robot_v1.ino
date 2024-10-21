#define trigPin  15
#define echoPin     14
#define MAX_DISTANCE 400

long distance = 0;
long duration = 0;

int hcsr(){
  long dis, dur;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  dur = pulseIn(echoPin, HIGH);
  dis = (dur/2) / 29.1;
  return dis;
}

void setup() {
  pinMode(21,OUTPUT);
  pinMode(22,OUTPUT); //define dc motor pins
}

void loop() {
  delay(50);
  distance = hcsr();
  Forward();
  if(distance<5){
    Stop();
    delay(1000);
    Right();
    delay(1000);
    distance = hcsr();
    if(distance < 5){
      Stop();
      delay(1000);
      Left();
      delay(500);
      // If the distance is less than 5, wait, turn right; if the distance is less than 5 again, move in the opposite direction
    }
  }
}

void Forward(){   //if the distance is higher than 5, go straight
  digitalWrite(21,HIGH);
  digitalWrite(22,HIGH); 
}
void Left(){     //turn left
  digitalWrite(21,LOW);
  digitalWrite(22,HIGH);
}
void Right(){   //turn right
  digitalWrite(21,HIGH);
  digitalWrite(22,LOW);  
}
void Stop(){
  digitalWrite(21,LOW);
  digitalWrite(22,LOW); 
}
