# Plant Station R18 — combined change record

Document basis: AM/TR/TS R18 D03, 11 Oct 2026. Preceding issue: R17 D02, 28 Sep 2026. Status: issued for combined prototype review; physical and electrical acceptance open. Units: mm.

## Authorised configuration

Kevin authorised combining the new fascia and open pump-wire route in R18 and completing the revision documents. The selected changes are replacement geometry, not additional assembly parts. Preserve R17 originals and user print projects. Uno UI v6 remains unchanged.

| Change ID | Previous configuration | R18 configuration | Evidence / limit |
|---|---|---|---|
| T18-1 | Enclosed pump-wire bore and crossover; fitted terminations reportedly cannot pass | Front opening x106.5–114, y82–96, z52–129; upward-open crossover x89–114, y88–96, z77–159 | C01 CAD and independent mesh/section checks; actual cable fit, bend and retention remain open |
| T18-2 | Three standalone 5 mm LED holes and one circular 4 mm speaker hole in retained fascia | Four holes closed flush through the 3 mm face plate; rear LED collars and piezo ring remain blind pockets | C02 CAD/mesh/section checks; new printed fascia fit and face inspection open |
| T18-3 | R17 D02 document configuration and older physical evidence | Combined R18 D03 documents; partial reported board-fit evidence; A17 actions carried forward plus A18 checks | Documentary incorporation does not establish a new physical pass |

The route floor remains z77, 17 mm above the z60 sump rim. The protected wet/dry partition, water bore, sump floor, board mounts and rear-right lid fixing are retained. Local wet-side riser removal between z52 and z60 is outside the protected divider; it does not define an accepted fill level. Actual wire/termination dimensions, minimum bend radius and positive restraint remain Unknown.

The fascia retains the three illuminated-button openings, 71.4 × 24.6 mm LCD aperture, 7 mm knob opening, 3.4 mm fixing holes and display bosses. It adds 214.414 mm³ in the four original aperture regions, with zero removed volume and zero added volume outside those regions. Integrated button lamps retain their existing D5/D6/D7 circuitry; D10 remains unused. No standalone LED or speaker is introduced or newly wired.

## Selected files and preserved history

Current main geometry: `tower_open_pump_route_r18.{stl,step}`, `fascia_no_aux_apertures_r18.{stl,step}`, retained `top_cover_flush_r16` and `planter_sage`. `route_trial_r18` is an optional 29 × 20 × 60 mm local test artefact; it cannot establish complete wire retention, strength or assembly acceptance. The R17 power-port coupon remains applicable to its unchanged interface.

R17 plate projects, slicer outputs and superseded geometry remain historical evidence. They are not accepted R18 printer files. No accepted combined R18 slicing, new physical print or hardware test is recorded.

## Evidence and limitations

**Reported:** Kevin says the newest printed tower accepts the Arduino and relay perfectly. The exact printed file, material, measured clearances, screw retention and underside inspection are not independently established. Preserve this as partial registration evidence against A17-02/A17-05; both complete actions remain open.

**Confirmed digital evidence:** C01/C02 STEP readback, protected-region comparisons and independent exported-mesh/section checks support the scoped geometry changes. Combined STEP checks record zero intersection for all six main-part pairings and retain all eight Uno/relay pilot sections. This demonstrates nominal compatibility and preservation, not fitted-hardware acceptance.

Candidate route comparison in Bambu Studio 2.5.0.66 estimated support deposition at 24.215 g for the baseline and 23.699 g for C01 under copied versions of one upright user profile, approximately 2.13% less. The route tunnel ceilings were removed; the full tower is not established support-free. Values are estimated commanded extrusion, not measured consumption. Missing-preset, ZFiller and bed-temperature/filament warnings, plus implausible timing metadata, make this comparison evidence only. It does not accept a printer job or establish the actual printed material.

Original candidate CAD runs printed geometry PASS then exited 1 during shutdown; separate mesh checkers exited 0. The R18 scratch regeneration produced byte-identical STL geometry for tower, fascia and route trial and completed geometry checks, but both CAD child processes returned 3221226356 (`0xC0000374`) after PASS; wrapper exit was 1. Combined STEP checks also completed and saved PASS evidence before process exit 1. The mesh-only checker exited 0. No clean CAD process success or full mesh self-intersection test is asserted. A17-13 remains open.

## Actions and disposition

All A17-01 through A17-13 actions remain open. Owners: Unassigned. Target dates: Not set. New action IDs are common to AM/TR/TS:

| ID | Action | Closure evidence |
|---|---|---|
| A18-01 | Measure and lay in the actual terminated pump lead without forcing or terminal removal | Actual cable dimensions, article hash and dry-fit photographs/observations |
| A18-02 | Check printed edges, bends, protection, restraint and lid/planter service removal | Identified cable bend/retention basis, no insulation damage, repeated fitted/removal observations |
| A18-03 | Inspect the four closed fascia positions and dry-fit retained controls and fixings | Continuous flat plate, no cracks/gaps/delamination, fitted component and removal evidence |
| A18-04 | Review the actual R18 print job and complete combined dry assembly | Accepted layer/material/orientation record, printed-part hashes, clear water tube/boards/terminals/services and untrapped removal |

No action is pre-closed. Electrical/default-OFF, LCD, leak/fill and measured dose acceptance must be recorded separately before accepted supervised wet use. Current disposition remains prototype review.

## Source map

- `technical/cad/candidates/R18_open_pump_route/CHANGE_RECORD.md`, `reported_first_article.json`, geometry/independent checks and source-assurance slice comparison.
- `technical/cad/candidates/R18_fascia_no_aux_apertures/CHANGE_RECORD.md`, geometry/independent checks and source-assurance STEP/mesh/section evidence.
- `verification/cad/r18_regeneration_process.json` and `verification/cad/r18_combined_checks.json`.
- Preserved R17 D02 AM/TR/TS sources and cumulative `change_matrix.json`.
- Frozen Uno UI v6 source and 27 Sep 2026 interface/upload record.
