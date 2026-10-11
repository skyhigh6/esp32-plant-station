# Plant Station — current project control

**Baseline:** R18 prototype / document issue D03 / Uno UI v6. **Date:** 11 October 2026. **Status:** issued for prototype review; print/dry-fit, electrical and wet acceptance open. **Previous issued baseline:** R17 / D02, preserved.

## Configuration authority

| Item | Current authority |
|---|---|
| Assembly, wiring, holds | [PLANT-AM-001 R18 D03](docs/documents/AM_R18/PLANT-AM-001_R18_D03.pdf) |
| Change justification and unknowns | [PLANT-TR-001 R18 D03](docs/documents/TR_R18/PLANT-TR-001_R18_D03.pdf) |
| Acceptance records | [PLANT-TS-001 R18 D03](docs/documents/TS_R18/PLANT-TS-001_R18_D03.pdf); A17-01–A17-13 and A18-01–A18-04 open |
| Firmware | `firmware/arduino/PlantUno/`; UI v6 unchanged |
| Combined CAD entry | `technical/cad/build_r18.py`; C01/C02 records preserved under `technical/cad/candidates/` |
| R18 geometry authority and datum | `technical/cad/R18_CONFIGURATION.md` describes actual R18 cuts; `technical/cad/parameters.json` retains inherited R17 port parameters; mm; x right, y rear, z up |
| Manufacture exports | `technical/print/manifest.json`; R18 tower/fascia, retained R16 lid/R13 planter and one chosen knob |
| R17 plate and printer files | `technical/print/plate_layout/r17_plate_layout.3mf` and `technical/print/slicer_exports/`; historical R17 evidence only; prepare new R18 slicing |
| Documentary lineage | `docs/control/`; preserved R17 set and selected source basis under `verification/source_basis/` |
| Release integrity | `releases/R18/manifest.json` and `SHA256SUMS.txt` |

## Incorporated changes

- **R15:** reinforced Uno bosses, 5.5 mm lid with recessed heads, pump-route relief.
- **R16:** four relay PCB mounting bosses below the Uno.
- **R17:** mounted USB-C aperture/pilots and adjacent Ø10 mm barrel-input extension hole. Unmeasured USB dimensions remain authorised estimates.
- **R18:** C01 opens the pump-wire riser and upward crossing for lay-in with terminated leads. C02 fills three standalone LED apertures and the dedicated speaker aperture, retaining button LEDs and all fit-defining fascia features.
- **UI v6:** three illuminated-button interface; D9 active-HIGH relay; A1 samples a 1,000–4,000 ms dose; post-dose soil display; 60 s LCD backlight timeout. Firmware unchanged.
- **D03:** full current R18 manual, review and acceptance set with editable sources, refreshed illustrations, history/effective-page lists and source-backed bars. R17/D02 remains the previous issued set.

## Evidence and limitations

**Reported:** Kevin says the latest printed R17 tower fits the Arduino and relay perfectly. R18 source checks retain their nominal pilots, mounting regions and interfaces. This first-article report is not measured hardware or operational acceptance.

**Confirmed digital scope:** C01/C02 records show valid STEP solids, closed/wound positive-volume meshes, retained interface sections, clear route probes and fascia additions confined to four obsolete openings. Source candidate builders printed PASS then returned exit 1. Current R18 scratch regeneration printed PASS and reproduced all three STL hashes; both child processes ended with Windows status `0xC0000374` (3221226356), while the wrapper returned 1. The shutdown anomaly remains open; no clean CAD process success is asserted. Separate independent checks return 0. See `verification/cad/r18_regeneration_process.json` and `r18_combined_checks.json`. Digital compatibility does not establish printed strength, leak resistance, bend radius or cable retention.

C01 slicing supports removal of selected route ceilings. Its warnings and anomalous timing metadata remain recorded; it is comparison evidence, not issued R18 toolpaths. Retained R17 plate and printer files represent predecessor geometry and must not be used as current R18 print instructions.

The 27 September UI v6 source records an upload and serial LCD status 0 with idle/activity backlight commands. Historical software evidence does not establish present LCD reliability, relay timing, delivered volume or lamp performance. This revision performs no upload or hardware operation.

## Open acceptance gates

| Actions | Required evidence |
|---|---|
| A17-01–A17-13 | All remain open: USB/DC fit and electrical interface, board/screw/lid/control trials, strength/leaks and electrical commissioning |
| A18-01 | Actual bundle lay-in without forcing or removing terminations; optional route trial checks local clearance only |
| A18-02 | Smooth bends, edge condition, slack, retention and service removal with retained parts installed |
| A18-03 | Printed fascia face continuity/flatness and dry fit of buttons, display, knob and fixings |
| A18-04 | Combined full dry assembly, clearances, new R18 slicer layers/supports and print inspection |

The reported Uno/relay fit closes no controlled action. USB/DC estimates require the retained port coupon and actual hardware. Verify USB-C wiring, voltage/current, barrel polarity and supply interaction before power; verify button leads/current limits, relay reset behaviour, pump ratings, LCD reliability, dose timing and delivered volume. STOP is software cancellation, not electrical isolation.

Detailed criteria and blank actual-result fields are in PLANT-TS-001. Owners: **Unassigned**. Target dates: **Not set**. No acceptance gate is closed by this issue.

## Recovery and change control

R17/D02 remains in `docs/documents/*_R17/` and `releases/R17/`. Original tower and fascia exports are frozen predecessor inputs, not current print choices. C01/C02 candidate records remain unchanged as issue-time evidence; their former “R17 remains issued” statements describe the review stage now incorporated into R18.

Preserve originals and user-edited geometry. Revise measured dimensions in editable sources, rebuild to a review area, rerun independent checks and inspect affected document pages before promoting outputs. Update manifests and issue records. Physical results require actual observations against this configuration; no force push or history rewrite is part of this revision.
