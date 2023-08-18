#include <AFMotor.h>
AF_DCMotor motor(1);
int enA = 9;
int in1 = 5;
int in2 = 4;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
  motor.setSpeed(100); // 0-255
  randomSeed(analogRead(0)); 

  Serial.begin(9600);
}

void loop() {
  int randomNumber = random(2); 
  if (randomNumber == 0) {
    digitalWrite(in1, HIGH);
	  digitalWrite(in2, LOW);
  } else {
    digitalWrite(in1, LOW);
	  digitalWrite(in2, HIGH);
  }
  delay(2000);	
	// Now turn off motors
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
}
