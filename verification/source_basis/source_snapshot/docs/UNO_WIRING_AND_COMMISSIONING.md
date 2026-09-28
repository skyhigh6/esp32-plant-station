# Arduino Uno plant station

**27 September 2026 interface revision:** The current switch, integrated LED and relay pin schedule is in [UNO_BUTTON_RELAY_REVISION_2026-09-27.md](UNO_BUTTON_RELAY_REVISION_2026-09-27.md). The wiring and motor-driver instructions below describe the earlier 15 September bench configuration and must not be used for the revised relay build. The R14 assembly manual and its frozen firmware snapshot remain historical issue records.

15 September 2026. Current electrical/firmware direction: classic 5 V Arduino Uno R3 / ATmega328P. Existing ESP32/SunFounder wiring is superseded for this build. Remove the SunFounder carrier from the circuit. Existing printed enclosure/PCB geometry is not Uno-compatible by assumption; bench mount first and measure before a mechanical redesign.

## Parts and wiring

Power off before rewiring. Assumed display: existing 16×2 QAPASS/PCF8574 I2C LCD. User reports a 3.3 V DC pump motor; rated/stall current unknown and no driver available. Motor and unidentified sounder remain disconnected.

| Uno label | Part |
|---|---|
| 5V | LCD VCC; dose potentiometer outer high terminal |
| GND | LCD GND; sensor GND; potentiometer outer low terminal; all switch returns and LED cathodes |
| A4 / SDA | LCD SDA — use analogue A4, not digital D4 |
| A5 / SCL | LCD SCL — use analogue A5, not digital D5 |
| 3.3V | Capacitive Soil Moisture Sensor v1.2 VCC, subject to module rating; no motor on this rail |
| A0 | Soil sensor AOUT |
| A1 | Potentiometer centre/wiper |
| D2 | WATER normally-open switch, other contact to GND |
| D3 | LAMP TEST normally-open switch, other contact to GND |
| D5 | 1 kΩ series resistor → red LED anode |
| D6 | 1 kΩ series resistor → blue LED anode |
| D7 | 1 kΩ series resistor → green LED anode |
| D4 | Optional STOP to GND; ignored unless USE_STOP is set true |
| D9 | Reserved motor-driver control, held LOW in supplied sketch |
| D8 | Reserved for a later identified sounder driver; leave disconnected |

Uno R3 has 5 V logic, so the 5 V PCF8574 LCD connects directly to A4/A5 without the ESP32 level shifter. Sensor is kept at 3.3 V; Uno ADC values will not necessarily span 0–1023. A4/A5 and dedicated SDA/SCL labels are the same bus. Each LED has its own resistor. Buttons use internal pull-ups. Never transfer ESP32 GPIO numbers to Uno terminals.

## Motor circuit still required

Use a regulated 3.3 V motor supply sized for measured startup/stall current. Motor + to supply +; motor − to logic-level N-MOSFET drain; source to supply GND; Uno GND to same GND. D9 through 100–220 Ω to gate, 47–100 kΩ gate-to-source pull-down. Flyback diode across motor with cathode/band to motor + and anode to drain. Driver must accept Uno's 5 V logic and be rated for the motor current. Do not power this 3.3 V motor from Uno 5V, a GPIO or the Uno 3.3V regulator. No driver or motor supply is selected until current is known.

## Sketch and setup

### v2 calibration and diagnostic view

User bench measurements: dry 447; watering transient 189; settled wet 221. The display uses dry=447 (0%) and settled wet=221 (100%); transient 189 is excluded as an endpoint. Moisture index is `(447 - raw) * 100 / 226`, clamped to 0–100%. This is a relative soil/probe index, not volumetric water content. Constants are saved in `PlantView.h` and survive resets as part of the sketch.

Press LAMP TEST three times within 1.2 seconds to toggle VIEW; each press and release must settle for 35 ms. Repeat to exit. Normal lamp-test behaviour is retained. VIEW updates every 100 ms: row 1 shows soil raw and moisture percentage; row 2 shows pot raw (0–1023), pot percentage and W/L input states (1=pressed). WATER cannot request a dose in VIEW; all buttons must be released before another dose is accepted on exit. View mode starts off after reset. Motor output remains disabled.

v2 compiled for Uno: 12418 bytes flash and 657 bytes static RAM. Host tests cover calibration/clamping, triple press, bounce, held input, timeout, clock rollover and dose inhibition/release after diagnostics.

Open `firmware/arduino/PlantUno/PlantUno.ino` in Arduino IDE. Keep its supplied `PlantController.h` in the same folder; this is a copy of the tested project controller. Select Arduino Uno (not Uno R4), and the freshly detected serial port. Install **hd44780 by Bill Perry** using Library Manager; it is already installed on this computer. This library is GPL-3.0; retain its licence if redistributing it.

LCD address and backpack mapping are auto-detected. LCD rows are overwritten without repeatedly clearing or switching the backlight. The LCD shows raw soil readings (not calibrated percent), readiness, release lockout, lamp test and simulated timed doses. USB serial is 115200 baud. LCD initialisation status 0 means success; nonzero is a fault. Runtime write errors disable display updates and report a fault; reset after repair. I2C transactions have a timeout.

The Uno ADC is scaled from 0–1023 to the existing controller's 0–4095 input. WATER samples the pot once for a 0–5000 ms simulated dose; releasing WATER does not cancel. LAMP TEST cancels and lights all three LEDs. Another dose requires stable release and a fresh press. Optional STOP is disabled by default. No moisture-triggered watering. MOTOR_ENABLED is false: D9 stays LOW regardless of requests. Do not enable merely by editing that constant: motor commissioning, display behaviour and fail-low pot wiring need review first.

## Acceptance sequence

1. Connect Uno and LCD only. Upload; confirm serial startup and LCD status=0. Display should show steady text. Turn the backpack contrast trimmer slowly if backlight is steady but characters are absent. If status is nonzero, repair power and I2C wiring first; contrast cannot repair bus communication.
2. If the whole backlight still flashes, disconnect power and check for loose supply/ground connections or shorts. Measure LCD VCC to GND and check serial for repeated startup messages. Flashing does not by itself prove a software fault.
3. Connect sensor and verify raw changes between dry/wet conditions. Record calibration in actual soil before adding a percentage. Keep electronics above the soil/water line.
4. Connect buttons and LEDs. With buttons released, serial water=0/lamp=0 and locked=0. Lamp test lights all three; release restores readiness after debounce. Check wiring if an input stays active.
5. Connect pot; check minimum/maximum dose, one request per press, no repeat while held, and lamp cancellation. Floating analogue inputs are not meaningful measurements. D9 must remain LOW throughout.
6. Motor testing remains pending driver, supply/current checks, diode, physical gate pull-down and calibrated flow. No wet commissioning or enclosure compatibility is claimed.

## Build verification

Uno target compilation passed: 11696 bytes flash, 605 bytes static RAM on Arduino AVR core 1.8.7. Existing controller host assertions passed. Uploaded successfully to newly detected CH340 COM9; serial startup confirms PlantUno bench v1. Over seven seconds, runtime timestamps advanced normally, released WATER/LAMP read 0, lockout read 0 and motor stayed OFF. LCD initialisation returned -4 and lcd=FAULT: LCD operation is not verified. Soil read 92–95 and scaled pot 368–380; these do not prove wiring or calibration. Evidence: `output/firmware_uno_2026-09-15/serial_readback.txt`. Next required physical check is LCD GND/5V/A4/A5 wiring, followed by reset.

References: https://docs.arduino.cc/hardware/uno-rev3/ and https://github.com/duinoWitchery/hd44780 .
