/*
  Course: Build Your First AI Computer Vision System
  Week 4 — Arduino alarm firmware

  Upload this sketch with the Arduino IDE, then close the Serial Monitor
  before running the Python programs (only one app can use the port).

  Wiring:
    - Built-in LED on pin 13 (always available)
    - Optional external LED on pin 8 (+ 220 ohm resistor to GND)
    - Optional active buzzer on pin 9 (to GND)

  Commands (one per line, ending with newline):
    LED_ON
    LED_OFF
    BUZZ_ON
    BUZZ_OFF
    ALARM
    DISARM
*/

const int LED_BUILTIN_PIN = 13;
const int LED_EXTERNAL_PIN = 8;
const int BUZZER_PIN = 9;

bool alarmMode = false;
unsigned long lastBlinkMs = 0;
bool blinkOn = false;

void setLed(bool on) {
  digitalWrite(LED_BUILTIN_PIN, on ? HIGH : LOW);
  digitalWrite(LED_EXTERNAL_PIN, on ? HIGH : LOW);
}

void setBuzz(bool on) {
  digitalWrite(BUZZER_PIN, on ? HIGH : LOW);
}

void setup() {
  pinMode(LED_BUILTIN_PIN, OUTPUT);
  pinMode(LED_EXTERNAL_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  setLed(false);
  setBuzz(false);

  Serial.begin(9600);
  while (!Serial) {
    ; // wait on boards that need it
  }
  Serial.println("READY");
}

void loop() {
  // Read a full command line when available
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();

    if (command == "LED_ON") {
      alarmMode = false;
      setLed(true);
      Serial.println("OK LED_ON");
    } else if (command == "LED_OFF") {
      alarmMode = false;
      setLed(false);
      Serial.println("OK LED_OFF");
    } else if (command == "BUZZ_ON") {
      alarmMode = false;
      setBuzz(true);
      Serial.println("OK BUZZ_ON");
    } else if (command == "BUZZ_OFF") {
      alarmMode = false;
      setBuzz(false);
      Serial.println("OK BUZZ_OFF");
    } else if (command == "ALARM") {
      alarmMode = true;
      Serial.println("OK ALARM");
    } else if (command == "DISARM") {
      alarmMode = false;
      setLed(false);
      setBuzz(false);
      Serial.println("OK DISARM");
    } else if (command.length() > 0) {
      Serial.print("ERR UNKNOWN ");
      Serial.println(command);
    }
  }

  // Simple alarm blink/beep pattern while alarmMode is true
  if (alarmMode) {
    unsigned long now = millis();
    if (now - lastBlinkMs >= 200) {
      lastBlinkMs = now;
      blinkOn = !blinkOn;
      setLed(blinkOn);
      setBuzz(blinkOn);
    }
  }
}
