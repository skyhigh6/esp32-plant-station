# Requirements and configuration control

P0 · 2026-09-08 · Accountable integrator: Demerzel workflow

## Scope and traceability

| ID | Requirement / proposed decision | Status | Evidence / acceptance |
|---|---|---|---|
| R01 | ESP32 controller, moisture sensor and LCD | Requested | Exact models unknown; E01–E03 |
| R02 | Small 5 V pump | Requested | Nameplate/current/head unknown; E04 |
| R03 | Exactly three buttons and three LEDs; retain lamp test and water functions | Requested update; third-button/LED roles proposed | F01–F05 |
| R04 | Printed pot with integrated lower sump containing pump | Requested | M01–M05 |
| R05 | Approximately 90 × 60 × 50 mm internal planting space; exactly two floor drains into sump | Requested; internal interpretation provisional | M01/M03 |
| R06 | Left electronics tower, LCD aperture/mount, three buttons/LEDs and dose potentiometer; accessible cover | Requested; front defined as LCD viewing face | M01/M05 |
| R07 | Research ESP32 carrier mounting dimensions and provide mount | Requested; SunFounder brand confirmed; exact camera carrier revision unknown | Mechanical source register; actual board measurement still required |
| R08 | LCD mounting-hole centres 73 × 30 mm and display cutout 70 × 25 mm | User measured; horizontal 73 / vertical 30 is landscape orientation assumption | M01 actual fit; hole diameter/PCB/backpack envelope still unknown |
| R09 | SunFounder ESP32 camera carrier hole centres X = 60 mm, Y = 55 mm | User measured; NOT 60 × 60 mm; no independent metrology | M01 mount fit; carrier hole diameter/outline/components still unknown |
| R10 | Potentiometer adjusts dose per watering-button press | Requested update | E06/F01/F08; actual flow calibration |
| R11 | Include 18650 cell and 5 V PCB sounder | Requested; chemistry/power management and sounder type unknown | E07/E08; default outputs disabled |
| R12 | Carrier mount/enclosure permits USB connector and cable insertion | Requested | M06 actual plug/strain relief check |
| D01 | One bounded timed dose per press; third button STOP | Proposed; supersedes hold-to-water | F01/F08 |
| D02 | Bounded maximum run, release to re-arm; dose setting captured at start | Proposed editable configuration | F02; volume check E04 |
| D03 | Lamp test never energises pump; inhibit restart until release | Proposed | F03 |
| D04 | Hardware pull-down and software off at boot/reset | Proposed safeguard | E05/F04 |
| D05 | No moisture-triggered automatic watering | Scope boundary | Source inspection/F05 |
| D06 | Recirculate soil drainage into pump sump through exactly two holes | Requested update supersedes initial separated-drainage proposal | M03; inspect/clean debris guards and pump |

## Unknowns requiring evidence

| ID | Unknown | How to close |
|---|---|---|
| U01 | ESP32 exact carrier revision, power input, exposed pins, outline/component envelope and hole diameter | User measured mounting centres X60/Y55 mm; historical photo available; obtain matching manufacturer pinout/schematic and reserve camera/SD pins where fitted |
| U02 | LCD controller, backpack mapping, supply and pull-up voltage; hole diameter and PCB/backpack envelope | QAPASS/PCF8574 visible in historical photo; user measured hole centres 73 × 30 mm and confirmed display cutout 70 × 25 mm; measure remaining geometry and idle SDA/SCL voltage |
| U03 | Sensor type, supply, output range and wetting limits | Datasheet; measure dry/wet output at proposed supply; calibrate in actual soil |
| U04 | Pump motor type, startup/stall current, dimensions, submersion limits, head/flow | Datasheet and current-limited bench measurements; avoid unsafe sustained stall |
| U05 | Tubing bore/outer diameter, outlet fit, bend radius | Measure actual tube/barbs and test retention |
| U06 | Pot/plant size, usable reservoir capacity, watering dose | Plant requirements, physical dimensions, measured delivery at installed lift |
| U07 | Printer envelope, material, dimensional error, watertightness | Printer specification, fit coupon, leak test or compatible liner |
| U08 | Supply transient capability, cable losses, fuse/switch ratings | Select from measured startup and normal current; verify under load |
| U09 | 18650 cell chemistry, capacity, discharge rating, protection, holder size and charger/power-path compatibility | Read cell and board markings; obtain matching datasheets/schematic; no cell wiring/charging approval from form factor alone |
| U10 | Sounder active/passive type, current, polarity and envelope | Identify part; verify required driver and supply; keep output disabled until confirmed |
| U11 | Button, LED, potentiometer and USB cable dimensions | Measure actual panel fittings/plug/strain relief; print test-fit fascia and mount first |

## Options and recommended path

| Decision | Options and trade-offs | P0 recommendation |
|---|---|---|
| Water command | Timed dose continues after release and needs a distinct stop path; hold-to-water gives direct duration control | Timed dose per user update; proposed STOP third button and lamp-test inhibit |
| Wet parts | Bare print needs sealing/leak validation; removable liner adds fit work but provides a separate water barrier | Prototype geometry, then use a compatible liner or validated coating and leak test |
| Drainage | Recirculation returns soil/fertiliser to pump and requires accessible debris guards and cleaning; separate collection needs changed scope | Recirculating lower sump as requested; record blockage and water-quality checks |
| LCD | Reuse existing backpack after identification; known 3.3 V interface reduces electrical ambiguity | Identify existing LCD before choosing adapter/library |

## Risks and limits

Software cannot guarantee pump shutdown after a processor hang or a shorted power transistor. The time limit is a software control, not an independent cut-off. An accessible pump power disconnect, physical leak containment and supervised commissioning remain necessary; consider an independent timed power cut-off if unattended use becomes a requirement. No unattended-operation claim is made.

No reservoir level sensor is specified: dry-run prevention relies on operator checks and the actual pump's limits. Repeated button presses can still overwater. A sensor reading cannot prove that soil needs a particular volume. Exactly two drainage holes can become blocked: retain access for clearing them and prevent soil loss with removable guards. Leave sump headspace for drain-back and never allow maximum fill to reach the soil floor. Plant photograph recovered; species identity and suitability for the requested small planting volume remain unknown.

Keep electronics above spill paths with cable drip loops, a removable dry enclosure and strain relief. Printed walls and cable openings are not an ingress-protection rating. Use low-voltage wet-area wiring; keep any mains adapter away from water.

## Change control

Record future changes with date, affected requirement, reason, component/CAD/firmware revision, and checks repeated. Close unknowns with measured values or manufacturer evidence; do not replace UNKNOWN with an unlabelled assumption. Archive accepted configurations before hardware changes.




## 2026-09-09 - Mechanical R5 and build guide

R05/R06/R08/R09/R12: concept-based R5 exported with seven STL/STEP parts, zero volumetric interference in all 21 solid pairs, LCD standoffs and checked PCB tool access. Measured centres/aperture preserved. Actual component envelopes and USB fit remain unresolved. Use mechanical/concept_rev5/README.md and verification.json for current mechanical authority; earlier mechanical insert/fit instructions are superseded. The illustrated PDF records the logical review-only pinout and conditional upload procedure; no upload performed. Existing firmware recompiled against ESP32 core 2.0.17 (272957 flash bytes, 21944 global RAM bytes); LCD text functionality remains unimplemented.

## 2026-09-11 - Mechanical R6: sump pump and button inserts

R03/R04/R05/R06: user requested revised STLs for pump accommodation and 12 mm button inserts, with purchase screenshot. R6 supersedes R5 mechanical dimensions for the sump, planter and hose clip. Sump external height 60 mm/internal depth 56 mm; planter raised 20 mm; three nominal 12 mm fascia holes retained and insert clearance checked for provisional 20 mm nuts/35 mm rear projection. Pump reference is the previously shortlisted 38.5 × 25.5 × 43 mm COM3700 envelope, not measured hardware. Rear hose/cable opening extended through skirt; clip bore 8.4 mm. Seven assembly STLs/STEPs plus three-diameter fit coupon exported. All 21 CAD assembly intersections zero; eight meshes independently checked, including fascia/coupon sections. Tower, fascia, top cover and battery tray STL hashes equal R5. Actual pump identity, insert variant/depth/nuts, component fit and leak tests remain open. See mechanical/concept_rev6/README.md and both verification records. No firmware change, printer operation or publication performed.
