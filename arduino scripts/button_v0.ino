int buttonPin = 2;

void setup() {
  pinMode(buttonPin, OUTPUT);
  digitalWrite(buttonPin, LOW); // Ensure the "button" is not pressed at startup
  Serial.begin(9600); // Start serial communication for computer interface
}

void loop() {
  if (Serial.available()) { // Check if there's incoming data from the computer
    char command = Serial.read();
    if (command == 'P') { // If the computer sends a 'P' character, "press" the button
      digitalWrite(buttonPin, HIGH); // "Press" the TRYME button
      delay(100); // Mimic a button press duration
      digitalWrite(buttonPin, LOW); // "Release" the button
    }
  }
}
