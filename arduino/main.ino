/* How to use the DHT-22 sensor with Arduino uno
   Temperature and humidity sensor
   More info: http://www.ardumotive.com/how-to-use-dht-22-sensor-en.html
   Dev: Michalis Vasilakis // Date: 1/7/2015 // www.ardumotive.com */

//Libraries
#include <DHT.h>;
#include "MQ135.h" 

//Constants
#define DHTPIN 13     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
#define DHTPIN1 121    // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino


DHT dht1(DHTPIN1, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

MQ135 gasSensor = MQ135(11); 

//Variables
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value
float hum1;  //Stores humidity value
float temp1; //Stores temperature value

void setup()
{
  Serial.begin(9600);
	dht.begin();
  dht1.begin();
}

void loop()
{
    //Read data and store it to variables hum and temp
    hum = dht.readHumidity();
    temp = dht.readTemperature();
    hum1 = dht1.readHumidity();
    temp1 = dht1.readTemperature();
    //Print temp and humidity values to serial monitor
    Serial.print("Board 1 ");
    Serial.print("Humidity: ");
    Serial.print(hum);
    Serial.print(" %, Temp: ");
    Serial.print(temp);
    Serial.println(" Celsius");

    Serial.print(hum - 80);
    Serial.print(",");
    Serial.print(temp - 30);
    Serial.println();

    Serial.print("Board 2 ");
    Serial.print("Humidity: ");
    Serial.print(hum1);
    Serial.print(" %, Temp: ");
    Serial.print(temp1);
    Serial.println(" Celsius");
    delay(20000); //Delay 2 sec.

    // float rzero = gasSensor.getRZero();
    // Serial.print("Gas ");
    // Serial.println(rzero);
    // delay(1000);
}

   