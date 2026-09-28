#ifndef PLANT_VIEW_H
#define PLANT_VIEW_H
#include <stdint.h>

constexpr int SOIL_DRY = 447;
constexpr int SOIL_WET = 221;
inline uint8_t moisturePercent(int raw) {
  if (raw >= SOIL_DRY) return 0;
  if (raw <= SOIL_WET) return 100;
  return static_cast<uint8_t>((static_cast<int32_t>(SOIL_DRY - raw) * 100) / (SOIL_DRY - SOIL_WET));
}

enum class SoilState : uint8_t { Fault, Dry, Wet };
constexpr uint8_t SOIL_DRY_BELOW_PERCENT = 25;
constexpr int SOIL_FAULT_LOW_RAW = 20;

class SoilIndicator {
 public:
  void begin(uint32_t now, int raw) {
    state_ = candidate_ = classify(raw);
    changed_ = now;
    percent_ = state_ == SoilState::Fault ? 0 : moisturePercent(raw);
  }
  SoilState update(uint32_t now, int raw) {
    const SoilState next = classify(raw);
    if (next == SoilState::Fault) {
      state_ = candidate_ = next;
      changed_ = now;
      percent_ = 0;
    } else if (next == state_) {
      candidate_ = next;
      changed_ = now;
      percent_ = moisturePercent(raw);
    } else if (next != candidate_) {
      candidate_ = next;
      changed_ = now;
    } else if (now - changed_ >= 500) {
      state_ = next;
      percent_ = moisturePercent(raw);
    }
    return state_;
  }
  SoilState state() const { return state_; }
  uint8_t percent() const { return percent_; }
 private:
  static SoilState classify(int raw) {
    if (raw <= SOIL_FAULT_LOW_RAW) return SoilState::Fault;
    return moisturePercent(raw) < SOIL_DRY_BELOW_PERCENT ? SoilState::Dry : SoilState::Wet;
  }
  SoilState state_ = SoilState::Fault, candidate_ = SoilState::Fault;
  uint8_t percent_ = 0;
  uint32_t changed_ = 0;
};

inline bool redSoilBlink(SoilState state, uint32_t now) {
  const uint16_t phase = static_cast<uint16_t>(now % 1000);
  if (state == SoilState::Dry) return phase < 500; // One slow blink per second.
  if (state == SoilState::Fault) return phase < 100 || (phase >= 200 && phase < 300);
  return false;
}

class DebouncedPress {
 public:
  void begin(uint32_t now, bool pressed) {
    raw_ = stable_ = pressed;
    changed_ = now;
  }
  bool update(uint32_t now, bool pressed) {
    if (pressed != raw_) { raw_ = pressed; changed_ = now; }
    if (raw_ == stable_ || now - changed_ < 35) return false;
    stable_ = raw_;
    return stable_;
  }
 private:
  bool raw_ = false, stable_ = false;
  uint32_t changed_ = 0;
};
#endif
