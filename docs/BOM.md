# Provisional bill of materials

**Superseded for the current build by [R8 BOM and fastener schedule](BOM_R8.md), 12 September 2026.** The following P0/R7 inventory is historical; use R8 for USB orientation, piezo mounting, knob options and fasteners.

P0 review only. Quantities describe the concept, not a purchase list. Existing kit contents are not inventoried beyond the user statements and historical photographs.

| Qty | Item | Selection / unresolved evidence |
|---|---|---|
| 1 | SunFounder ESP32 camera extension board/controller | Exact physical revision/pinout unverified; R7 manufacturer reference: 67 × 64 mm PCB, 60 × 57 mm centres; both USB ports upwards, offsets unconfirmed |
| 1 | Character LCD and I2C backpack | R7 supplied diagram: PCB 80 × 36 mm, centres 75 × 31 mm, holes 3 mm; aperture 71.4 × 24.6 mm; actual backpack depth unverified |
| 1 | Capacitive moisture sensor | Historical v1.2 marking; supply/output limits and real-soil calibration unverified |
| 1 | Small 5 V pump | Dimensions, motor type, startup current, head, flow and dry-run limits unknown |
| 3 | Normally open momentary buttons | Proposed WATER/LAMP TEST/STOP; 12 mm nominal panel holes requested; purchased variant, nut and depth require fit check |
| 3 | LEDs and individual series resistors | Proposed red/blue/green; 5 mm holes, initial 1 kΩ resistors provisional |
| 1 | Linear potentiometer | Resistance, shaft and travel unknown; powered from 3.3 V; 7 mm panel hole provisional |
| 1 set | Pot wiper bias/filter components | Choose after pot value; verify an open wiper cannot select maximum dose |
| 1 | Pump power MOSFET | On-resistance specified at 3.3 V or lower gate drive; current/thermal rating from measurements |
| 1 each | Pump gate resistor and pull-down | Provisional 100–220 Ω and 47–100 kΩ respectively |
| 1 | Pump flyback/suppression device | For actual motor type; current/reverse-voltage rating from evidence |
| 1 | Bidirectional I2C level translator | Required if LCD pull-ups are at 5 V; verify both rail pull-ups |
| 1 | 5 V PCB sounder | Active/passive, current, polarity, mounting pattern unknown |
| 1 set | Sounder driver and bias/suppression | Select from actual sounder; disabled scaffold output |
| 1 | Supplied 18650 cell | Chemistry, protection, capacity, current rating and condition unknown |
| 1 | Insulated cell holder | Actual envelope/contacts unknown; printed cradle retains a holder, not bare-cell contacts |
| TBD | Compatible charger, protection and regulated 5 V power path | Do not assume carrier provides these; verify USB/battery isolation and charging chemistry |
| 1 set | Supply fuse/current protection, disconnect, decoupling and wiring | Size for startup current, cable loss and fault energy; no pump current through GPIO |
| TBD | Tubing, outlet elbow/clip, debris screens and liner/seal | Nominal 8 mm OD tube placeholder; exactly two drains; verify leak/siphon/retention |
| 7 | Printed parts | See ../mechanical/concept_rev7/independent_mesh_check.json; seven assembly parts plus three fit coupons, mm; prototype only |
| TBD | Insulating spacers, screws/inserts, ties, glands and strain relief | R7 carrier pilots 2.8 mm; LCD bores 3 mm, screw heads at most 5.5 mm; verify actual fasteners and insulating clearance |

Power sizing must include simultaneous controller/LCD/three-LED/sounder demand and pump startup, not just its running current. For a future boost supply, approximate input current is output power divided by (minimum cell voltage × converter efficiency); use actual rated values and transient measurements. No runtime or battery compatibility claim is made.
