#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int taster = 7;
int tasterstatus = 0;
String deleteStatus = "false";

char ssid[] = "#########";
char pass[] = "#########";

WiFiClient WiFiClient;
MqttClient mqttClient(WiFiClient);

const char broker[] = "192.168.2.188"; // Address of the MQTT server
int        port     = 1883;
const char topic[]  = "arduino/barcode";
const char topic_del[]  = "arduino/delete";

void setup() {

  Serial.begin(9600);
  Serial1.begin(9600);

  pinMode(taster, INPUT_PULLUP);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); 
  }

  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);
  while (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
  }
  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

}

void loop() {

  tasterstatus=digitalRead(taster);

  if (tasterstatus == 0){ 
    deleteStatus = "true";
    Serial.println("Taster AN");
    delay(500);
  }
  else deleteStatus = "false";
  
  String buffer = "";
  char input = ' ';
  
  display.clearDisplay();
  display.setCursor(0, 0); //oled display
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.print("Bitte Code scannen");
  display.display();
  delay(500);
 
  if(Serial1.available()){
    display.clearDisplay();
    display.setCursor(0, 0);
    delay(5);
 
    while (Serial1.available()) {  
      input = Serial1.read();
      buffer = buffer + input;
      delay(5);
    }
    
  display.print(buffer);
  display.display();
  delay(1000);
  String barcode = String(buffer);

  mqttClient.beginMessage(topic);
  mqttClient.print(barcode);
  mqttClient.endMessage();
  mqttClient.beginMessage(topic_del);
  mqttClient.print(deleteStatus);
  mqttClient.endMessage();
  Serial.println("Sent MQTT message.");

  }

}
