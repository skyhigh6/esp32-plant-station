# ESP32 Plant Station

A compact, manual-dose ESP32 plant-watering prototype with a printable enclosure, removable planting compartment and lower pump sump.

**Current mechanical revision: R13, 14 September 2026.** Four main enclosure parts. Removed clip/shelf and old battery bores; rounded hose riser; corrected lower support roots; sensor lead entry lowered to the sump rim with local planter clearance.

![R13 assembly](mechanical/concept_rev13/assembly.png)

## Downloads and interactive explorer

- [Complete R13 review package](ESP32_Plant_R13_Illustrated_Review.zip).
- [Kit assembly instructions - customer-format prototype edition](output/pdf/Plant_Station_R13_Kit_Assembly_Instructions.pdf).
- [Design review and annotation disposition](output/pdf/Plant_Station_R13_Design_Review.pdf).
- [R13 geometry, assembly and verification](mechanical/concept_rev13/README.md).
- [STLs](mechanical/concept_rev13/stl/), [STEPs](mechanical/concept_rev13/step/), [assembly STEP](mechanical/concept_rev13/assembly.step).
- [Interactive explorer instructions](mechanical/concept_rev13/viewer/README.md).
- [AI product illustration and provenance](mechanical/concept_rev13/AI_IMAGE_PROVENANCE.md).

19 meshes and STEP parts checked; four-solid assembly, six zero-overlap pairs, 61 sampled planter lift positions clear. CAD/STEP assertions passed with the existing runtime shutdown exit 1; independent mesh and section tools exited 0. Physical fit, slicing, strength, leaks and electrical commissioning remain open. The low cable entry is not a sealed gland or an approved fill level. See the revision records for limits.

## Firmware

[Source and build instructions](firmware/README.md) implement one bounded manual timed dose per WATER press. Proposed STOP and LAMP TEST cancel the dose. Moisture is advisory; no automatic watering is implemented.

The pump output is disabled by default. The firmware uses an explicitly selected classic ESP32 compile-review profile, not an approved pin map for the actual SunFounder camera carrier. LCD text output is not implemented, and the probe path still needs I2C initialisation. Camera functionality, battery charging and wet operation are not validated.

Review compilation against ESP32 Arduino core 2.0.17 used 272,957 bytes flash and 21,944 bytes global RAM. No hardware upload was performed for R5.

## Rebuilding the artefacts

The CAD source uses Python, CadQuery 2.8, trimesh, NumPy and VTK. The PDF source uses ReportLab. Install dependencies in an isolated environment; local bundled runtimes are not included in this repository.

```powershell
python mechanical/concept_rev13/build.py
python mechanical/concept_rev13/check_exports.py
python mechanical/concept_rev13/check_step.py
python scripts/build_guide_r13.py
python scripts/package_r13_illustrated.py
```

Read the firmware README and PDF before compiling or attempting an upload. Confirm the exact board revision and GPIO reservations first; even a pump-disabled build configures other pins as outputs.

## Project records

[Requirements and unknowns](docs/PROJECT_CONTROL.md) and [electronics notes](docs/ELECTRONICS.md) retain the engineering context. The R13 kit guide supersedes the old R8 mechanical part and fastener quantities; [R8 electronics BOM](docs/BOM_R8.md) remains provisional background. Dimensional reference images are included with attribution; local build tools are excluded.

Next steps: measure the actual components, validate the carrier-specific pin map, print fit trials, review slicing, and complete dry electrical and controlled leak/flow tests.
