#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); //sesuaikan dengan format lcd(alamat I2c, Dimensi Horizontal LCD, Dimensi Vertikal LCD)

//Buzzer untuk alarm dan led untuk Lampu LED 
//Sesuaikan penggunaan alarm dan LED serta port pada arduino
//format #define buzzer/led(number) port
#define buzzer1 13
#define buzzer2 12
#define led1 11 
#define led2 10 

//x, y, z adalah bagian dari accelerometer
#define x A0 
#define y A1 
#define z A2 

int xsample = 0;
int ysample = 0;
int zsample = 0;
long start;
int buz = 0;

/*Macros*/
//MaxVal dan MinVal dapat diubah sesuai sensitivitas accelerometer atau sesuai dengan perkiraan kekuatan gempa
#define samples 9
#define maxVal 9999 
#define minVal -9999 
#define buzTime 2000 

void setup() {
    lcd.begin();
    lcd.backlight();
    lcd.clear();

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

    pinMode(buzzer1, OUTPUT);
    pinMode(buzzer2, OUTPUT);
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    buz = 0;
    digitalWrite(buzzer1, buz);
    digitalWrite(buzzer2, buz);
    digitalWrite(led1, buz);
    digitalWrite(led2, buz);

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
    lcd.print(" X     Y     Z ");
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
        if (buz == 0) {
            start = millis();
        }
        buz = 1; 
    }

    if (buz == 1) {
        lcd.setCursor(0, 0);
        lcd.print("Earthquake Alert");
        if (millis() >= start + buzTime) {
            buz = 0;
        }
    } else {
        lcd.setCursor(0, 0);
        lcd.print(" X     Y     Z ");
    }

    digitalWrite(buzzer1, buz);
    digitalWrite(buzzer2, buz); 
    digitalWrite(led1, buz);
    digitalWrite(led2, buz);

    //Merupakan perintah yang akan dijalankan jika menerima !alert dari bot discord
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command == "ALERT") {
            buz = 1;
            start = millis();
        }
    }
}
