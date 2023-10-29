const int motorPin = 9; // Connect motor control to digital pin 9

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 bps
  pinMode(motorPin, OUTPUT); // Set the motor pin as output
}

void loop() {
  if (Serial.available()) {  // Check if data is available to read
    char command = Serial.read(); // Read the first character

    switch (command) {
      case '1':
        digitalWrite(motorPin, HIGH);  // Turn on the motor
        break;

      case '0':
        digitalWrite(motorPin, LOW);  // Turn off the motor
        break;

      default:
        // If an unsupported command is received, do nothing.
        break;
    }
  }
}
