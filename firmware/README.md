# ESP32 manual dose firmware

Review scaffold only. Three buttons: WATER and LAMP TEST, with STOP proposed for the unconfirmed third function. Three LEDs: red lockout, blue dose request, proposed green ready. LED colours/functions need user confirmation. Pump output is disabled by default; sounder output is always disabled pending identification. LCD adapter remains disabled.

- A debounced WATER press requests one bounded timed dose. Releasing WATER does not stop the dose; STOP or LAMP TEST cancels immediately on the next loop.
- Potentiometer is sampled once at dose start: 12-bit 0–4095 maps to provisional 0–5000 ms. Zero requests no pump output. Changing the knob during a dose does not change that dose.
- No repeated or queued doses: after completion/cancellation all buttons must be released continuously for 35 ms before a fresh WATER press can start another dose.
- Boot-held buttons require the same stable release. Lamp test lights all three LEDs and inhibits the pump; STOP always inhibits the pump.
- Manual only: soil reading does not trigger watering. No networking, automatic watering or persistent storage.

Duration is not calibrated volume. Do not label the knob in ml yet. Measure delivered volume at several durations using the installed tubing, lift, supply and priming condition. For an adequately linear calibrated range, volume_ml = measured_flow_ml_per_s × duration_ms / 1000. Record startup lag, repeated-dose variation and uncertainty; use a measured lookup table if nonlinear. The provisional 5 s cap is a software review value, not an approved wet-test quantity.

## Build / verification

The actual SunFounder camera carrier revision and pin allocation remain unknown. No real hardware pin map is approved. The explicit classic DevKit/WROOM-32 profile exists solely for a compile review, not for flashing the supplied carrier.

```powershell
arduino-cli compile --fqbn esp32:esp32:esp32 --libraries firmware\libraries --build-property "compiler.cpp.extra_flags=-DPLANT_BOARD_PROFILE_CLASSIC_DEVKIT_WROOM32_REVIEW_ONLY" firmware\arduino\PlantEsp32ManualPump
```

Host assertions (requires a native C++ compiler):

```powershell
g++ -std=c++17 -Wall -Wextra -Werror firmware/test/plant_controller_tests.cpp -o plant_controller_tests.exe
.\plant_controller_tests.exe
```

Tests cover debounce, fixed sampled dose, release during dose, deadline, held/repress guard, stable release, lamp/STOP priority, boot STOP held, zero dose, clamping, reset and clock rollover. Target compilation does not execute these host tests or prove physical operation. Software deadlines depend on loop execution; use a hardware cutoff if failure-independent timing is required.

Verification 2026-09-08: classic ESP32 review profile compiled successfully with installed ESP32 Arduino core 2.0.17; 272957 bytes flash and 21944 bytes global RAM. Integrator executed all host assertions successfully using portable Zig 0.16.0 with C++17, -nostdlib++, -Wall -Wextra -Werror; see docs/REVIEW.md. No upload or physical output test performed.

