#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); 
  }

}

void loop() {
  
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
  delay(5000);
  }

}
