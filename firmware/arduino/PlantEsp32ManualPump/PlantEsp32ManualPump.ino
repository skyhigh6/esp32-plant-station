#include <Arduino.h>
#include <Wire.h>

#include <PlantController.h>

#ifndef PLANT_HARDWARE_ENABLE
#define PLANT_HARDWARE_ENABLE 0
#endif
#ifndef PLANT_LCD_ENABLE
#define PLANT_LCD_ENABLE 0
#endif
#ifndef PLANT_LCD_BACKPACK_PCF8574
#define PLANT_LCD_BACKPACK_PCF8574 0
#endif
#ifndef PLANT_LCD_I2C_ADDRESS
#define PLANT_LCD_I2C_ADDRESS 0x27
#endif

// No default physical pin map is provided. The board brand is confirmed as
// SunFounder, but the exact ESP32 camera extension/carrier revision is unknown.
// Camera/SD carrier boards reserve pins for camera, SD, PSRAM, flash, and onboard functions.
// Define PLANT_BOARD_PROFILE_CLASSIC_DEVKIT_WROOM32_REVIEW_ONLY only for a common
// ESP32 DevKit / ESP32-WROOM-32 review build after checking the actual schematic.
#if !defined(ARDUINO_ARCH_ESP32)
#error "This sketch is for ESP32 Arduino targets only."
#endif

#if !defined(PLANT_BOARD_PROFILE_CLASSIC_DEVKIT_WROOM32_REVIEW_ONLY)
#error "Select and review an explicit ESP32 board profile before compiling. Unknown camera carrier boards are not pin-compatible with this scaffold."
#endif

#if defined(PLANT_BOARD_PROFILE_CLASSIC_DEVKIT_WROOM32_REVIEW_ONLY)
#if !defined(CONFIG_IDF_TARGET_ESP32)
#error "The classic DevKit/WROOM-32 review profile requires a classic ESP32 target."
#endif
constexpr uint8_t PIN_SOIL_ADC = 34;
constexpr uint8_t PIN_DOSE_POT_ADC = 35;
constexpr uint8_t PIN_BUTTON_STOP = 13;
constexpr uint8_t PIN_LED_GREEN = 14;
constexpr uint8_t PIN_SOUNDER_GATE = 23;
constexpr uint8_t PIN_PUMP_GATE = 25;
constexpr uint8_t PIN_LED_RED = 26;
constexpr uint8_t PIN_LED_BLUE = 27;
constexpr uint8_t PIN_BUTTON_WATER = 32;
constexpr uint8_t PIN_BUTTON_LAMP_TEST = 33;
constexpr uint8_t PIN_I2C_SDA = 21;
constexpr uint8_t PIN_I2C_SCL = 22;
#endif

constexpr uint32_t SERIAL_PERIOD_MS = 1000;
constexpr uint32_t LCD_PERIOD_MS = 500;

plant::PlantController controller(plant::ControllerConfig{35, 5000});
uint32_t lastSerialMs = 0;
uint32_t lastLcdMs = 0;
bool pumpOutputApplied = false;

struct LcdAdapter {
  bool begin() {
#if PLANT_LCD_ENABLE && PLANT_LCD_BACKPACK_PCF8574
    Wire.beginTransmission(PLANT_LCD_I2C_ADDRESS);
    return Wire.endTransmission() == 0;
#else
    return false;
#endif
  }

  void update(uint32_t, int soilRaw, const plant::Outputs& outputs) {
    // Address probing is implemented behind the gate; bit mapping and HD44780
    // writes remain disabled until the photographed backpack is identified.
    (void)soilRaw; (void)outputs;
  }
};

LcdAdapter lcd;

bool buttonPressed(uint8_t pin) {
  return digitalRead(pin) == LOW;
}

void applyOutputs(const plant::Outputs& outputs) {
  const bool armedPump = PLANT_HARDWARE_ENABLE && outputs.pumpRequested;
  digitalWrite(PIN_PUMP_GATE, armedPump ? HIGH : LOW);
  pumpOutputApplied = armedPump;
  digitalWrite(PIN_LED_GREEN, outputs.greenLed ? HIGH : LOW);
#if PLANT_SOUNDER_ENABLE
#if PLANT_SOUNDER_PASSIVE
  if (outputs.lampTestActive) tone(PIN_SOUNDER_GATE, 2400);
  else noTone(PIN_SOUNDER_GATE);
#else
  digitalWrite(PIN_SOUNDER_GATE, outputs.lampTestActive ? HIGH : LOW);
#endif
#else
  digitalWrite(PIN_SOUNDER_GATE, LOW);
#endif
  digitalWrite(PIN_LED_RED, outputs.redLed ? HIGH : LOW);
  digitalWrite(PIN_LED_BLUE, outputs.blueLed ? HIGH : LOW);
}

void printStatus(uint32_t nowMs, int soilRaw, const plant::Outputs& outputs) {
  Serial.print(F("t_ms="));
  Serial.print(nowMs);
  Serial.print(F(" soil_raw="));
  Serial.print(soilRaw);
  Serial.print(F(" pump_request="));
  Serial.print(outputs.pumpRequested ? F("true") : F("false"));
  Serial.print(F(" pump_applied="));
  Serial.print(pumpOutputApplied ? F("true") : F("false"));
  Serial.print(F(" lamp_test="));
  Serial.print(outputs.lampTestActive ? F("true") : F("false"));
  Serial.print(F(" locked="));
  Serial.print(outputs.lockedOut ? F("true") : F("false"));
  Serial.print(F(" dose_ms="));
  Serial.println(outputs.doseMs);
}

void setup() {
  digitalWrite(PIN_PUMP_GATE, LOW);
  pinMode(PIN_PUMP_GATE, OUTPUT);

  Serial.begin(115200);
  delay(50);

  digitalWrite(PIN_SOUNDER_GATE, LOW);
  pinMode(PIN_SOUNDER_GATE, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_BUTTON_STOP, INPUT_PULLUP);
  pinMode(PIN_DOSE_POT_ADC, INPUT);
  analogReadResolution(12);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_BLUE, OUTPUT);
  pinMode(PIN_BUTTON_WATER, INPUT_PULLUP);
  pinMode(PIN_BUTTON_LAMP_TEST, INPUT_PULLUP);
  pinMode(PIN_SOIL_ADC, INPUT);

  const bool lcdReady = lcd.begin();
  Serial.println(F("ESP32 plant manual pump scaffold"));
#if PLANT_HARDWARE_ENABLE
  Serial.println(F("Hardware output: ENABLED by compile flag. Use only after wiring review."));
#else
  Serial.println(F("Hardware output: DISABLED. Set PLANT_HARDWARE_ENABLE=1 only after wiring review."));
#endif
  Serial.println(lcdReady ? F("LCD adapter enabled") : F("LCD adapter disabled: module and level shifting unknown"));

  const uint32_t nowMs = millis();
  const plant::Inputs inputs{buttonPressed(PIN_BUTTON_WATER), buttonPressed(PIN_BUTTON_LAMP_TEST), buttonPressed(PIN_BUTTON_STOP), static_cast<uint16_t>(analogRead(PIN_DOSE_POT_ADC))};
  const plant::Outputs outputs = controller.begin(nowMs, inputs);
  applyOutputs(outputs);
}

void loop() {
  const uint32_t nowMs = millis();
  const plant::Inputs inputs{buttonPressed(PIN_BUTTON_WATER), buttonPressed(PIN_BUTTON_LAMP_TEST), buttonPressed(PIN_BUTTON_STOP), static_cast<uint16_t>(analogRead(PIN_DOSE_POT_ADC))};
  const plant::Outputs outputs = controller.update(nowMs, inputs);
  applyOutputs(outputs);

  const int soilRaw = analogRead(PIN_SOIL_ADC);

  if (nowMs - lastLcdMs >= LCD_PERIOD_MS) {
    lastLcdMs = nowMs;
    lcd.update(nowMs, soilRaw, outputs);
  }

  if (nowMs - lastSerialMs >= SERIAL_PERIOD_MS) {
    lastSerialMs = nowMs;
    printStatus(nowMs, soilRaw, outputs);
  }

  delay(5);
}

