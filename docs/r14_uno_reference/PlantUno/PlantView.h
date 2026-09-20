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

class TriplePress {
 public:
  void begin(uint32_t now, bool pressed) {
    raw_ = stable_ = pressed;
    changed_ = now;
    count_ = 0;
  }
  bool update(uint32_t now, bool pressed) {
    if (count_ && now - first_ > 1200) count_ = 0;
    if (pressed != raw_) { raw_ = pressed; changed_ = now; }
    if (raw_ == stable_ || now - changed_ < 35) return false;
    stable_ = raw_;
    if (!stable_) return false;
    if (!count_) first_ = now;
    if (++count_ != 3) return false;
    count_ = 0;
    return true;
  }
 private:
  bool raw_ = false, stable_ = false;
  uint8_t count_ = 0;
  uint32_t changed_ = 0, first_ = 0;
};
#endif
