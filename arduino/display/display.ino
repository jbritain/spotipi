#include <LiquidCrystal.h>


// initialize the library by associating any needed LCD interface pin

// with the arduino pin number it is connected to

String inputString;

// Rotary Encoder
#define encoderOutA 6 // CLK
#define encoderOutB 7 // DT
volatile int counter = 0;
volatile int encoderState;
volatile int previousEncoderState;

// LCD
#define registerSelect 12 // RS
#define enable 11 // E
#define d4 5
#define d5 4
#define d6 3
#define d7 2


LiquidCrystal lcd(registerSelect, enable, d4, d5, d6, d7);

void setup() {

  // Rotary Encoder
  pinMode(encoderOutA, INPUT);
  pinMode(encoderOutB, INPUT);
  previousEncoderState = digitalRead(encoderOutA);

  // LCD
  lcd.begin(16, 2);

  // Serial
  Serial.begin(115200);
  Serial.setTimeout(1);
}

String displayContents;
String input;

void loop() {
  // update display if necessary
  if (Serial.available()){
    input = Serial.readString();

    if(displayContents.length() >= 32){
      displayContents = "";
    }
    displayContents += input;
    lcd.setCursor(0, 0);
    lcd.print(displayContents.substring(0,16));
    lcd.setCursor(0, 1);
    lcd.print(displayContents.substring(16,32));
  }
  
  // send volume if necessary
  encoderState = digitalRead(encoderOutA);
  if (encoderState != previousEncoderState){
    if (digitalRead(encoderOutB) != encoderState){
      counter++;
    } else {
      counter--;
    }
    Serial.print(counter);
  };
  previousEncoderState = encoderState;
}

