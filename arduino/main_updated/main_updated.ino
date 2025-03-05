//Libraries
#include <DHT.h>;
#include "MQ135.h" 

// PINS
#define MQPIN 0
#define DHTPIN0 13
#define DHTPIN1 12
#define RELAYPIN0 7
#define RELAYPIN1 3

#define DHTTYPE DHT22   // DHT 22  (AM2302)

DHT dht0(DHTPIN0, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
DHT dht1(DHTPIN1, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
MQ135 mq = MQ135(MQPIN); 

int iteration_delay = 1;

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
  delay(duration);
  digitalWrite(relay1, HIGH);
}

// Helper function to write value triple to commandline
void write_line(String type, int id, float value){
  Serial.print(type);
  Serial.print(',');
  Serial.print(id);
  Serial.print(',');
  Serial.println(value);
}

void loop() {
  write_line("H", DHTPIN0, dht0.readHumidity());
  write_line("T", DHTPIN0, dht0.readTemperature());

  write_line("H", DHTPIN1, dht1.readHumidity());
  write_line("T", DHTPIN1, dht1.readTemperature());

  write_line("G", MQPIN, mq.getRZero())
  delay(iteration_delay);
}
