# ESP32 Plant Station

A compact, manual-dose ESP32 plant-watering prototype with a printable enclosure, removable planting compartment and lower pump sump.

**Current mechanical revision: R14 Uno mounts, 15 September 2026.** R13 integrated tower/sump revised with four asymmetric Uno R3 standoffs. The remaining enclosure parts are R13. Physical board, fastener and USB cable fit remain open.

![R14 tower](mechanical/concept_rev14_uno/preview.png)

## Downloads and revision records

- [Complete R14 mechanical review package](Plant_Station_R14_Uno_Review.zip).
- [R14 configuration and source](mechanical/concept_rev14_uno/README.md).
- [Replacement tower STL](mechanical/concept_rev14_uno/stl/tower_sump_body_uno.stl), [STEP](mechanical/concept_rev14_uno/step/tower_sump_body_uno.step), [fit coupon](mechanical/concept_rev14_uno/stl/uno_mount_fit_coupon.stl).
- [Assembly supplement](mechanical/concept_rev14_uno/ASSEMBLY.md), [change and verification record](mechanical/concept_rev14_uno/REVISION_CHECKS.md), [acceptance actions](mechanical/concept_rev14_uno/ACCEPTANCE.md).
- [Retained R13 parts and assembly guidance](mechanical/concept_rev13/README.md). Its carrier mounting instructions are superseded by R14; its electronics guidance is historical for the Uno configuration.

Two new meshes and STEP exports checked. No changed volume outside the mount regions; nominal board envelope clear. Independent mesh checks exit 0. CAD build reports PASS then exits 1 during shutdown; cause unresolved. Print the coupon before the tower. Slicing, physical fit, USB access, strength, leaks and commissioning remain open.

## Firmware

[Source and build instructions](firmware/README.md) implement one bounded manual timed dose per WATER press. Proposed STOP and LAMP TEST cancel the dose. Moisture is advisory; no automatic watering is implemented.

The pump output is disabled by default. The firmware uses an explicitly selected classic ESP32 compile-review profile, not an approved pin map for the actual SunFounder camera carrier. LCD text output is not implemented, and the probe path still needs I2C initialisation. Camera functionality, battery charging and wet operation are not validated.

Review compilation against ESP32 Arduino core 2.0.17 used 272,957 bytes flash and 21,944 bytes global RAM. No hardware upload was performed for R5.

## Rebuilding the artefacts

The CAD source uses Python, CadQuery 2.8, trimesh, NumPy and VTK. The PDF source uses ReportLab. Install dependencies in an isolated environment; local bundled runtimes are not included in this repository.

```powershell
python mechanical/concept_rev14_uno/build.py
python mechanical/concept_rev14_uno/check_exports.py
python scripts/package_r14_uno.py
```

Read the firmware README and PDF before compiling or attempting an upload. Confirm the exact board revision and GPIO reservations first; even a pump-disabled build configures other pins as outputs.

## Project records

[Requirements and unknowns](docs/PROJECT_CONTROL.md) and [electronics notes](docs/ELECTRONICS.md) retain the engineering context. The R13 kit guide supersedes the old R8 mechanical part and fastener quantities; [R8 electronics BOM](docs/BOM_R8.md) remains provisional background. Dimensional reference images are included with attribution; local build tools are excluded.

Next steps: measure the actual components, validate the carrier-specific pin map, print fit trials, review slicing, and complete dry electrical and controlled leak/flow tests.
