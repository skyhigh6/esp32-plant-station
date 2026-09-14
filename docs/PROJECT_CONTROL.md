# Requirements and configuration control

## Current mechanical change - R13, 14 September 2026

R13 supersedes R12. All five browser annotations are addressed; see ../mechanical/concept_rev13/README.md and the two R13 PDFs. Four main parts. Sensor entry lower edge at z60 is a geometric datum, not a fill mark. Existing electrical release gates remain open.

## Historical mechanical change - R8, 12 September 2026

R8 supersedes the older dimensions below for manufacture preparation. Carrier reference pattern is 60 x 57 mm, rotated 90 degrees anticlockwise from R7 as viewed from the fascia to 57 horizontal x 60 vertical, with USB ports facing left. LCD pattern remains R7 75 x 31 mm. Roof access hole closed; provisional left window 28 x 20 mm requires actual cable measurements. Upper fascia bosses have continuous side-wall webs. User specifies a 10 mm round piezo, glued in, and glued LEDs. Eight knob bore options are supplied because shaft size is unknown. Current R03/R06 three-button requirement is retained; no firmware change.

See [R8 dimensional contract](../mechanical/concept_rev8/README.md), [assembly route and first article record](ASSEMBLY_GUIDE_R8.md), and [current BOM](BOM_R8.md). Historical R08/R09 and U01/U02 dimensions below are superseded by R7 references and the R8 installed orientation. USB position, shaft fit, piezo height, actual fastener retention, slicing and physical acceptance remain OPEN.

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

## 2026-09-11 - R6-A1 concept and assembly documentation

User requested updated concept art, illustrated assembly documentation and GitHub publication. Added generated appearance art based on the R6 CAD reference, with prompt/provenance and explicit limits; eight-page PDF and corresponding Markdown guide; 15 assembly steps and acceptance worksheet. PDF pages rendered and visually reviewed; six source links embedded. R6 STL hashes checked unchanged. Mechanical/electrical fit gates remain open; LCD text and illuminated rings in the image are illustrative. Complete illustrated review archive supplements the original mechanical archive. Publishing authorised by the user; no printer or hardware operation requested.


## 2026-09-12 - Mechanical R7 and illustrated guide R7-A1

User supplied SunFounder documentation and LCD dimension image; source review on 11 September supersedes prior measured mounting values for this revision. Carrier centres change from 60 × 55 to 60 × 57 mm (67 × 64 mm outline). LCD centres change from 73 × 30 to 75 × 31 mm; 3 mm holes; bezel 71 × 24.2 mm receives a 71.4 × 24.6 mm aperture. Actual unit match remains unverified. Carrier is rotated in its plane so both USB ports face upwards; old rear access removed and shared 72 × 46 mm top service opening added. Port offsets and cable sizes are not dimensioned by the source: access remains deliberately broad, unsealed and subject to physical cable fit and strain relief.

Tower, fascia and top cover replaced; R6 sump, planter, battery tray and hose clip retained. Ten STL/STEP exports include separate button, LCD and carrier coupons. All 21 CAD assembly intersections pass; independent ten-mesh validation and dimensional sections exit 0. CAD generator reports PASS then exits 1 during shutdown without traceback; no clean CAD process exit is claimed. Seven-page illustrated PDF and Markdown guide include source drawing, actual CAD views, assembly instructions and acceptance worksheet. PDF rendered and visually reviewed. No firmware change, hardware fit test, electrical operation or printer run. User authorised GitHub publication and requested future updates also be pushed.


## 2026-09-13 - R9 annotated tower correction

Browser annotations requested closure above the upper fascia support and softened sharp/internal corners. R9 extends both webs to the 158 mm rim, adds cavity/support/root fillets and rim/front/USB/shelf edge treatment. Functional interfaces retained; scope is the annotated tower. Tower and upper-boss coupon changed, other 20 STL files match R8. Independent mesh/dimensional checks pass (exit 0); all 21 solid pairs clear; reopened STEP assertions pass with known runtime shutdown exit 1. See mechanical/concept_rev9/REVISION_CHECKS.md. Updated interactive viewer and mechanical review archive. No firmware or physical test changes.


## 2026-09-13 - R10 integrated tower/sump and internal cable route

User requested one printable body and internal cable routing rising above water-containing walls before entering electronics. Baseline R9 retained. Fused tower/sump with continuous web; elevated open cable trough floor z77 above sump rim z60. 8 mm entry/crossover bores, provisional 4 mm cable. No below-rim opening through the wet/dry wall. Revised planter service slot, upper retaining ribs and shelf clearance allow removal; 61 lift positions clear. Six main parts/21 exports. Mesh checks, 15 CAD pair checks, wall/continuity/route probes and STEP solid checks pass with documented CadQuery shutdown anomaly. Added actual-STL cable section and revised assembly guidance. Cable dimensions, bend radius, connector, strain relief and maximum water level remain unverified. No physical printing or electrical changes.


## 2026-09-13 - R11 supported riser and integrated battery saddle

R10 cantilevered route rejected in browser annotation. Replaced by compact floor/wall-integrated riser at the sump/tower junction with 8 mm vertical and crossover passages; crossover bottom z77, rim z60. No below-rim opening through wet/dry divider. Wet-side riser inlet z24 may admit sump water into riser below water level; not a sealed conduit. Local planter relief replaces long slot; 61 lift positions clear. Battery saddle fused into body; 6 x 2.5 mm transverse tie slot added; original holder clearance retained. Enclosed residual floor pilot voids filled. Five main parts, 20 exports; independent mesh and section checks pass, ten CAD pair checks clear and STEP assertions pass with known shutdown anomaly. Guide and section views updated; actual fit, tie/cable bending, fill level, slicing and leaks unverified.


## 2026-09-14 - R12 tube, pump-wire and sensor access

User noted R11 cable bore cannot carry the water tube and two pump wires; requested an above-planter sensor entry. Enlarged supported common intake to 23.5 x 34 mm, with separate 10 mm tube / 8 mm wire passages. Tube exits z128 outside electronics; wire crossover lower edge z77 remains above sump rim z60. Added independent 8 mm sensor entry, centre y65/z128, lower edge 8 mm above planter top. Local planter relief enlarged; original soil cavity, drains, integrated battery saddle and tie slot retained. Five main parts/20 exports; ten pair checks and 61 lift positions clear, independent mesh/section checks and STEP assertions pass with known CAD shutdown anomaly. Actual 8 mm tube OD, two 2.5 mm wire ODs and 4 mm sensor lead remain provisional pending measurements. No physical fit or wet-operation approval.
