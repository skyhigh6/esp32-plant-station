# Plant Station — current project control

**Baseline:** R17 prototype / document issue D02 / Uno UI v6. **Date:** 28 September 2026. **Status:** issued for prototype review; physical and electrical acceptance open.

## Configuration authority

| Item | Current authority |
|---|---|
| Assembly, wiring, holds | [PLANT-AM-001 R17 D02](docs/documents/AM_R17/PLANT-AM-001_R17_D02.pdf) |
| Change justification and unknowns | [PLANT-TR-001 R17 D02](docs/documents/TR_R17/PLANT-TR-001_R17_D02.pdf) |
| Acceptance records | [PLANT-TS-001 R17 D02](docs/documents/TS_R17/PLANT-TS-001_R17_D02.pdf); A17-01–A17-13 open |
| Firmware | `firmware/arduino/PlantUno/`; UI v6 source preserved unchanged |
| Geometry parameters | `technical/cad/parameters.json`; mm; x right, y rear, z up |
| Manufacture exports | `technical/print/manifest.json`; four main parts plus one chosen knob |
| Documentary lineage | `docs/control/`; selected source basis under `verification/source_basis/` |
| Release integrity | `releases/R17/manifest.json` and `SHA256SUMS.txt` |

## Incorporated changes

- **R15:** reinforced Uno bosses, 5.5 mm lid with recessed heads, pump-route relief.
- **R16:** four relay PCB mounting bosses below the Uno.
- **R17:** left mounted USB-C aperture/pilots and adjacent Ø10 mm barrel-input extension hole. Unmeasured USB details use estimates explicitly authorised by the user.
- **UI v6:** three button/lamp interface; D9 active-HIGH relay; A1 samples a 1,000–4,000 ms dose; post-dose soil display; 60 s LCD backlight timeout.
- **D02:** current assembly manual, design review and test sheets issued directly at R17. No intermediate R15/R16 manuals are asserted. AM predecessor R14 D01; TR predecessor R13 D01; TS newly assigned.

Repository reorganisation changes file locations and publication tooling. It does not change current firmware, R17 geometry or issued PDF content. Selected inherited STL/STEP files retain their originating revision suffixes and hashes.

## Evidence and limitations

Digital evidence records valid STEP solids, closed/wound STL meshes and named port sections. The original CAD builder printed PASS and exited 1 during a runtime shutdown anomaly; this is not a clean build. The independent exported-mesh checker exited 0. PDF layout, controls and clean rendered-page rebuilds are recorded separately.

Regeneration at the new paths reproduced both released R17 STL hashes and passed the independent section checker (exit 0). The CAD process again terminated abnormally after export, this time with Windows status `0xC0000005` / exit `-1073741819`. This remains an open runtime anomaly; regeneration is not recorded as a clean process success. Canonical released exports remain unchanged.

The 27 September interface source records an uploaded UI v6 and serial LCD status 0 with idle/activity backlight response. That historical serial/software evidence does not establish physical display reliability, relay timing, delivered volume or lamp performance. The user's report of operation remains reported evidence. This publication performs no upload or hardware operation.

## Open acceptance gates

1. Fit actual USB module, screws and mating plug to the port coupon; verify estimated pitch and aperture, flange seating, local wall strength and solder access.
2. Fit the actual DC extension, nut and plug; verify Ø10 bore, 6 mm panel grip, cable depth and connector clearance.
3. Complete Uno/relay screw and underside-clearance trials, recessed lid trial and pump-route trial; select the physical knob fit.
4. Inspect slicer layers, printing orientation, dry assembly, strength and leakage.
5. Identify USB-C power/data/CC wiring, source voltage/current, barrel polarity and supply interaction before connecting power. Supplier “6 pin / 5 A” image text is not a verified rating.
6. Verify button leads/current limits, relay reset behaviour, pump ratings, LCD reliability, dose timing and delivered volume. STOP is software cancellation, not electrical isolation.

Detailed test criteria and blank actual-result fields are in PLANT-TS-001. Owners: **Unassigned**. Target dates: **Not set**. No acceptance gate is closed by this release.

## Recovery and change control

Pre-cleanup published baseline: `18ab0d889db349c712b43624d315e4f15ed3ebe2`. Earlier published work remains in Git history; unpublished files and a verified Git bundle are retained in an external local backup. The current tree contains only the R17 deliverables and required lineage records. No force push or history rewrite is part of this change.

Revise measured dimensions in the editable source, generate trial outputs to `.build/`, rerun independent checks, review affected document pages and deliberately promote accepted digital outputs. Update the controlled manifests and issue records before making another release. Physical results require actual observations recorded against this configuration.
