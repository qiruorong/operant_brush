int enA = 9;
int in1 = 8;
int in2 = 7;
unsigned long stimTimestamps[100];

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
  analogWrite(enA, 255);
  for (int i = 0; i < 100; i++) {
    int randomNum = random(2); // Generate a new random number for each iteration
    Serial.println(randomNum);
    stimTimestamps[i] = millis();
    Serial.println(stimTimestamps[i]);
    
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
