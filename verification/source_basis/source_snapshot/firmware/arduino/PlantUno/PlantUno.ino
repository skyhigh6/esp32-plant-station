#include <Arduino.h>
#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include "PlantController.h"
#include "PlantView.h"

#if !defined(ARDUINO_AVR_UNO)
#error "Select Arduino Uno (ATmega328P). This pin map is not for ESP32 or Uno R4."
#endif

constexpr uint8_t WATER_BUTTON = 2, LAMP_BUTTON = 3, STOP_BUTTON = 4;
// Red STOP, yellow LAMP TEST and green WATER lamps each need their own current limit.
constexpr uint8_t LOCKOUT_LED = 5, DOSING_LED = 6, READY_LED = 7;
constexpr uint8_t RELAY_MODULE_IN = 9;
enum class RelayTrigger { Unknown, ActiveHigh, ActiveLow };
constexpr RelayTrigger RELAY_TRIGGER = RelayTrigger::ActiveHigh; // User-reported module behaviour.
constexpr bool RELAY_ENABLED = true;
constexpr uint32_t MIN_PUMP_RUN_MS = 1000;
constexpr uint32_t MAX_PUMP_RUN_MS = 4000;
constexpr uint32_t LCD_BACKLIGHT_IDLE_MS = 60000;
constexpr uint16_t POT_ACTIVITY_DEADBAND = 8;
static_assert(MIN_PUMP_RUN_MS <= MAX_PUMP_RUN_MS, "Invalid pump duration range.");
static_assert(!RELAY_ENABLED || RELAY_TRIGGER != RelayTrigger::Unknown,
              "Set the measured relay trigger polarity before enabling D9.");
plant::PlantController controller(plant::ControllerConfig{35, MAX_PUMP_RUN_MS, MIN_PUMP_RUN_MS});
hd44780_I2Cexp lcd;
bool lcdReady = false;
bool backlightControlAvailable = false, backlightOn = false;
uint32_t lastActivityAt = 0;
uint16_t lastPotActivityRaw = 0;
bool relayApplied = false;
DebouncedPress pageButton;
SoilIndicator soilIndicator;
uint8_t page = 0;
enum class Notice : uint8_t { None, StopPressed, Cleared };
Notice notice = Notice::None;
uint32_t noticeAt = 0, doseStartedAt = 0, stopPressedAt = 0;
uint16_t completedCount = 0, cancelledCount = 0;
uint32_t lastCompletedMs = 0;
bool wasRunning = false, stopWasPressed = false, stopHoldHandled = false;
bool returnToSoil = false;
bool ignoreLampPageUntilRelease = false;
uint16_t potRaw = 0;
uint32_t lastDisplay = 0, lastSerial = 0;

plant::Inputs readInputs() {
  // Uno ADC is 10-bit; preserve the controller's full 0..4095 range.
  potRaw = analogRead(A1);
  const uint16_t pot = static_cast<uint16_t>(static_cast<uint32_t>(potRaw) * 4095UL / 1023UL);
  return {digitalRead(WATER_BUTTON) == LOW, digitalRead(LAMP_BUTTON) == LOW,
          digitalRead(STOP_BUTTON) == LOW, pot};
}

void apply(const plant::Outputs& out, SoilState soilState, uint32_t now) {
  if (RELAY_ENABLED) {
    const uint8_t active = RELAY_TRIGGER == RelayTrigger::ActiveHigh ? HIGH : LOW;
    relayApplied = out.pumpRequested;
    digitalWrite(RELAY_MODULE_IN, relayApplied ? active : (active == HIGH ? LOW : HIGH));
  }
  const bool red = out.lampTestActive || out.lockedOut || redSoilBlink(soilState, now);
  const bool green = out.lampTestActive || (!out.lockedOut && soilState == SoilState::Wet);
  digitalWrite(LOCKOUT_LED, red ? HIGH : LOW);
  digitalWrite(DOSING_LED, out.blueLed ? HIGH : LOW);
  digitalWrite(READY_LED, green ? HIGH : LOW);
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

void show(int soil, SoilState soilState, uint8_t soilPercent, const plant::Outputs& out,
          const plant::Inputs& in, uint32_t now) {
  if (!lcdReady) return;
  char top[17] = "", bottom[17] = "";
  if (out.pumpRequested) {
    const uint32_t elapsed = now - doseStartedAt;
    const uint32_t left = elapsed < out.doseMs ? out.doseMs - elapsed : 0;
    snprintf(top, sizeof(top), "PUMP RUNNING");
    snprintf(bottom, sizeof(bottom), "Left %lu.%lus STOP",
             static_cast<unsigned long>(left / 1000), static_cast<unsigned long>((left % 1000) / 100));
  } else if (out.lampTestActive) {
    snprintf(top, sizeof(top), "LAMP TEST");
    snprintf(bottom, sizeof(bottom), "Screen %u of 3", static_cast<unsigned>(page + 1));
  } else if (!returnToSoil && notice != Notice::None && now - noticeAt < 2000) {
    switch (notice) {
      case Notice::StopPressed:
        snprintf(top, sizeof(top), "STOP pressed");
        snprintf(bottom, sizeof(bottom), "Hold 2s: clear");
        break;
      case Notice::Cleared:
        snprintf(top, sizeof(top), "COUNTERS CLEAR");
        snprintf(bottom, sizeof(bottom), "Pump is OFF");
        break;
      default: break;
    }
  } else if (out.lockedOut && !returnToSoil) {
    snprintf(top, sizeof(top), "PUMP LOCKED");
    snprintf(bottom, sizeof(bottom), "Release buttons");
  } else if (page == 0) {
    if (soilState == SoilState::Fault) {
      snprintf(top, sizeof(top), "CHECK SOIL A0");
      snprintf(bottom, sizeof(bottom), "Raw %4d", soil);
    } else {
      const uint32_t setMs = controller.plannedDoseMs(in.dosePotRaw);
      snprintf(top, sizeof(top), "%s %3u%% %s", soilState == SoilState::Dry ? "DRY" : "WET",
               static_cast<unsigned>(soilPercent),
               soilState == SoilState::Dry ? "WATER" : "READY");
      snprintf(bottom, sizeof(bottom), "Dose set %lu.%lu s", static_cast<unsigned long>(setMs / 1000),
               static_cast<unsigned long>((setMs % 1000) / 100));
    }
  } else if (page == 1) {
    snprintf(top, sizeof(top), "Soil raw %4d", soil);
    snprintf(bottom, sizeof(bottom), "Pot raw  %4u", static_cast<unsigned>(potRaw));
  } else {
    snprintf(top, sizeof(top), "OK%3u CUT%3u", static_cast<unsigned>(completedCount),
             static_cast<unsigned>(cancelledCount));
    if (completedCount) snprintf(bottom, sizeof(bottom), "Last %lu.%lu sec",
                                 static_cast<unsigned long>(lastCompletedMs / 1000),
                                 static_cast<unsigned long>((lastCompletedMs % 1000) / 100));
    else snprintf(bottom, sizeof(bottom), "No doses yet");
  }
  bool ok = writeRow(0, top);
  ok = writeRow(1, bottom) && ok;
  if (!ok || Wire.getWireTimeoutFlag()) {
    lcdReady = false;
    Serial.println(F("LCD write failed: check 5V/GND/SDA=A4/SCL=A5; reset after repair."));
  }
}

void updateBacklight(uint32_t now, bool active) {
  if (active) lastActivityAt = now;
  if (!lcdReady || !backlightControlAvailable) return;
  const bool shouldBeOn = now - lastActivityAt < LCD_BACKLIGHT_IDLE_MS;
  if (shouldBeOn == backlightOn) return;
  const int status = shouldBeOn ? lcd.backlight() : lcd.noBacklight();
  if (status != 0) {
    backlightControlAvailable = false;
    Serial.print(F("LCD backlight control failed, status=")); Serial.println(status);
    return;
  }
  backlightOn = shouldBeOn;
  Serial.println(shouldBeOn ? F("LCD backlight=ON activity") : F("LCD backlight=OFF idle"));
}

void setup() {
  // Establish the inactive level before switching D9 to output mode.
  if (RELAY_ENABLED) {
    digitalWrite(RELAY_MODULE_IN, RELAY_TRIGGER == RelayTrigger::ActiveHigh ? LOW : HIGH);
    pinMode(RELAY_MODULE_IN, OUTPUT);
  } else {
    digitalWrite(RELAY_MODULE_IN, LOW); // No pull-up while D9 is an input.
    pinMode(RELAY_MODULE_IN, INPUT);
  }
  pinMode(WATER_BUTTON, INPUT_PULLUP);
  pinMode(LAMP_BUTTON, INPUT_PULLUP);
  pinMode(STOP_BUTTON, INPUT_PULLUP);
  pinMode(LOCKOUT_LED, OUTPUT); pinMode(DOSING_LED, OUTPUT); pinMode(READY_LED, OUTPUT);
  Serial.begin(115200);
  Serial.println(F("PlantUno UI v6; relay HIGH; dose 1000..4000ms; LCD backlight idle 60s"));
  Wire.begin();
  Wire.setWireTimeout(25000, true);
  const int status = lcd.begin(16, 2);
  lcdReady = status == 0;
  Serial.print(F("LCD initialisation status=")); Serial.println(status);
  if (!lcdReady) Serial.println(F("LCD failed: check 5V/GND/SDA=A4/SCL=A5. Adjust contrast only after status=0."));
  if (lcdReady) {
    const int backlightStatus = lcd.backlight();
    backlightControlAvailable = backlightStatus == 0;
    backlightOn = backlightControlAvailable;
    if (!backlightControlAvailable) {
      Serial.print(F("LCD backlight control unavailable, status=")); Serial.println(backlightStatus);
    }
  }
  const plant::Inputs in = readInputs();
  pageButton.begin(millis(), in.lampTestButtonRaw);
  const uint32_t now = millis();
  lastActivityAt = now;
  lastPotActivityRaw = potRaw;
  soilIndicator.begin(now, analogRead(A0));
  apply(controller.begin(now, in), soilIndicator.state(), now);
}

void loop() {
  const uint32_t now = millis();
  const plant::Inputs in = readInputs();
  const bool potMoved = abs(static_cast<int>(potRaw) - static_cast<int>(lastPotActivityRaw)) >=
                        POT_ACTIVITY_DEADBAND;
  if (potMoved) lastPotActivityRaw = potRaw;
  if (wasRunning && in.lampTestButtonRaw) ignoreLampPageUntilRelease = true;
  if (!in.lampTestButtonRaw) ignoreLampPageUntilRelease = false;
  if (pageButton.update(now, in.lampTestButtonRaw) && !ignoreLampPageUntilRelease) {
    page = static_cast<uint8_t>((page + 1) % 3);
    returnToSoil = false;
    Serial.print(F("SCREEN ")); Serial.println(static_cast<unsigned>(page + 1));
  }
  if (in.stopButtonRaw && !stopWasPressed) {
    stopPressedAt = now;
    stopHoldHandled = false;
    returnToSoil = false;
    notice = Notice::StopPressed;
    noticeAt = now;
  } else if (!in.stopButtonRaw) {
    stopHoldHandled = false;
  }
  stopWasPressed = in.stopButtonRaw;
  const plant::Outputs out = controller.update(now, in);
  const int soil = analogRead(A0);
  const SoilState soilState = soilIndicator.update(now, soil);
  const uint8_t soilPercent = soilIndicator.percent();
  apply(out, soilState, now);
  const bool doseEnded = wasRunning && !out.pumpRequested;
  if (out.pumpRequested && !wasRunning) {
    doseStartedAt = now;
    returnToSoil = false;
    Serial.print(F("DOSE START ms=")); Serial.println(out.doseMs);
  } else if (doseEnded) {
    page = 0;
    returnToSoil = true;
    notice = Notice::None;
    if (controller.lockReason() == plant::LockReason::DoseComplete) {
      if (completedCount < 999) ++completedCount;
      lastCompletedMs = out.doseMs;
      Serial.println(F("DOSE COMPLETE"));
    } else {
      if (cancelledCount < 999) ++cancelledCount;
      Serial.println(F("DOSE CANCELLED"));
    }
  }
  wasRunning = out.pumpRequested;
  updateBacklight(now, in.waterButtonRaw || in.lampTestButtonRaw || in.stopButtonRaw ||
                       potMoved || out.pumpRequested || doseEnded);
  if (in.stopButtonRaw && !stopHoldHandled && now - stopPressedAt >= 2000) {
    completedCount = 0;
    cancelledCount = 0;
    lastCompletedMs = 0;
    stopHoldHandled = true;
    returnToSoil = false;
    notice = Notice::Cleared;
    noticeAt = now;
    Serial.println(F("SESSION COUNTERS CLEAR"));
  }
  if (now - lastDisplay >= 100) { lastDisplay = now; show(soil, soilState, soilPercent, out, in, now); }
  if (now - lastSerial >= 1000) {
    lastSerial = now;
    Serial.print(F("t=")); Serial.print(now);
    Serial.print(F(" soil=")); Serial.print(soil);
    Serial.print(F(" moisture_pct="));
    if (soilState == SoilState::Fault) Serial.print(F("INVALID"));
    else Serial.print(soilPercent);
    Serial.print(F(" soil_state="));
    Serial.print(soilState == SoilState::Fault ? F("FAULT") :
                 soilState == SoilState::Dry ? F("DRY") : F("WET"));
    Serial.print(F(" page=")); Serial.print(static_cast<unsigned>(page + 1));
    Serial.print(F(" pot_raw=")); Serial.print(potRaw);
    Serial.print(F(" pot=")); Serial.print(in.dosePotRaw);
    Serial.print(F(" water=")); Serial.print(in.waterButtonRaw);
    Serial.print(F(" lamp=")); Serial.print(in.lampTestButtonRaw);
    Serial.print(F(" stop=")); Serial.print(in.stopButtonRaw);
    Serial.print(F(" locked=")); Serial.print(out.lockedOut);
    Serial.print(F(" request=")); Serial.print(out.pumpRequested);
    Serial.print(F(" dose_ms=")); Serial.print(out.doseMs);
    Serial.print(F(" relay="));
    Serial.print(relayApplied ? F("ON") : F("OFF"));
    Serial.print(F(" lcd=")); Serial.println(lcdReady ? F("OK") : F("FAULT"));
  }
}
