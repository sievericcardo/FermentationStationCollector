//Libraries
#include <DHT.h>;
#include "MQ135.h" 

// PINS
#define MQPIN 0
#define DHTPIN0 11
#define DHTPIN1 14
#define RELAYPIN0 7
#define RELAYPIN1 3

#define DHTTYPE DHT22   // DHT 22  (AM2302)

DHT dht0(DHTPIN0, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
DHT dht1(DHTPIN1, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
MQ135 mq = MQ135(MQPIN); 

int delay = 1;

void setup() {
  Serial.begin(9600);
	dht0.begin();
  dht1.begin();

  // Relay is LOW activated!!!
  digitalWrite(RELAYPIN0, HIGH);
  digitalWrite(RELAYPIN1, HIGH);
}

// Relay movement
// Relay is LOW activated!!!
// TODO think about this again...
void move_relay(int relay, int duration){
  digitalWrite(relay, LOW);
  delay(delay);
  digitalWrite(relay1, HIGH);
}

// Helper function to write value triple to commandline
void write_line(String type, int id, float value){
  Serial.print(type)
  Serial.print(',')
  Serial.print(int)
  Serial.print(',')
  Serial.println(value)
}

void loop() {
  write_line("h", DHTPIN0, dht0.readHumidity());
  write_line("t", DHTPIN0, dht0.readTemperature());

  write_line("h", DHTPIN1, dht1.readHumidity());
  write_line("t", DHTPIN1, dht1.readTemperature());

  write_line("g", MQPIN, mq.getRZero())
  delay(delay);
}
