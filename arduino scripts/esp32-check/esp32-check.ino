void setup() {
  pinMode(2, OUTPUT); // Set GPIO2 as an output
}

void loop() {
  digitalWrite(2, HIGH); // Turn the LED on
  delay(1000);           // Wait for a second
  digitalWrite(2, LOW);  // Turn the LED off
  delay(1000);           // Wait for a second
}
