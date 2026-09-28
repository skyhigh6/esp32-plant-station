# R17 revision change matrix

The prior D01 matrix is preserved in verification/source_basis/previous_control. This matrix selects surviving historical changes and adds the new R15-R17 changes. Source comparison is not physical acceptance.

| ID | Label | Change | Frozen source basis |
|---|---|---|---|
| T06-1 | R6 | 60 mm sump and provisional pump envelope | mechanical/concept_rev6/README.md |
| T07-2 | R7 | 75 x 31 LCD centres and 71.4 x 24.6 aperture | mechanical/concept_rev7/README.md |
| T08-3 | R8 | Piezo/LED seats and adhesive precautions | mechanical/concept_rev8/README.md |
| T08-4 | R8 | Knob variants and axial clearance | mechanical/concept_rev8/README.md |
| T10-1 | R10 | Integrated tower/sump body | mechanical/concept_rev10/README.md |
| T11-1 | R11 | Integrated holder saddle and tie slot | mechanical/concept_rev11/README.md |
| T12-1 | R12 | Separate tube/wire routes | mechanical/concept_rev12/README.md |
| T13-1 | R13 | No separate hose clip or tray | mechanical/concept_rev13/README.md |
| T13-4 | R13 | Sensor entry z64 and lower edge z60 | mechanical/concept_rev13/README.md |
| T14-1 | R14 | Asymmetric Uno board mounting centres | mechanical/concept_rev14_uno/README.md |
| T15-1 | R15 | Reinforced Uno bosses after reported splitting | mechanical/concept_rev15_uno/DESIGN_REVIEW.md |
| T15-2 | R15 | 5.5 mm lid with flush-head pockets | mechanical/concept_rev15_uno/DESIGN_REVIEW.md |
| T15-3 | R15 | Pump relief lowered to z4 and extended to x132 | mechanical/concept_rev15_uno/DESIGN_REVIEW.md |
| T16-1 | R16 | Four relay mounts below Uno | mechanical/concept_rev16_uno_relay/REVIEW.md |
| T17-1 | R17 | Mounted USB-C cut replaces old pass-through; DC diameter 10 | mechanical/concept_rev17_uno_ports/README.md |
| T17-2 | R17 | Current UI v6 three-button and lamp/relay interface incorporated into manual | docs/UNO_BUTTON_RELAY_REVISION_2026-09-27.md |
| T17-3 | R17 | Current dose, soil status, display return and backlight behaviour incorporated | firmware/arduino/PlantUno/PlantUno.ino |
| T17-4 | R17 | Current digital evidence and cumulative physical acceptance plan | mechanical/concept_rev17_uno_ports/verification.json |
| T17-5 | R17 | USB/barrel extensions remain an electrical interface hold | mechanical/concept_rev17_uno_ports/README.md |

## Supersession and gaps

R14 diameter-6 Uno supports, 3 mm unrecessed roof, broad USB cable opening and motor-disabled/spare-button instructions are superseded for the current build. R15/R16 manual PDFs are deliberately not created. R1-R4 and prior unlocated PDFs remain unknown, as documented in the previous inventory. R17 figure captions identify retained R13/R16 source views; no changed detail is falsely claimed as a measured fit.
