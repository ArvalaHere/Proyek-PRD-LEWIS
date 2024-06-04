#include <Wire.h>
#include <LiquidCrystal_I2C.h>  
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define buzzer 13 
#define yellowLED 12 
#define redLED 11

#define x A3 
#define y A2 
#define z A1 

int xsample = 0;
int ysample = 0;
int zsample = 0;
long start;
int buz = 0;
int yellowStatus = 0;
int redStatus = 0;

/*Macros*/
#define samples 9
#define maxVal 3000 
#define minVal -3000 
#define buzTime 2000 

void setup() {
    lcd.begin(); 
    Serial.begin(9600); 
    delay(1000);
    lcd.print("EarthQuake ");
    lcd.setCursor(0, 1);
    lcd.print("Detector ");
    delay(2000);
    lcd.clear();
    lcd.print("Calibrating.....");
    lcd.setCursor(0, 1);
    lcd.print("Please wait...");
    pinMode(buzzer, OUTPUT);
    pinMode(yellowLED, OUTPUT);
    pinMode(redLED, OUTPUT);
    buz = 0;
    digitalWrite(buzzer, buz);
    digitalWrite(yellowLED, buz);
    digitalWrite(redLED, buz);
    for (int i = 0; i < samples; i++) {
        xsample += analogRead(x);
        ysample += analogRead(y);
        zsample += analogRead(z);
    }

    xsample /= samples; 
    ysample /= samples; 
    zsample /= samples; 

    delay(3000);
    lcd.clear();
    lcd.print("Calibrated");
    delay(1000);
    lcd.clear();
    lcd.print("Device Ready");
    delay(1000);
    lcd.clear();
    lcd.print(" X      Y      Z ");
}

void loop() {
    int value1 = analogRead(x); 
    int value2 = analogRead(y); 
    int value3 = analogRead(z); 

    int xValue = xsample - value1; 
    int yValue = ysample - value2; 
    int zValue = zsample - value3; 

    lcd.setCursor(0, 1);
    lcd.print(xValue);
    lcd.setCursor(6, 1);
    lcd.print(yValue);
    lcd.setCursor(12, 1);
    lcd.print(zValue);
    delay(100);

    if (xValue < minVal || xValue > maxVal || yValue < minVal || yValue > maxVal || zValue < minVal || zValue > maxVal) {
        if (buz == 0) start = millis(); 
        buz = 1; 
        yellowStatus = 1;
        redStatus = 1;
    }

    if (buz == 1) {
        lcd.setCursor(0, 0);
        lcd.print("Earthquake Alert ");
    } else {
        lcd.clear();
        lcd.print(" X      Y      Z ");
    }

    if (millis() >= start + buzTime) {
        buz = 0;
        yellowStatus = 0;
        redStatus = 0;
    }

    digitalWrite(buzzer, buz); 
    digitalWrite(yellowLED, yellowStatus); 
    digitalWrite(redLED, redStatus);

    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command == "ALERT1") {
            buz = 1;
            yellowStatus = 1;
            redStatus = 0;
            start = millis();
        } else if (command == "ALERT2") {
            buz = 1;
            yellowStatus = 0;
            redStatus = 1;
            start = millis();
        } else if (command == "ALERT3") {
            buz = 1;
            yellowStatus = 1;
            redStatus = 1;
            start = millis();
        }
    }
}
