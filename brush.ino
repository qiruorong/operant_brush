#include <AFMotor.h>
AF_DCMotor motor(1);
int enA = 9;
int in1 = 8;
int in2 = 7;

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
    motor.run(FORWARD);
  } else {
    motor.run(BACKWARD);
  }
  delay(2000);
}
