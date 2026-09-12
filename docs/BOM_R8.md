# R8 bill of materials

One build; provisional fit-trial selections, not released purchasing specifications.

## Fasteners

| Qty | Provisional selection | Location and engagement constraint |
| --- | --- | --- |
| 4 | 3 x 8 plastic thread-forming pan head | Fascia: 3 panel + 5 pilot engagement; 2.8 pilots, 9 deep. |
| 4 | 3 x 8 plastic thread-forming pan head | Carrier: assumed 1.6 PCB + 6.4 engagement; 2.8 pilots, 11 deep. Verify PCB holes and underside insulation. |
| 4 | 3 x 8 plastic thread-forming pan head | Roof: 3 cover + 5 engagement; 7 deep pilots. Narrow wall: hand tighten. |
| 2 | 3 x 6 plastic thread-forming pan head | Battery tray: 3 tray + 3 engagement; 4 deep pilots. |
| 1 | 3 x 6 plastic thread-forming pan head | Hose clip: 4 clip + 2 engagement; only 3 deep pilot. Do not use 8 mm screw here. |
| 4 + 4 | M2.5 x 16 machine screws + M2.5 nuts | LCD: underhead plane y=1; printed stack to y=12, assumed PCB 1.6. Head OD <=5.5; verify nut access and thread projection. |
| 3 sets | Button supplied nuts/washers | 12 mm panel insert, 3 panel; provisional nut OD <=20, rear body <=35. |
| 1 set | Pot supplied nut/washer | 7 mm provisional panel bore; confirm actual bushing before purchase. |

12 x 3 x 8 and 3 x 3 x 6 plastic thread-forming screws total; allow two spares of each type. LCD: four screws and four nuts. Verify engagement on actual stacks.

## Electronics

| Qty | Item | Specification / open evidence |
| --- | --- | --- |
| 1 each | SunFounder carrier + ESP32 module | Carrier drawing reference only; identify board/module revision and pin reservations. |
| 1 | LCD with I2C backpack | 80 x 36 reference PCB, 75 x 31 holes; identify supply, pull-ups and backpack depth. |
| 1 | Capacitive moisture sensor | Identify output range; calibrate in the actual pot. |
| 1 | 5 V pump | Reference body 38.5 x 25.5 x 43; verify actual outlet, current and submersion. |
| 3 | Momentary panel buttons | 12 mm nominal; WATER, LAMP TEST, proposed STOP per current project record. |
| 3 + 3 | LEDs + individual series resistors | Nominal 5 mm bodies; determine polarity/current and resistor values from actual parts. |
| 1 | Linear potentiometer | Value, shaft, bushing and travel unknown; use 3.3 V ADC-compatible circuit. |
| 1 | 10 mm round piezo buzzer | User diameter; active/passive, height, rating and driver remain unknown. |
| 1 set | Pump driver and flyback protection | 3.3 V-compatible MOSFET drive, gate resistor/pull-down; size from actual motor. |
| As needed | I2C translator and sounder driver | Required where actual electrical levels/current require them. |
| 1 each | 18650 cell + insulated holder | Verify chemistry/protection/current and holder fit; printed tray is not bare-cell contacts. |
| 1 set | Power path, fuse, disconnect, wiring | Confirm charger/boost compatibility, USB isolation and pump startup capacity. |

## Printed and consumable materials

Seven enclosure parts plus one selected knob. Six fit coupons and optional USB marking blank. Compatible adhesive, insulating sleeves, terminals/wire, cable ties and anchors, tube to measured length, outlet adapters, removable screens and wet-side liner/coating if required. See ASSEMBLY_GUIDE_R8.md for dimensions, quantities, glue process, print orientations and acceptance gates.
