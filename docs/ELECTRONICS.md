# ESP32 Plant Station Electronics - Initial Engineering Package

## Scope

This is a bounded provisional electronics package for an ESP32 plant station with:

- soil moisture sensor input;
- LCD status display;
- small 5 V DC pump;
- water button;
- lamp-test button;
- three status LEDs (red, blue and proposed green);
- third button proposed as STOP (function unconfirmed);
- dose potentiometer;
- supplied 5 V PCB sounder (active/passive type unknown).

The design is manual-only. There is no networking, automatic watering, flash storage, cloud dependency, or scheduled pump action in this package.

## Hardware Status

| Item | Status |
|---|---|
| ESP32 board variant | SunFounder brand confirmed; exact ESP32 camera extension/carrier revision unknown |
| Soil sensor type | Unknown |
| LCD module/backpack | Unknown |
| Pump voltage/current/startup current | Unknown |
| Pump supply | Unknown |
| MOSFET part | Unknown |
| Button wiring | Provisional |
| LED resistor values | Provisional |

The firmware has no default board pin map. A classic ESP32 DevKit / ESP32-WROOM-32 map is retained only as an opt-in review profile for compiling the controller scaffold. It is not applicable to the SunFounder camera extension/carrier board unless the exact board schematic proves every selected pin is free and electrically suitable.

Camera/SD boards may reserve GPIOs for camera data, camera clock, SCCB/I2C camera control, SD card, PSRAM, flash, onboard LEDs, buttons, or power enables. Treat all pins as unavailable until the exact board variant is identified.

## Primary ESP32 Electrical References

The current Espressif primary documents checked for this package were:

- [ESP32-WROOM-32 Datasheet](https://documentation.espressif.com/esp32-wroom-32_datasheet_en.pdf)
- [ESP32-WROOM-32E / ESP32-WROOM-32UE Datasheet](https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf)
- [ESP32 Series Datasheet](https://documentation.espressif.com/esp32_datasheet_en.pdf)
- [ESP32 Hardware Design Guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/index.html)
- [SunFounder ESP32 Camera Extension candidate reference](https://docs.sunfounder.com/projects/esp-cam-kit/en/latest/component_esp32_extension.html)

Key points used here:

- ESP32 module supply is a 3.3 V design, with module VDD maximum ratings around 3.6 V depending on the exact module document.
- GPIO input high is referenced to the IO power domain, with maximum input levels not allowing direct 5 V signalling.
- ESP32-WROOM modules identify strapping pins including GPIO0, GPIO2, GPIO5, GPIO12/MTDI, and GPIO15/MTDO. Avoid using these for buttons or pump control in a first-pass build.
- GPIO drive capability is limited and intended for logic loads. Do not drive a pump, relay coil, motor, or high-current lamp directly from an ESP32 pin.
- Espressif hardware guidance expects proper local decoupling and supply design; USB board power may not tolerate motor startup current or noise.
- SunFounder documents an ESP32 Camera Extension combining an ESP32 WROOM 32E, OV2640 camera, Micro SD, battery interface, GPIO headers, and screw terminals. This matches the recovered photo evidence, but the exact revision still needs confirmation.

## Recovered Photo Evidence

Photos in `evidence/prior-uno/` show:

- `photo-8.jpg`: SunFounder-style ESP32 camera extension/carrier with a central ESP32-WROOM development board, camera FPC connector, Micro SD socket, GPIO headers, and screw terminals.
- `photo-5.jpg`: LCD back marked `QAPASS`, with PCF8574T I2C backpack and GND/VCC/SDA/SCL header.
- `photo-9.jpg`: capacitive soil moisture sensor marked `Capacitive Soil Moisture Sensor v1.2`, with AOUT, VCC, and GND.

These photos improve component identification, but they do not close the carrier-board pin map. Camera and SD nets must be reserved from the actual SunFounder circuit, not inferred from a generic ESP32 pinout.

## Isolated Candidate Pin Map - Classic DevKit/WROOM-32 Review Only

The following map is not the current hardware baseline. It exists only to keep the firmware scaffold compile-reviewable against a common ESP32 DevKit/WROOM-32 profile.

| Function | Provisional ESP32 Pin | Notes |
|---|---:|---|
| Soil sensor analogue output | GPIO34 | Input-only ADC-capable pin. Sensor output must remain within 0-3.3 V. |
| Pump MOSFET gate | GPIO25 | Output to MOSFET gate resistor only, never directly to pump. |
| Red status LED | GPIO26 | Use series resistor. |
| Blue status LED | GPIO27 | Use series resistor. |
| Water button | GPIO32 | Use `INPUT_PULLUP`; button to GND. |
| Lamp-test button | GPIO33 | Use `INPUT_PULLUP`; button to GND. |
| I2C SDA | GPIO21 | Common ESP32 default; check board schematic. |
| I2C SCL | GPIO22 | Common ESP32 default; check board schematic. |

Avoid using boot strapping pins for this first build. If the physical board is a camera extension/carrier board, stop and create a specific pin map from the exact board schematic before connecting the pump stage.

## Physical Layout Constraint

The plant pot internal space is 90 mm x 60 mm x 50 mm with exactly two drain holes into a lower pump sump. The electronics tower is on the left and carries the LCD plus three buttons and a potentiometer.

Implications:

- drainage is recirculating, so debris and soil fines can return to the pump sump;
- add a removable inlet filter or coarse screen before the pump;
- design access for cleaning the sump, pump inlet, and drain holes;
- keep electronics above splash height and isolated from the sump;
- route wiring with drip loops and strain relief;
- do not place the pump driver board below any likely overflow or cleaning water path.

## Provisional Wiring

### ESP32 Power

- Power the ESP32 from USB or a known-good regulated 5 V input intended for the development board.
- Do not power the pump from the ESP32 3.3 V pin.
- If sharing a 5 V supply between ESP32 board input and pump, size it for ESP32 current plus pump running current plus pump startup current margin.
- Tie ESP32 GND and pump supply GND together at a controlled common point.

### Pump Driver

Use a low-side N-channel logic-level MOSFET driver:

- pump positive to external 5 V pump supply;
- pump negative to MOSFET drain;
- MOSFET source to GND;
- ESP32 GPIO25 to MOSFET gate through a small series resistor, provisionally 100-220 ohm;
- MOSFET gate to GND through a pull-down resistor, provisionally 47-100 kOhm;
- flyback diode across the pump, cathode to +5 V and anode to MOSFET drain;
- optional local electrolytic capacitor near pump supply, sized after measuring startup behaviour.

The MOSFET must be suitable at 3.3 V gate drive. Confirm low Rds(on) at Vgs = 2.5-3.3 V, drain current rating, thermal margin, and package heat dissipation. Do not use a bare small-signal transistor unless the pump current proves it is within rating with margin.

### Buttons

Provisional arrangement:

- one side of each button to ESP32 input pin;
- other side to GND;
- firmware uses internal pull-ups;
- optional external 10 kOhm pull-up to 3.3 V if wiring is long or noisy;
- never pull ESP32 button inputs to 5 V.

The firmware debounces WATER before one timed dose. Releasing WATER does not stop that dose. Proposed STOP and LAMP TEST cancel immediately; see firmware behaviour below.

### LEDs

Provisional arrangement:

- GPIO26 -> resistor -> red LED -> GND;
- GPIO27 -> resistor -> blue LED -> GND;
- start with 1 kOhm for low-current indication, then adjust only after checking LED current and brightness;
- do not exceed GPIO current limits.

Add the third LED with its own resistor (proposed green ready). Lamp-test turns on all three LEDs and never requests pump output.

### Soil Sensor

Because the sensor type is unknown:

- sensor VCC must be compatible with the sensor output and ESP32 ADC limit;
- analogue output into GPIO34 must stay in the 0-3.3 V range;
- if the sensor is a 5 V module with possible 5 V analogue output, use scaling or a 3.3 V-compatible sensor;
- resistive exposed-prong probes can corrode if powered continuously, so consider switched sensor power in a later revision.

Calibration must be performed in the actual pot and soil. Treat raw readings as installation-specific.

### LCD / I2C

The LCD adapter is disabled by default. Explicit `PLANT_LCD_ENABLE`, `PLANT_LCD_BACKPACK_PCF8574` and `PLANT_LCD_I2C_ADDRESS` gates now provide a safe address-probe path. HD44780 writes remain disabled until the photographed backpack bit mapping is confirmed.

Many 16x2 LCD I2C backpacks are 5 V PCF8574-style modules with pull-ups to VCC. If the backpack is powered at 5 V and pulls SDA/SCL to 5 V, use bidirectional I2C level translation between the ESP32 and LCD. Do not connect 5 V I2C pull-ups directly to ESP32 GPIO.

Before enabling LCD code, identify:

- LCD controller/backpack type;
- I2C address;
- VCC requirement;
- existing pull-up resistor destination;
- whether level shifting is already present.

Current photo evidence identifies a QAPASS LCD module with a PCF8574T backpack. The I2C address and pull-up destination remain unmeasured. If VCC is 5 V and the pull-ups go to 5 V, use bidirectional I2C level translation.

## Added controls, sounder and battery

The third button function is unconfirmed: STOP is proposed because WATER now triggers a timed dose. The potentiometer adjusts duration as a proxy for water amount; it is sampled once at start. Wire pot ends to 3.3 V/GND and wiper to a suitable ADC input, never 5 V. Pot resistance and mechanical details remain unknown. Provide a wiper pull-down selected for the actual pot value and verify open-wiper behaviour before enabling the pump; filtering and endpoint calibration must account for its loading. An open wiper must not silently select a maximum dose.

The direct-I/O budget is **12 GPIOs**: two ADC inputs (soil and pot), three button inputs, three LED outputs, pump gate, sounder driver, and two I2C lines. This excludes every camera/SD/peripheral reservation. No approved mapping exists for the actual SunFounder carrier; a GPIO expander for buttons/LEDs may be required after schematic review. Keep the pump gate on a suitable direct GPIO with a physical pull-down.

The compile-only classic profile adds GPIO35 pot ADC, GPIO13 STOP, GPIO14 green LED, and GPIO23 sounder gate to the table above. These are NOT wiring instructions for the supplied camera carrier. GPIO13/14 also conflict with JTAG use. Every carrier net must be checked before adopting any pin.

The supplied 5 V PCB sounder is not identified as active or passive. The sketch keeps its driver output low by default; enable and select an active/passive mode only after identification. Use a separate appropriately rated transistor/MOSFET driver and gate/base bias; never power it directly from a GPIO. Confirm current, polarity, required waveform and whether it is magnetic or piezoelectric; inductive loads need suppression. No audible alarm is claimed until those checks pass.

The supplied cell is described as an 18650 and called “LiPo”. Chemistry, exact part, protection, polarity, allowed charge current and the carrier charging circuitry are UNKNOWN. The description does not establish any of these. Do not assume the carrier charges it safely, connect it for charging, or assume a cell can directly supply the 5 V pump. Identify cell and carrier schematic first; establish charger/protection, regulated rails and load/current budgets. Use a known regulated bench/USB supply for initial electronics checks with the battery isolated.

## Firmware behaviour and acceptance checks

See `firmware/README.md` for the current behaviour and build commands. WATER starts one 0–5000 ms provisional dose after 35 ms debounce. Pot is sampled once at start. Release does not cancel an active dose. STOP or LAMP TEST cancels on the next loop; lamp test illuminates all three LEDs. After completion/cancellation, all buttons must remain released for 35 ms before another press is accepted. Held buttons and presses during a dose cannot queue more water. Boot-held controls are locked out until stable release. Zero pot setting runs no pump. Pump output is disabled by default; LCD and sounder are disabled.

1. Compile the isolated review target and run host assertions when a native compiler is available. Compilation alone does not verify physical operation.
2. Close the actual carrier pin map and supply/driver review before any wiring or output enable.
3. With pump disconnected, verify all three controls, boot-held lockout, pot extrema, fixed duration after knob changes, no repeat on hold, and stable release/repress.
4. Verify STOP and lamp test cancel doses; check all three LEDs and measure pump gate LOW at boot/reset. Blue indicates a software request, not confirmed flow.
5. On a controlled bench, check startup current, voltage sag, driver heating and noise/reset behaviour. Add current limiting/fusing suitable for the measured load.
6. Calibrate delivered volume using installed tubing/head and repeated timed collections before marking ml. No flow rate or delivered volume is currently known. Reduce the provisional time cap for first wet tests.
7. Confirm splash isolation, drip loops, strain relief and sump cleanability before installing electronics.

Software timing requires the loop to keep executing. A processor stall or failed MOSFET can defeat the software cap; this is not a hardware safety cutoff. There is no reservoir-level or flow feedback, dry-run protection, autonomous watering or remote control in this scaffold.

## Open items

Actual carrier revision/schematic and free pins; third button and third LED functions; sounder identification/driver; battery chemistry/protection/charging; pump current and flow calibration; pot value and open-wiper behaviour; LCD address and pull-up voltage; measured soil-sensor output range. Photo evidence identifies the QAPASS/PCF8574T LCD and capacitive v1.2 probe visually, without electrical verification.

