# Uno button lamps and pump relay — 27 September 2026

For an operator-facing pin map and test sequence, open the [self-contained browser view](UNO_BUTTON_RELAY_BROWSER_VIEW_2026-09-27.html).

This is the current electrical interface for `firmware/arduino/PlantUno/PlantUno.ino`. It supersedes the switch-lamp and motor-driver pin instructions in the 15 September Uno bench note and the frozen R14 manual. The old documents remain evidence of their issued configurations.

## Confirmed choices and limits

- Three four-wire momentary buttons: WATER, LAMP TEST and STOP/cancel. Their two switch wires are electrically separate from their two LED wires. STOP is a software cancellation input, not an electrical isolation switch.
- Button colours and functions: green WATER/wet; yellow NEXT SCREEN/lamp test/dose in progress; red STOP/dry warning. The operator set **below 25% moisture** as too dry on 27 September.
- Rear lead colours, reported by the user for the buttons: **green = LED+**, **yellow = LED−**, **red and black = switch contacts**. Use red as the digital-input contact and black as the GND contact in this schedule; the switch pair is non-polarised. The lead assignment is a reported observation, not an electrical test result, so confirm each of the three physical buttons before power is applied.
- User reports that the proposed 5 V trigger relay module switches ON when its input is HIGH. The actual module, input current, coil supply requirements, power-on behaviour and contact rating have not been identified or measured.
- The user reports that the buttons, LCD, relay and pump work, with the pump supplied separately at 3.5 V. This is operator-reported function, not measured timing, current, volume or a rated-voltage check.
- `RELAY_ENABLED=true` remains active. D9 is set LOW at the start of `setup()` and goes HIGH only for an accepted WATER dose request, now 1,000–4,000 ms according to A1. D9 is high impedance during reset/bootloader time; its voltage and relay contact state have not been measured here.
- The pump supply was reported OFF before the LCD backlight revision was uploaded on COM8. Serial readback identified `PlantUno UI v6` and `relay=OFF` at rest. This boot initialised the LCD with status `0`; prior v5 and v4 runs had intermittent LCD communication faults, so the display connection still needs inspection. Physical confirmation of post-dose return remains open.

## Pin and wire schedule

| Uno terminal | Connection | Firmware behaviour |
| --- | --- | --- |
| D2 | Green WATER button's **red switch lead**; black switch lead to GND | `INPUT_PULLUP`; pressed reads LOW |
| D3 | Yellow LAMP TEST button's **red switch lead**; black switch lead to GND | `INPUT_PULLUP`; pressed reads LOW |
| D4 | Red STOP button's **red switch lead**; black switch lead to GND | `INPUT_PULLUP`; pressed reads LOW; cancels a dose |
| D5 | Series current limit to red STOP button's **green LED+ lead**; yellow LED− lead to GND | Slow blink below 25% moisture; fast double flash for rail-low A0; solid for STOP/lockout or lamp test |
| D6 | Series current limit to yellow LAMP TEST button's **green LED+ lead**; yellow LED− lead to GND | HIGH during a dose request or lamp test |
| D7 | Series current limit to green WATER button's **green LED+ lead**; yellow LED− lead to GND | Steady at 25% moisture or above, including during a dose; OFF for dry, sensor fault or STOP/lockout; ON for lamp test |
| D9 | Relay module logic input, physical wiring to verify | Enabled output; active HIGH for an accepted request; otherwise LOW |
| D10 | No connection to LCD VCC | Reserved; LCD backlight is controlled over I²C |
| A4 / A5 | Existing LCD SDA / SCL | I2C display; 5 V and GND per backpack marking |
| A0 / A1 | Existing soil-sensor output / dose-pot wiper | Sensor advisory; A1 sets 1,000–4,000 ms, sampled once when WATER starts |

Each button uses all four leads: red switch lead to its digital input, black switch lead to GND; green LED+ lead from its separate digital output through a suitable current limit, yellow LED− lead to GND. Identify the actual contacts and LED polarity for **each** button with power removed; the reported colour mapping is not a substitute for measurement. Confirm whether each purchased LED has an internal 5 V current limiter; choose and verify an external resistor if it does not. Do not connect an unverified LED directly to an Uno output. Keep the switch and LED circuits distinct even though both returns reach a ground rail.

WATER produces one timed request, yellow indication and D9 HIGH. The potentiometer's lowest ADC reading selects 1,000 ms and its highest selects 4,000 ms; an intermediate position is linear between those endpoints. The value is sampled once when WATER starts, so turning the knob cannot lengthen or shorten a running dose. The LCD shows a countdown and returns directly to the Status page's soil percentage when the request ends, even if WATER is still held. A sensor fault shows `CHECK SOIL A0` instead of a false percentage. STOP or yellow cancels on the next controller update; all switches then need a stable release before another WATER press.

Each debounced yellow press while idle cycles the LCD through Status (moisture and next duration), Raw (soil and knob ADC values), and Session (completed/cancelled counts and last completed duration). Holding yellow lights all three button LEDs. If yellow cancels a run, that press does not change page; after release the soil Status page returns. STOP shows an idle-press notice; holding it for two seconds clears the volatile session counters. These counters reset on power loss. A screen page does not initiate pumping. The soil reading is advisory only; an LCD fault does not inhibit a manual request. The prior upload initialised the LCD successfully, then lost write communication during a WATER request; the pages were not physically verified after that fault.

The red lamp blinks once per second while a valid A0 reading is **below 25%** on the installed 447-dry/221-wet calibration. At **25% or above**, the green lamp stays on. A state change needs 500 ms of stable readings so small ADC noise around 25% does not chatter. A raw A0 value of 20 or less is treated as an invalid rail-low sensor reading: green stays OFF, red gives a fast double flash, the Status page says `CHECK SOIL A0`, and serial prints `soil_state=FAULT`. STOP/lockout makes red solid; lamp test lights all three LEDs. Soil state never starts a pump dose automatically.

## LCD backlight timeout — UI v6

Keep LCD VCC connected to the Uno **5 V** supply and LCD GND to GND. Do **not** wire VCC to D10: the Uno R3 pinout specifies a 20 mA maximum per I/O pin, and this module's total LCD plus backlight current has not been measured. UI v6 uses the I²C backpack's backlight command, so LCD logic remains powered. The backlight goes off after 60 seconds without button use or a significant A1 knob movement (at least eight ADC counts). It wakes on any button press or knob movement. A pump request keeps it on, and completion or cancellation restarts the full 60-second interval at pump stop. Serial logs each successful backlight state change. If the LCD does not initialise, no backlight behaviour is claimed; inspect the intermittent LCD supply/I²C fault if status `-4` recurs. A full VCC power cut would need a rated switch and a design check for I²C back-powering before wiring it.

## Relay and pump circuit — rating and reset checks open

Use a **relay module with a logic input and onboard coil driver**, not a bare relay coil on D9. Confirm that a 5 V HIGH from the Uno meets the module's trigger specification without exceeding the D9 output-current limit. Power the module coil from a verified 5 V supply with enough current; connect its logic GND to Uno GND as its datasheet requires. Check the module's coil suppression and behaviour when its logic lead is open, during Uno reset and when either supply starts first. Provide an external D9-to-GND pull-down if needed for a measured default OFF state throughout boot. A sketch cannot control D9 during the bootloader interval.

The relay's **normally-open contacts** switch the pump's *separate, correctly rated* DC supply: supply positive → fuse/disconnect → COM → NO → pump positive; pump negative → supply negative. The contact circuit does not take pump power from D9, the Uno 5 V pin, or its 3.3 V pin. Size the supply, fuse, contacts, wiring and flyback suppression from the identified pump's operating and startup/stall current. For an ordinary brushed DC pump, verify a suitable diode or other suppression directly across the motor, polarity correct, and check its effect on contact release. Keep a physical power disconnect; a software STOP cannot interrupt welded contacts or a hung controller.

`RELAY_ENABLED` is `true` at the user's direction. `RELAY_TRIGGER` is set to `ActiveHigh` from the user's report. The operator reports a working pump path, but module identity, rated currents, supply voltage under load and contact state through reset have not been recorded. This is a supervised manual-dose system, with no automatic watering or proven volume calibration.

## Revised interface checks

1. With power removed, verify red/black as each switch pair by continuity: open released, closed pressed. Verify green as LED+ and yellow as LED− for each button using its part marking or a current-limited test. Identify each lamp's current-limiting arrangement separately. Record button part identifiers and ratings.
2. With the pump supply OFF, read back the revised sketch and confirm `relay=OFF` at rest. Press/release each button while watching serial. The v6 LCD initialised at status `0`, but earlier runs returned `-4` or lost write communication. Check supply stability, ground, A4/A5 and relay/pump suppression under load before treating screen pages as accepted. Sweep A1 from lowest to highest and verify that Status sets 1.0–4.0 seconds.
3. With a valid sensor reading, verify red blinks below 25% and green stays on at 25% or above; hold each side of the boundary for at least 500 ms. During a dose yellow lights and the moisture lamp retains its state. At pump stop, the screen should immediately return to the soil percentage, including if WATER remains held; release is still required for another dose. STOP cancels and makes red solid during lockout. Yellow lights all three while held and cycles the LCD pages. Hold STOP for two seconds to clear session counts. With A0 rail-low, check fast double red flash and `soil_state=FAULT`; do not interpret raw zero as wet.
4. With the pump supply OFF, verify the identified relay module's input current, HIGH=ON, LOW=OFF, and contacts OFF through power-up, reset and supply sequencing. Record any transient contact closure. For a supervised powered trial, measure the actual 1.0 and 4.0 second endpoints and delivered volume.
5. With LCD initialisation status `0`, leave the controls untouched for 60 seconds and observe `LCD backlight=OFF idle`. Press a button or move the knob by at least eight ADC counts and observe `LCD backlight=ON activity`. Finish or cancel a dose and verify the full 60-second interval starts again at pump stop. The LCD's 5 V wire stays on the 5 V terminal throughout.

The R14 assembly manual's bench results and source snapshot do not verify this revised wiring or the purchased hardware. Maintain a new build/test record rather than overwriting the historical one.

## Current UI v6 backlight upload record

On 27 September 2026, UI v6 compiled for `arduino:avr:uno` using 14,950 bytes of flash and 870 bytes of global RAM. After the operator confirmed the separate pump supply OFF, Arduino CLI uploaded it to the CH340 Uno on COM8. SHA-256 of `PlantUno.ino`: `0B702102A4EF74E1B1D6970B161125E77A69A9E28F2DA299324B71A1908D146F`.

Serial startup identified `PlantUno UI v6; relay HIGH; dose 1000..4000ms; LCD backlight idle 60s`. LCD initialisation returned `0`. With controls untouched, serial logged `LCD backlight=OFF idle` just after `t=60000`; a subsequent A1 movement (pot raw about 1016 to 964) logged `LCD backlight=ON activity`. Serial reported `relay=OFF` throughout. This verifies controller commands and I²C acknowledgement, not a direct visual observation of the backlight. Pump completion was not triggered in this check, so the post-dose timer reset remains to be observed. The previous intermittent LCD faults also remain open.

## Previous soil-return display upload record

On 27 September 2026, the UI v5 sketch compiled for `arduino:avr:uno` using 14,408 bytes of flash and 862 bytes of global RAM. After the operator confirmed the separate pump supply OFF, Arduino CLI uploaded it to the plant Uno on COM8. SHA-256 of `PlantUno.ino`: `E18A0A637255EE7214697E45D8E5005621363259B77CAAF760D99939AFBD0308`.

Serial startup identified `PlantUno UI v5; relay HIGH; dose 1000..4000ms; soil after dose`. At rest over approximately 1–10 seconds, raw soil was 454–455 (`0%`, `soil_state=DRY`), WATER/LAMP/STOP each read 0, `request=0` and `relay=OFF`. LCD initialisation returned `-4`; no dose was requested during this readback, so the immediate post-dose display has not been physically observed. The controller still requires a stable all-button release before another dose.

## Previous 25% lamp UI v4 upload record

On 27 September 2026, the 25% soil-indicator sketch compiled for `arduino:avr:uno` using 14,528 bytes of flash and 904 bytes of global RAM. After the operator confirmed the separate pump supply OFF, Arduino CLI uploaded it to the plant Uno, now enumerated as USB CH340 on COM8. SHA-256 of `PlantUno.ino`: `D5BEA386847DB1E126E490B675D9DDA22BF7BDBA945A2074FBD4533AC9108FEB`.

Serial identified `PlantUno UI v4; relay HIGH; dose 1000..4000ms; dry below 25pct`. At rest, raw soil was about 453 (`0%`, `soil_state=DRY`), all three buttons read 0, `request=0`, and `relay=OFF`. A physical WATER input was subsequently read as 1 with the pot near maximum; the sketch requested 3,975 ms and serial reported `relay=ON`, then `DOSE COMPLETE` and `relay=OFF`. The physical pump supply state at that later button press and actual relay contact/pump operation were not measured by this readback.

LCD initialisation returned `0`, followed by `LCD write failed` during the request and `lcd=FAULT` thereafter. Raw soil moved from about 453 dry to 208 (displayed 100%, `soil_state=WET`) and back to 443 (displayed 1%, `soil_state=DRY`) over the next roughly 25 seconds. This shows the software classification and 25% crossing, not a measured soil moisture change or a visual check of the button lamps. Correlate A0 readings with actual sensor position, wiring and supply before treating the index as plant moisture. No independent timing or volume measurement was made.

## Previous 1–4 second UI v3 upload record

On 27 September 2026, the revised sketch compiled for `arduino:avr:uno` using 13,986 bytes of flash and 861 bytes of global RAM. Arduino CLI uploaded it to the USB serial Uno on COM9 with the separate pump supply OFF. SHA-256 of `PlantUno.ino`: `72CD3DD4A3E21A96920D6ACA3EED329EB099DFBAC1F97C060491FF8E1E9BF676`.

Serial startup identified `PlantUno UI v3; relay HIGH; dose 1000..4000ms`. At rest for approximately 1–20 seconds, WATER/LAMP/STOP each read `0`, `request=0`, `relay=OFF`, and page `1`. The pot read approximately 120–123 of 1023 and soil read `0`. LCD initialisation returned `-4` and serial reported `lcd=FAULT`. The 1–4 second physical run time, new screen pages and button actions have not yet been checked on this upload. The browser demonstration is not connected to the Arduino.

## Previous one-second upload record

On 27 September 2026, the active-HIGH relay-trial sketch compiled for `arduino:avr:uno` using 12,546 bytes of flash and 658 bytes of global RAM. Arduino CLI uploaded it to the currently detected CH340 Uno on COM9; the upload exited successfully. SHA-256 of `PlantUno.ino`: `CB81B818E8B05F1232051A40C5416ECB9499EBC4F85AAEEF562B9A6C8EA6A40A`.

Post-upload serial startup identified `PlantUno relay trial; max 1000ms`. LCD initialisation returned `-4`. From approximately 1–11 s after reset, readback showed WATER/LAMP/STOP `0`, `request=0`, `relay=OFF`, pot raw approximately 85–86 and soil raw `0`. These are software readbacks, not measured pin voltage or proof of peripheral wiring. No button press, relay-contact measurement or powered pump run was performed by this upload.
