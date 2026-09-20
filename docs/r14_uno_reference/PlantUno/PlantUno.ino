#include <Arduino.h>
#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include "PlantController.h"
#include "PlantView.h"

#if !defined(ARDUINO_AVR_UNO)
#error "Select Arduino Uno (ATmega328P). This pin map is not for ESP32 or Uno R4."
#endif

constexpr uint8_t WATER = 2, LAMP = 3, STOP = 4;
constexpr uint8_t RED = 5, BLUE = 6, GREEN = 7, MOTOR = 9;
constexpr bool USE_STOP = false; // Two controls; optional third STOP on D4.
constexpr bool MOTOR_ENABLED = false; // No driver fitted: bench requests only.
plant::PlantController controller(plant::ControllerConfig{35, 5000});
hd44780_I2Cexp lcd;
bool lcdReady = false;
bool viewMode = false;
TriplePress viewGesture;
uint16_t potRaw = 0;
uint32_t lastDisplay = 0, lastSerial = 0;

plant::Inputs readInputs() {
  // Uno ADC is 10-bit; preserve the controller's full 0..4095 range.
  potRaw = analogRead(A1);
  const uint16_t pot = static_cast<uint16_t>(static_cast<uint32_t>(potRaw) * 4095UL / 1023UL);
  return {digitalRead(WATER) == LOW, digitalRead(LAMP) == LOW,
          USE_STOP && digitalRead(STOP) == LOW, pot};
}

void apply(const plant::Outputs& out) {
  digitalWrite(MOTOR, MOTOR_ENABLED && out.pumpRequested ? HIGH : LOW);
  digitalWrite(RED, out.redLed ? HIGH : LOW);
  digitalWrite(BLUE, out.blueLed ? HIGH : LOW);
  digitalWrite(GREEN, out.greenLed ? HIGH : LOW);
}

bool writeRow(uint8_t row, const char* text) {
  if (lcd.setCursor(0, row) != 0) return false;
  bool ended = false;
  for (uint8_t i = 0; i < 16; ++i) {
    if (!ended && text[i] == '\0') ended = true;
    if (lcd.write(ended ? ' ' : text[i]) != 1) return false;
  }
  return true;
}

void show(int soil, const plant::Outputs& out, const plant::Inputs& in) {
  if (!lcdReady) return;
  char line[17];
  if (viewMode) snprintf(line, sizeof(line), "VIEW S:%4d %3u%%", soil, static_cast<unsigned>(moisturePercent(soil)));
  else snprintf(line, sizeof(line), "Moisture: %3u%%", static_cast<unsigned>(moisturePercent(soil)));
  bool ok = writeRow(0, line);
  if (viewMode) snprintf(line, sizeof(line), "P%4u %3u%% W%u L%u", static_cast<unsigned>(potRaw), static_cast<unsigned>(static_cast<uint32_t>(potRaw) * 100 / 1023), static_cast<unsigned>(in.waterButtonRaw), static_cast<unsigned>(in.lampTestButtonRaw));
  else if (out.lampTestActive) snprintf(line, sizeof(line), "LAMP TEST");
  else if (out.lockedOut) snprintf(line, sizeof(line), "Release buttons");
  else if (out.pumpRequested) snprintf(line, sizeof(line), "TEST dose %4lums", static_cast<unsigned long>(out.doseMs));
  else snprintf(line, sizeof(line), "Ready MOTOR OFF");
  ok = writeRow(1, line) && ok;
  if (!ok || Wire.getWireTimeoutFlag()) {
    lcdReady = false;
    Serial.println(F("LCD write failed: check 5V/GND/SDA=A4/SCL=A5; reset after repair."));
  }
}

void setup() {
  digitalWrite(MOTOR, LOW);
  pinMode(MOTOR, OUTPUT);
  pinMode(WATER, INPUT_PULLUP);
  pinMode(LAMP, INPUT_PULLUP);
  if (USE_STOP) pinMode(STOP, INPUT_PULLUP);
  pinMode(RED, OUTPUT); pinMode(BLUE, OUTPUT); pinMode(GREEN, OUTPUT);
  Serial.begin(115200);
  Serial.println(F("PlantUno bench v2; motor disabled; dry=447 wet=221; triple LAMP toggles view"));
  Wire.begin();
  Wire.setWireTimeout(25000, true);
  const int status = lcd.begin(16, 2);
  lcdReady = status == 0;
  Serial.print(F("LCD initialisation status=")); Serial.println(status);
  if (!lcdReady) Serial.println(F("LCD failed: check 5V/GND/SDA=A4/SCL=A5. Adjust contrast only after status=0."));
  const plant::Inputs in = readInputs();
  viewGesture.begin(millis(), in.lampTestButtonRaw);
  apply(controller.begin(millis(), in));
}

void loop() {
  const uint32_t now = millis();
  const plant::Inputs in = readInputs();
  const bool toggled = viewGesture.update(now, in.lampTestButtonRaw);
  if (toggled) {
    viewMode = !viewMode;
    Serial.println(viewMode ? F("VIEW ON") : F("VIEW OFF"));
  }
  plant::Inputs controls = in;
  // Diagnostic button checks cannot request a dose; release is required on exit.
  controls.stopButtonRaw = controls.stopButtonRaw || viewMode || toggled;
  const plant::Outputs out = controller.update(now, controls);
  apply(out);
  const int soil = analogRead(A0);
  if (toggled || now - lastDisplay >= 100) { lastDisplay = now; show(soil, out, in); }
  if (now - lastSerial >= 1000) {
    lastSerial = now;
    Serial.print(F("t=")); Serial.print(now);
    Serial.print(F(" soil=")); Serial.print(soil);
    Serial.print(F(" moisture_pct=")); Serial.print(moisturePercent(soil));
    Serial.print(F(" view=")); Serial.print(viewMode);
    Serial.print(F(" pot_raw=")); Serial.print(potRaw);
    Serial.print(F(" pot=")); Serial.print(in.dosePotRaw);
    Serial.print(F(" water=")); Serial.print(in.waterButtonRaw);
    Serial.print(F(" lamp=")); Serial.print(in.lampTestButtonRaw);
    Serial.print(F(" locked=")); Serial.print(out.lockedOut);
    Serial.print(F(" request=")); Serial.print(out.pumpRequested);
    Serial.print(F(" dose_ms=")); Serial.print(out.doseMs);
    Serial.print(F(" motor=OFF lcd=")); Serial.println(lcdReady ? F("OK") : F("FAULT"));
  }
}
