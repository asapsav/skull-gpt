const int RIGHT_EYE_LED_PIN = 12;
const int LEFT_EYE_LED_PIN = 7;

void setup() {
  pinMode(RIGHT_EYE_LED_PIN, OUTPUT);
  pinMode(LEFT_EYE_LED_PIN, OUTPUT);// initialize the digital pin 13 as an output
}

void loop() {
  digitalWrite(RIGHT_EYE_LED_PIN, HIGH); // turn the LED on
  digitalWrite(LEFT_EYE_LED_PIN, HIGH);
  delay(1000);            // wait for a second
  digitalWrite(RIGHT_EYE_LED_PIN, LOW);
  digitalWrite(LEFT_EYE_LED_PIN, LOW);// turn the LED off
  delay(1000);            // wait for a second
}
