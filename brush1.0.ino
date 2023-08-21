int enA = 9;
int in1 = 8;
int in2 = 7;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  randomSeed(analogRead(0));

  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  int randomNum = random(2);
  Serial.println(randomNum);

  analogWrite(enA, 255);
  for (int loopCount = 0; loopCount < 5; loopCount++) {
    if (randomNum == 0) {
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      delay(1000);
    } else {
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      delay(1000);
    }
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    delay(1000);
  }
}

void repeat(void (*action)()){
  for (int i = 0; i < 5; i++){
    loop();
  }
}

int main(){
  repeat(loop);
  return 0;
}
