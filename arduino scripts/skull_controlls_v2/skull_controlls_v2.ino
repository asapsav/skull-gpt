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
  delay(100);
  digitalWrite(ledPin_left, LOW);
  digitalWrite(ledPin_right, LOW);
  digitalWrite(motorPin, LOW);
  delay(100);
}


bool runCustomSequence = false;

void loop() {
  if (runCustomSequence) {
      // Custom sequence
      blinkOnce();
      blinkOnce();
      blinkOnce();
      delay(200);
      blinkOnce();
      blinkOnce();
    }
    
  if (Serial.available()) {
    char command = Serial.read();
    
    if (command == 's') {
      runCustomSequence = false;
    } else if (command == 'g') {
      delay(1500); //delay 1 sec for elevel labs API to propagate
      runCustomSequence = true;
    }
    
    else {
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
          
        default:
          // Unsupported command, do nothing
          break;
      }
    }
  }
}
