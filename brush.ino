const int motorPin1 = 9;  // Motor control pin 1
const int motorPin2 = 10; // Motor control pin 2

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  randomSeed(analogRead(0));  // Seed the random number generator
  
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  int randomNum = random(2); // Generate a random number: 0 or 1
  
  // Send the random number to the computer via serial communication
  Serial.println(randomNum);

  if (randomNum == 0) {
    // Turn the motor in one direction
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
  } else {
    // Turn the motor in the other direction
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
  }

  delay(2000); // Wait for 2 seconds before changing direction
}
