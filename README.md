# ESP32 Plant Station

A compact, manual-dose ESP32 plant-watering prototype with a printable enclosure, removable planting compartment and lower pump sump.

**Current mechanical revision: R8, 12 September 2026. Left-side USB access, closed roof, reinforced fascia bosses, glued piezo/LED mounts and eight knob options. Manufacturing preparation: actual hardware fit remains unverified.**

![R8 CAD assembly](mechanical/concept_rev8/assembly.png)

## Interactive STL explorer

[Launch instructions and controls](mechanical/concept_rev8/viewer/README.md) for the R8 rotatable, zoomable exploded viewer, with part isolation and visibility controls. Uses the original seven enclosure STLs.

## Downloads

- [R8 illustrated assembly guide (PDF)](output/pdf/Plant_Station_R8_Illustrated_Assembly_Guide.pdf) and [online guide](docs/ASSEMBLY_GUIDE_R8.md).
- [Complete R8 illustrated review pack (ZIP)](ESP32_Plant_R8_Illustrated_Review.zip), including [BOM and fastener schedule](docs/BOM_R8.md).
- [22 STLs: seven enclosure parts, eight knob alternatives, six coupons and a marking blank](mechanical/concept_rev8/stl/), [STEP solids](mechanical/concept_rev8/step/), [assembly STEP](mechanical/concept_rev8/assembly.step) and [editable CAD source](mechanical/concept_rev8/build.py).
- [Dimensions, assumptions and print guidance](mechanical/concept_rev8/README.md), [dimensional sources](mechanical/concept_rev8/references/SOURCES.md).
- Historical packages: [R7](ESP32_Plant_R7_Illustrated_Review.zip), [R6](ESP32_Plant_R6_Illustrated_Review.zip), [R5](ESP32_Plant_R5_Review.zip). Use the R8 tower, fascia and roof together.

## Design

- Left-hand dry electronics tower; overall assembly 207 × 100 × 161 mm.
- SunFounder reference board 67 × 64 mm, rotated 90 degrees anticlockwise from R7 viewed from the fascia: installed 64 × 67 mm with **57 horizontal × 60 vertical** mounting centres. Both USB ports face left towards a provisional **28 × 20 mm** window. The roof is closed.
- Supplied LCD reference: PCB 80 × 36 mm, mounting centres **75 × 31 mm**, 3 mm holes. Fascia aperture **71.4 × 24.6 mm** clears the 71 × 24.2 mm bezel with a nominal 0.2 mm per side.
- Three nominal **12 mm** button holes retained under the current project control update. Piezo glue seat **10.4 mm ID** for the user-specified **10 mm** buzzer; three LED glue collars behind nominal 5 mm holes.
- Eight **20 mm OD × 14 mm** knob options: round 5.0/5.2/6.0/6.2/6.35/6.55 mm and D 6.0/6.2 mm. Fit coupon supplied; actual shaft dimensions unknown.
- Upper fascia screw bosses now have solid side-wall webs and sloped undersides; a real-geometry boss coupon is included.
- R6 sump retained: 60 mm external height / 56 mm internal depth; provisional pump envelope 38.5 × 25.5 × 43 mm. Planting cavity 90 × 60 × 50 mm with two 6 mm drains.

Print the fit coupons first. Port offsets, plug dimensions, shaft/bushing geometry, buzzer height, carrier stack and LCD depth need measurement. The small USB window is provisional, unsealed and may require relocation or enlargement. The included marking blank permits a measured trim aperture; it is not a snap-fit seal.

Enclosure STLs use millimetres and common assembly coordinates; accessory knobs/coupons use local coordinates. Orient and place each part on the bed before slicing. R8 replaces the tower, fascia and top cover; the sump, planter, battery tray and hose clip retain R7 geometry.

## Verification

All 22 exported meshes are closed, consistently wound, positive-volume single components, with two faces per edge and no degenerate faces. All 21 assembled enclosure part-pair intersections are zero within the recorded threshold. Reopened STEP files contain 22 valid single solids and a seven-solid assembly, with STL dimensions/volumes cross-checked. See [CAD verification](mechanical/concept_rev8/verification.json), [independent mesh checks](mechanical/concept_rev8/independent_mesh_check.json), [STEP checks](mechanical/concept_rev8/step_check.json) and [documentation QA](docs/R8_DOCUMENTATION_QA.md).

The local CadQuery runtime prints PASS then exits 1 during shutdown; a bare CadQuery import reproduces this, while VTK import and independent mesh checking exit 0. The STEP checker also reports successful assertions before the same CadQuery shutdown issue. Actual component fit, slicing, strength, watertightness and electrical operation remain unverified.

## Firmware

[Source and build instructions](firmware/README.md) implement one bounded manual timed dose per WATER press. Proposed STOP and LAMP TEST cancel the dose. Moisture is advisory; no automatic watering is implemented.

The pump output is disabled by default. The firmware uses an explicitly selected classic ESP32 compile-review profile, not an approved pin map for the actual SunFounder camera carrier. LCD text output is not implemented, and the probe path still needs I2C initialisation. Camera functionality, battery charging and wet operation are not validated.

Review compilation against ESP32 Arduino core 2.0.17 used 272,957 bytes flash and 21,944 bytes global RAM. No hardware upload was performed for R5.

## Rebuilding the artefacts

The CAD source uses Python, CadQuery 2.8, trimesh, NumPy and VTK. The PDF source uses ReportLab. Install dependencies in an isolated environment; local bundled runtimes are not included in this repository.

```powershell
python mechanical/concept_rev8/build.py
python mechanical/concept_rev8/check_exports.py
python mechanical/concept_rev8/check_step.py
python scripts/build_guide_r8.py
python scripts/package_r8_illustrated.py
```

Read the firmware README and PDF before compiling or attempting an upload. Confirm the exact board revision and GPIO reservations first; even a pump-disabled build configures other pins as outputs.

## Project records

[Requirements and unknowns](docs/PROJECT_CONTROL.md) and [electronics notes](docs/ELECTRONICS.md) retain the engineering context. [Current R8 BOM](docs/BOM_R8.md), mechanical notes and guide supersede older mechanical dimensions and fitting placeholders. Dimensional reference images are included with attribution; local build tools are excluded.

Next steps: measure the actual components, validate the carrier-specific pin map, print fit trials, review slicing, and complete dry electrical and controlled leak/flow tests.
