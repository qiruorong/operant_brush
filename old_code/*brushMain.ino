int enA = 9;
int in1 = 8;
int in2 = 7;
int stimulusPinIn = A1;
int stimulusPinOut = 12;
unsigned long stimTimestamps[100];
bool stimulusActive = false;


void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(stimulusPinIn, INPUT); 
  pinMode(stimulusPinOut, OUTPUT); 
  randomSeed(analogRead(0));
  Serial.begin(9600); 
}

void loop() {
  if (digitalRead(stimulusPinIn)) {
    stimulusActive = true;
    analogWrite(enA, 255);
    for (int i = 0; i < 100; i++) {
      int randomNum = random(2); 
      Serial.println(randomNum);
      stimTimestamps[i] = millis();
      Serial.println(stimTimestamps[i]);
      
      if (randomNum == 0) {
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        analogWrite(stimulusPinOut, 255); 
      } else {
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        analogWrite(stimulusPinOut, 255); 
      }

      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      delay(1000);
    } 
  }
}
