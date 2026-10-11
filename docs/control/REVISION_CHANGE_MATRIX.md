# R18 revision change matrix

The cumulative JSON matrix is `change_matrix.json`. Prior D01 control records remain under `verification/source_basis/previous_control`; R17/D02 documents and their release are preserved. Source comparison is not physical acceptance. Historical changes are included only where they survive in the current design/instructions.

| ID | Label | Change | Frozen source basis |
|---|---|---|---|
| T06-1 | R6 | 60 mm sump and provisional pump envelope | mechanical/concept_rev6/README.md |
| T07-2 | R7 | 75 × 31 LCD centres and 71.4 × 24.6 aperture | mechanical/concept_rev7/README.md |
| T08-3 | R8 | Historical piezo/LED seats and adhesive precautions; front apertures superseded by T18-2 | mechanical/concept_rev8/README.md |
| T08-4 | R8 | Knob variants and axial clearance | mechanical/concept_rev8/README.md |
| T10-1 | R10 | Integrated tower/sump body | mechanical/concept_rev10/README.md |
| T11-1 | R11 | Integrated holder saddle and tie slot | mechanical/concept_rev11/README.md |
| T12-1 | R12 | Separate tube/wire routes; wire enclosure superseded by T18-1 | mechanical/concept_rev12/README.md |
| T13-1 | R13 | No separate hose clip or tray | mechanical/concept_rev13/README.md |
| T13-4 | R13 | Sensor entry z64 and lower edge z60 | mechanical/concept_rev13/README.md |
| T14-1 | R14 | Asymmetric Uno board mounting centres | mechanical/concept_rev14_uno/README.md |
| T15-1 | R15 | Reinforced Uno bosses after reported splitting | mechanical/concept_rev15_uno/DESIGN_REVIEW.md |
| T15-2 | R15 | 5.5 mm lid with flush-head pockets | mechanical/concept_rev15_uno/DESIGN_REVIEW.md |
| T15-3 | R15 | Pump relief lowered to z4 and extended to x132 | mechanical/concept_rev15_uno/DESIGN_REVIEW.md |
| T16-1 | R16 | Four relay mounts below Uno | mechanical/concept_rev16_uno_relay/REVIEW.md |
| T17-1 | R17 | Mounted USB-C cut replaces broad pass-through; DC diameter 10 | mechanical/concept_rev17_uno_ports/README.md |
| T17-2 | R17 | UI v6 three-button and lamp/relay interface incorporated into manual | docs/UNO_BUTTON_RELAY_REVISION_2026-09-27.md |
| T17-3 | R17 | Dose, soil status, display return and backlight behaviour incorporated | firmware/arduino/PlantUno/PlantUno.ino |
| T17-4 | R17 | Digital evidence and cumulative physical acceptance plan | mechanical/concept_rev17_uno_ports/verification.json |
| T17-5 | R17 | USB/barrel extensions remain an electrical interface hold | mechanical/concept_rev17_uno_ports/README.md |
| T18-1 | R18 | Open front wire riser and upward crossing for terminated-lead lay-in; optional route trial | technical/cad/candidates/R18_open_pump_route/CHANGE_RECORD.md |
| T18-2 | R18 | Fill three standalone LED apertures and one speaker aperture; retain illuminated-button openings and fit interfaces | technical/cad/candidates/R18_fascia_no_aux_apertures/CHANGE_RECORD.md |
| T18-3 | R18 | Reported board-fit evidence, combined R18/D03 configuration and unresolved manufacture/acceptance | technical/cad/candidates/R18_open_pump_route/reported_first_article.json; both candidate change records |

## Supersession and gaps

R14 diameter-6 Uno supports, 3 mm unrecessed roof, broad USB opening and motor-disabled/spare-button instructions were superseded before R18. R18 supersedes the enclosed pump-wire riser/crossing and four auxiliary fascia apertures. It does not remove integrated button LEDs, change firmware, delete retained rear LED/speaker seats or accept actual cable retention.

R17/D02 is now the previous issued instruction set. Its plate/slicer files are historical evidence, not current R18 toolpaths. Original R17 tower and R13-lineage fascia exports are frozen sources; select their R18 replacements for a current build. C01/C02 “R17 remains issued” wording is preserved as candidate issue-time history.

All A17 actions remain open; A18-01–A18-04 add route, retention, fascia and combined dry-fit/manufacturing checks. Reported Uno/relay fit is partial evidence only. R1–R4 and earlier unlocated PDFs remain Unknown as recorded in the historical inventory; no missing manual issues or test closures are invented.
