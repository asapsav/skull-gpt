const int ledPin_left = 7;
const int ledPin_right = 12;
const int motorPin = 9;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin_left, OUTPUT);
  pinMode(ledPin_right, OUTPUT);
  pinMode(motorPin, OUTPUT);
  Serial.println("READY");
}

void blinkOnce() {
  digitalWrite(ledPin_left, HIGH);
  digitalWrite(ledPin_right, HIGH);
  digitalWrite(motorPin, HIGH);
  delay(200);
  digitalWrite(ledPin_left, LOW);
  digitalWrite(ledPin_right, LOW);
  digitalWrite(motorPin, LOW);
  delay(200);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    
    switch (command) {
      case '1':
        digitalWrite(ledPin_left, HIGH);
        digitalWrite(ledPin_right, HIGH);
        digitalWrite(motorPin, HIGH);
        break;
        
      case '0':
        digitalWrite(ledPin_left, LOW);
        digitalWrite(ledPin_right, LOW);
        digitalWrite(motorPin, LOW);
        break;

      case 's':  // Custom sequence
        blinkOnce();
        blinkOnce();
        blinkOnce();
        delay(500); // Pause
        blinkOnce();
        blinkOnce();
        delay(500); // Pause
        blinkOnce();
        blinkOnce();
        blinkOnce();
        delay(500); // Pause
        blinkOnce();
        blinkOnce();
        break;
        
      default:
        // Unsupported command, do nothing
        break;
    }
  } 
}
