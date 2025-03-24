
// Define stepper motor connections and steps per revolution:
// define dirPin = 2
// define stepPin = 3
// define stepsPerRevolution = 200

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  // clockwise:
  digitalWrite(dirPin, HIGH);
  for (int i = 0; i < 3 * stepsPerRevolution; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(2000);
  }
  delay(3000);

  // counterclockwise:
  digitalWrite(dirPin, LOW);
  for (int i = 0; i < 3 * stepsPerRevolution; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(1000);
  }
  delay(10000);
