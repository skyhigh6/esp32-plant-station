#ifndef PLANT_CONTROLLER_H
#define PLANT_CONTROLLER_H
#include <stdint.h>
namespace plant {
struct ControllerConfig {
  ControllerConfig(uint32_t debounce = 35, uint32_t maximum = 5000)
      : debounceMs(debounce), maxPumpRunMs(maximum) {}
  uint32_t debounceMs;
  uint32_t maxPumpRunMs;
};
struct Inputs {
  Inputs(bool water = false, bool lamp = false, bool stop = false, uint16_t pot = 0)
      : waterButtonRaw(water), lampTestButtonRaw(lamp), stopButtonRaw(stop), dosePotRaw(pot) {}
  bool waterButtonRaw, lampTestButtonRaw, stopButtonRaw;
  uint16_t dosePotRaw;
};
struct Outputs {
  bool pumpRequested = false, redLed = false, blueLed = false, greenLed = false;
  bool lampTestActive = false, lockedOut = false;
  uint32_t doseMs = 0;
};
enum class LockReason { None, BootHeld, StopOrLamp, DoseComplete };
class PlantController {
 public:
  explicit PlantController(ControllerConfig config = ControllerConfig{}) : config_(config) {}
  Outputs begin(uint32_t now, Inputs in) {
    started_ = true; running_ = false; tracking_ = false; releasing_ = false;
    doseMs_ = 0; lock_ = any(in) ? LockReason::BootHeld : LockReason::None;
    return update(now, in);
  }
  Outputs update(uint32_t now, Inputs in) {
    if (!started_) return begin(now, in);
    // Raw stop/lamp edges cancel a dose without debounce. Neither can start one.
    if (in.stopButtonRaw || in.lampTestButtonRaw) {
      running_ = false; tracking_ = false; releasing_ = false;
      lock_ = LockReason::StopOrLamp;
      return output(in.lampTestButtonRaw);
    }
    if (running_) {
      if (now - startMs_ >= doseMs_) {
        running_ = false; lock_ = LockReason::DoseComplete; releasing_ = false;
      }
      return output(false);
    }
    // A stable all-released interval AFTER completion/cancellation prevents bounce,
    // held buttons or presses made during a dose from queuing another dose.
    if (lock_ != LockReason::None) {
      if (any(in)) releasing_ = false;
      else if (!releasing_) { releasing_ = true; releaseMs_ = now; }
      else if (now - releaseMs_ >= config_.debounceMs) {
        lock_ = LockReason::None; releasing_ = false;
      }
      return output(false);
    }
    if (!in.waterButtonRaw) { tracking_ = false; return output(false); }
    if (!tracking_) { tracking_ = true; pressMs_ = now; }
    if (now - pressMs_ >= config_.debounceMs) {
      // No volume claim: provisional 0..max milliseconds, pot sampled once at start.
      const uint16_t raw = in.dosePotRaw > 4095 ? 4095 : in.dosePotRaw;
      doseMs_ = static_cast<uint32_t>((static_cast<uint64_t>(raw) * config_.maxPumpRunMs) / 4095);
      startMs_ = now; tracking_ = false; running_ = doseMs_ > 0;
      if (!running_) lock_ = LockReason::DoseComplete;
    }
    return output(false);
  }
  LockReason lockReason() const { return lock_; }
 private:
  static bool any(Inputs in) { return in.waterButtonRaw || in.lampTestButtonRaw || in.stopButtonRaw; }
  Outputs output(bool lamp) const {
    Outputs out;
    out.pumpRequested = running_; out.lockedOut = lock_ != LockReason::None;
    out.lampTestActive = lamp; out.redLed = lamp || out.lockedOut;
    out.blueLed = lamp || running_; out.greenLed = lamp || (!running_ && !out.lockedOut);
    out.doseMs = doseMs_; return out;
  }
  ControllerConfig config_;
  bool started_ = false, running_ = false, tracking_ = false, releasing_ = false;
  uint32_t startMs_ = 0, pressMs_ = 0, releaseMs_ = 0, doseMs_ = 0;
  LockReason lock_ = LockReason::None;
};
}
#endif
