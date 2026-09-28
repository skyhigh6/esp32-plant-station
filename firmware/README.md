# Arduino Uno firmware — UI v6

Current source: `arduino/PlantUno/PlantUno.ino`, with adjacent `PlantController.h` and `PlantView.h`. Target: classic ATmega328P Arduino Uno; the sketch rejects other board profiles.

## Interface

| Pin | Connection |
|---|---|
| D2 / D3 / D4 | WATER / NEXT SCREEN and held lamp test / STOP; INPUT_PULLUP switches to GND |
| D5 / D6 / D7 | Red / yellow / green lamp outputs, each with a verified current limit |
| D9 | Enabled active-HIGH relay module input; module behaviour is user reported |
| A0 / A1 | Soil signal / dose potentiometer |
| A4 / A5 | LCD SDA / SCL; LCD VCC on regulated 5 V and GND |
| D10 | Unconnected; LCD backlight controlled over I²C |

A1 is sampled once at dose start for 1,000–4,000 ms. STOP or lamp test cancels; all buttons must be released before another dose. Soil indication is advisory; no automatic watering. The screen returns to soil status after a dose; backlight turns off after 60 s idle and wakes on input activity.

See the [operator view](../docs/operator_view.html) and [current assembly manual](../docs/documents/AM_R17/PLANT-AM-001_R17_D02.pdf) for wiring, lead identification and holds. The separate pump supply, actual relay/input characteristics and current limits need physical verification. Software STOP does not isolate power.

## Target build

Install Arduino AVR core and Bill Perry's `hd44780` library. The controlled source record distinguishes the historical build/upload evidence from physical acceptance. No new upload is performed by this release.

```powershell
arduino-cli compile --fqbn arduino:avr:uno firmware/arduino/PlantUno
```

Before any separately authorised upload or powered test, confirm the pump supply is OFF and re-detect the actual serial port.

## Host assertions

The tests include the same controller/view headers as the current Uno sketch. They cover debounce, sampled duration and bounds, STOP/lamp priority, release/lockout, clock rollover, soil fault/threshold indications, UI pages and backlight timing. They do not execute AVR GPIO/I²C or prove physical hardware operation.

```powershell
New-Item -ItemType Directory -Force .build | Out-Null
g++ -std=c++17 -Wall -Wextra -Werror firmware/test/plant_controller_tests.cpp -o .build/controller_tests.exe
g++ -std=c++17 -Wall -Wextra -Werror firmware/test/plant_view_tests.cpp -o .build/view_tests.exe
.build/controller_tests.exe
.build/view_tests.exe
```

The original UI v6 sketch and both adjacent headers are preserved byte-for-byte in this reorganisation. The older competing ESP32 controller implementation has been retired from the current tree.
