const int EYE_PIN     = 2;
const int ALCOHOL_PIN = A0;
const int BUZZER_PIN  = 8;
const int RELAY_PIN   = 7;

void setup() {
  Serial.begin(9600);
  pinMode(EYE_PIN,    INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RELAY_PIN,  OUTPUT);

  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(BUZZER_PIN, LOW);

  Serial.println("Arduino Ready!");
}

void loop() {
  Serial.print("EYE:");
  Serial.println(digitalRead(EYE_PIN));

  Serial.print("ALCOHOL:");
  Serial.println(analogRead(ALCOHOL_PIN));

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if      (cmd == "BUZZER_ON")  digitalWrite(BUZZER_PIN, HIGH);
    else if (cmd == "BUZZER_OFF") digitalWrite(BUZZER_PIN, LOW);
    else if (cmd == "STOP")       digitalWrite(RELAY_PIN,  LOW);
    else if (cmd == "START")      digitalWrite(RELAY_PIN,  HIGH);
  }

  delay(100);
}
