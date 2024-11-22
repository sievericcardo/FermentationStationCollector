int relay1 = 7;
int relay2 = 3;

void setup() {
  Serial.begin(9600);
  
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  digitalWrite(relay1, HIGH);
  digitalWrite(relay2, HIGH);
}

void loop() {
// Relay is LOW activated!!!

  digitalWrite(relay1, LOW);
  delay(100);
  digitalWrite(relay2, HIGH);
  Serial.println("Relay 2");
  delay(9000);

  digitalWrite(relay2, LOW);
  delay(100);
  digitalWrite(relay1, HIGH);
  Serial.println("Relay 1");
  delay(9000);

  digitalWrite(relay1, HIGH);
  digitalWrite(relay2, HIGH);
  delay(3000);
}