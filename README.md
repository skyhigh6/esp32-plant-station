# ESP32 Plant Station

A compact, manual-dose ESP32 plant-watering prototype with a printable enclosure, removable planting compartment and lower pump sump.

**Current mechanical revision: R6, 11 September 2026. Deeper sump for the shortlisted pump, checked 12 mm button insert spaces and enlarged hose clip. Prototype only: actual hardware fit and the SunFounder carrier pinout remain unverified.**

![R6 concept appearance - component fit unverified](mechanical/concept_rev6/concept_art.png)

Concept appearance only: LCD text, illumination and tube routing are illustrative. Use the [R6 CAD assembly view](mechanical/concept_rev6/assembly.png) and dimensioned notes for geometry.

## Downloads

- [R6 illustrated assembly guide (PDF)](output/pdf/Plant_Station_R6_Illustrated_Assembly_Guide.pdf): updated concept art, exploded/section CAD views, 15 assembly steps and acceptance worksheet.
- [Read the R6 assembly guide online](docs/ASSEMBLY_GUIDE_R6.md).
- [Complete R6 illustrated review pack (ZIP)](ESP32_Plant_R6_Illustrated_Review.zip): CAD/STL files, concept art, guide and source documentation.
- [R6 STL/STEP review package (ZIP)](ESP32_Plant_R6_Mechanical_Review.zip).
- [R6 seven assembly STLs plus fit coupon](mechanical/concept_rev6/stl/), [STEP solids](mechanical/concept_rev6/step/) and [R6 dimensions, assumptions and print guidance](mechanical/concept_rev6/README.md).
- [R6 assembly STEP](mechanical/concept_rev6/assembly.step) and [editable CAD source](mechanical/concept_rev6/build.py).
- [Earlier R5 illustrated build guide (PDF)](output/pdf/Plant_Station_R5_Illustrated_Build_Guide.pdf): R6 mechanical notes supersede its sump, planter and hose-clip dimensions; electrical information remains provisional.
- [Complete R5 review package (ZIP)](ESP32_Plant_R5_Review.zip).
- [Seven STL parts](mechanical/concept_rev5/stl/) and [individual STEP solids](mechanical/concept_rev5/step/).
- [Assembly STEP](mechanical/concept_rev5/assembly.step), [CAD source](mechanical/concept_rev5/build.py) and [mechanical notes](mechanical/concept_rev5/README.md).

## Design

- Left-hand dry electronics tower, viewed from the LCD/control face.
- Sage/charcoal design based on the [concept art](mechanical/concept_rev5/concept_reference.png).
- Approximate planting cavity: 90 x 60 x 50 mm, with two 6 mm floor drains into the sump.
- User-measured PCB mounting centres: 60 x 55 mm.
- User-measured LCD mounting centres: 73 x 30 mm; aperture: 70 x 25 mm.
- Three buttons, three LEDs, dose potentiometer, battery-holder tray and external hose clip.

STLs use millimetres and retain common assembly coordinates. Load them together without auto-arranging to inspect assembly; orient and place each individual part on the bed before slicing.

## Verification

Eight closed, consistently wound, positive-volume single-component meshes were checked: seven assembly parts and a button-fit coupon. All 21 assembled CAD part-pair intersections were zero within the stated threshold. Pump, button, mount, aperture, drain and tool-access checks are recorded in [R6 verification.json](mechanical/concept_rev6/verification.json), with [independent exported-mesh checks](mechanical/concept_rev6/independent_mesh_check.json).

Actual component envelopes, fasteners, printer tolerances, structural strength and watertightness are not validated. The mechanical notes record the local CAD runtime shutdown anomaly separately from completed geometry assertions and export checks. The supplied carrier's physical header pinout remains unknown; the illustrated pinout is a logical compile-review map only.

## Firmware

[Source and build instructions](firmware/README.md) implement one bounded manual timed dose per WATER press. Proposed STOP and LAMP TEST cancel the dose. Moisture is advisory; no automatic watering is implemented.

The pump output is disabled by default. The firmware uses an explicitly selected classic ESP32 compile-review profile, not an approved pin map for the actual SunFounder camera carrier. LCD text output is not implemented, and the probe path still needs I2C initialisation. Camera functionality, battery charging and wet operation are not validated.

Review compilation against ESP32 Arduino core 2.0.17 used 272,957 bytes flash and 21,944 bytes global RAM. No hardware upload was performed for R5.

## Rebuilding the artefacts

The CAD source uses Python, CadQuery 2.8, trimesh, NumPy and VTK. The PDF source uses ReportLab. Install dependencies in an isolated environment; local bundled runtimes are not included in this repository.

```powershell
python mechanical/concept_rev5/build.py
python scripts/build_guide_r5.py
```

Read the firmware README and PDF before compiling or attempting an upload. Confirm the exact board revision and GPIO reservations first; even a pump-disabled build configures other pins as outputs.

## Project records

[Requirements and unknowns](docs/PROJECT_CONTROL.md), [electronics notes](docs/ELECTRONICS.md), and [provisional BOM](docs/BOM.md) retain the original engineering context. R5 mechanical notes and the PDF supersede older mechanical dimensions and fitting placeholders in those records. Personal reference photos, superseded CAD revisions and local build tools are not included.

Next steps: measure the actual components, validate the carrier-specific pin map, print fit trials, review slicing, and complete dry electrical and controlled leak/flow tests.
