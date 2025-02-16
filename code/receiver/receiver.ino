#include <LiquidCrystal.h>
#define LDR_PIN A0  // we read from LDR at pin A0
#define THRESHOLD 500 // this value is empirical
#define MAX_MESSAGE_LEN 50  // Maximum message length

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

const int bitDuration = 2000;  // NOTE: this duration is the same for TX and RX
int lastState = 0;
unsigned long lastTime = 0;
char receivedMessage[50];
int bitCount = 0;
byte currentByte = 0;
int charIndex = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LDR_PIN, INPUT);

  // we set up the LCD's number of columns and rows
  lcd.begin(16, 2);
  
}

void processManchesterBit(int bit) {
  currentByte = (currentByte << 1) | bit;
  bitCount++;
  Serial.println("received bit %d", bit);

  if (bitCount == 8) {  // Full character received
    if (charIndex < MAX_MESSAGE_LEN - 1) {
      receivedMessage[charIndex++] = (char)currentByte;
      receivedMessage[charIndex] = '\0';  // Ensure null-terminated string
    }
    bitCount = 0;
    currentByte = 0;
    if (charIndex >= MAX_MESSAGE_LEN - 1 || (char)currentByte == '#') {
      Serial.println(receivedMessage);  // Print the reconstructed message
      lcd.print(receivedMessage);
      charIndex = 0;  // Reset for next message
    }
  }
}

void loop() {
  int ldrValue = analogRead(LDR_PIN);
  int state = (ldrValue < THRESHOLD) ? 1 : 0;  // Convert to digital signal

  unsigned long currentTime = micros();
  unsigned long deltaTime = currentTime - lastTime;

  if (state != lastState) {  // Detect transition (Manchester encoding)
      if (deltaTime >= (bitDuration / 2)) {
          int bit = (state == 1) ? 1 : 0;  // Decode bit
          processManchesterBit(bit);
      }
      lastTime = currentTime;
      lastState = state;
  }
}

