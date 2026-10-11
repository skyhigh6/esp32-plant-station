# Plant Station R18 - Test and Acceptance Sheets
PLANT-TS-001 / R18 / D03 / 11 October 2026
Issued for combined prototype review; physical acceptance open

Current mechanical configuration: R18 open-route tower and R18 fascia with auxiliary holes closed; retained R16 lid (R15 geometry) and R13 planter. Electrical reference remains frozen Uno UI v6 and the 27 September interface record. Arduino/relay registration is Reported; physical retention, wiring, wet and operational acceptance remain open.

## Test article, prerequisites and recording rules

Test article: combined R18 tower_open_pump_route_r18 and fascia_no_aux_apertures_r18, retained R16 lid/R13 planter, and unchanged Uno UI v6. Kevin reports newest-tower Arduino/relay fit; this is partial evidence only. No R18 physical pass is pre-populated. Link every action to actual build/part hashes, component identities, operator/date and retained evidence.

| Record field | Actual value |
| --- | --- |
| Build ID / serial / operator / date | ________________ |
| Printed-part hashes / document issue | ________________ |
| Printer / material / slicer / orientation | ________________ |
| Component models/revisions and photographs | ________________ |
| Screw measurements / engagement | ________________ |
| Supply identifiers / ratings / protections | ________________ |
| Instruments and calibration/check status | ________________ |
| Test method / environmental conditions | ________________ |
| Deviation IDs / defect report / evidence location | ________________ |

Before electrical work disconnect every supply. Before powered logic/upload checks confirm the separate pump supply is OFF. No upload, printer operation or powered test is executed by this document.

Use Pass / Fail / Not tested / Deferred with evidence. A blank actual result remains Not tested. Acceptance tolerances not supplied must be agreed and recorded before assessing that test; do not invent acceptable duration, volume, torque or leak rates.

## Mechanical coupons and dry assembly

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-01 | USB/DC fit coupon | USB shell and screw pattern fit; plug engages; DC thread/nut span 6 mm; no cracks | Not tested |
| A17-02 | Uno screws and board | 2.8 pilot trial takes actual screws; all four centres register without PCB bowing | Open; board fit Reported, screws/underside unaccepted |
| A17-03 | Flush lid | Heads sit flush/below surface; pockets intact; lid seats; engagement verified | Not tested |
| A17-04 | Pump route | Actual pump/tube clear relief; no kink; dry partition preserved | Not tested |
| A17-05 | Relay fit | Four-hole registration; solder, screws, terminals and service removal clear | Open; board fit Reported, underside/wires unaccepted |
| A17-06 | Fascia and full dry build | LCD/buttons/pot fit; wiring untrapped; planter lifts clear; all fasteners retain | Not tested |

A17-01: print the port coupon in the intended material; measure both mounting centres and each cut; trial connectors, fasteners, actual plugs, DC nut and solder/wire access together.

A17-02: trial actual screws in full-length 2.8 mm bosses; measure engagement and remaining pilot-depth margin. Inspect splitting/retention and all four Uno holes before approving a body change.

A17-03/04: trial actual lid heads and pump with attached tube against matching coupons, then check seat, clearances, removal and dry boundary in the body.

A17-05/06: retain the reported Arduino/relay fit as an attributed observation, not a complete pass. Measure relay pitch/underside, fit all screws and inspect actual wires/tool access. Dry-build R18 fascia, boards, wiring and planter; record full removal travel. New route/fascia results also require A18-01 to A18-04.

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-01 | ________________________ | Not tested / __________ |
| A17-02 | ________________________ | Not tested / __________ |
| A17-03 | ________________________ | Not tested / __________ |
| A17-04 | ________________________ | Not tested / __________ |
| A17-05 | ________________________ | Not tested / __________ |
| A17-06 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## Power interface and relay reset acceptance

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-07 | USB/barrel electrical interface | Exact USB pins/CC/power/data, DC polarity/voltage and source behaviour identified | Open design hold |
| A17-08 | Relay default OFF | Coil/input/contact ratings recorded; OFF through reset and both supply sequences | Not tested |

A17-07: identify USB-C part/pins and intended power/data adaptation; inspect configuration-channel provision. Measure actual DC extension polarity, mating dimensions and grip. Freeze the approved input diagram and source selection before energising it.

Record USB input, board rails and barrel input voltages/current under the agreed load. Record the intended supply arrangement and unwanted coupling tests appropriate to it. Define numerical pass limits from matching component specifications first.

A17-08: with pump disconnected, identify coil/input/contact ratings and measure contact state through board reset, open logic input and both source power-up orders. Expected contact state is OFF throughout inhibit conditions; stop on any transient closure.

Verify an accessible physical pump-power disconnect, selected fuse/wire/contact ratings and motor suppression. Do not substitute a software OFF message for measured contact state.

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-07 | ________________________ | Not tested / __________ |
| A17-08 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## LCD, controls and dose measurements

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-09 | LCD and controls | Display stable, buttons/lamps verified, dose return and full 60 s timeout observed | Partial serial record only |
| A17-10 | Dose and volume | Actual contact/pump durations and volume measured at selected endpoints | Not measured |

A17-09: with pump supply OFF, verify each switch and lamp; stable LCD status 0 and visible pages; STOP/release lockout; 1-4 s indicated endpoints; safe soil-index/fault test inputs; no automatic request from moisture.

Observe and record the actual LCD backlight after 60 s idle, button/knob wake and 60 s after completed/cancelled requests. Confirm immediate soil Status return at request end. Retain video/timed observation and serial as separate evidence.

A17-10: after power/reset protections pass, run a supervised measured pump trial using the approved supply and installed tube/lift. Measure contact ON duration and delivered volume at 1.0/4.0 s settings and intermediate points required by the intended use.

Timing and volume acceptance tolerances: Not yet defined. Record instrumentation resolution, repetitions, individual readings, mean/range and failures. Do not mark a test Pass without the pre-set numerical criteria.

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-09 | ________________________ | Not tested / __________ |
| A17-10 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## Leak/fill, print configuration and CAD exception

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-11 | Leak/fill and wet route | Leak, drain-back, tilt/splash evidence; fill limit below unsealed openings recorded | Not tested |
| A17-12 | Material/print configuration | Material, slicer layers, orientation, local fit/strength recorded | Unknown |
| A17-13 | CAD shutdown anomaly | Clean CAD process log or isolated dependency defect with retained evidence | Open; build exits 1 |

A17-11: define leak-test duration, fill candidate, containment and acceptance first. Record actual water level, drain-back headspace, soil/drain condition, planter movement, tilt/splash exposure and dry-tower inspection. Fill mark acceptance needs physical evidence.

A17-12: record actual material, printer, saved R18 job, part hashes, orientation/supports and measured holes; inspect complete layers and rear bosses. Prior R17 plate projects are historical. Candidate slice comparisons carry warnings and do not close this action or supply accepted R18 machine files.

A17-13: retain build outputs and exit statuses. Original candidate CAD runs report geometry PASS then exit 1. Scratch R18 regeneration reproduces all three STL hashes, but both child processes exit 3221226356 (0xC0000374) after PASS; wrapper exit 1. Combined STEP checking saves PASS then exits 1; mesh-only checks exit 0. Preserve the exception until a clean process or isolated dependency-defect evidence closes it; no physical fit follows.

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-11 | ________________________ | Not tested / __________ |
| A17-12 | ________________________ | Not tested / __________ |
| A17-13 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## R18 route, fascia and combined-build acceptance

| Action ID | Test / method | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A18-01 | Terminated pump-lead lay-in | Actual bundle dimensions recorded; lays into front/top channel with terminations retained and no forcing | Open / Not tested |
| A18-02 | Wire bends, edges and retention | Deburred edges; no insulation damage/kink; qualified bend/retention basis; wire stays seated through lid/planter service | Open / Not tested |
| A18-03 | Replacement fascia face and controls | 4 positions continuous/flat without cracks; buttons/LCD/knob/fixings seat and remove without force | Open / Not tested |
| A18-04 | Combined print and full dry build | Actual R18 job/layers/part hashes recorded; existing tube, boards, terminals, lid and planter clear; service removal untrapped | Open / Not tested |

A18-01: with every supply disconnected, measure the actual bundle and termination envelopes. Remove lid/planter and lay the intermediate wire into the open front channel x106.5-114/y82-96/z52-129 and upward-open crossover x89-114/y88-96/z77-159. Keep terminations fitted. Retain measurements and photographs; optional route_trial_r18 only checks local width/lay-in.

A18-02: inspect printed edges and document the actual cable bend/strain-relief basis before assessing retention. Fit the retained lid, planter and fascia, observe pinching/lifting and repeat removal/reinstallation without disturbing boards or removing terminals. Record any protection/retention correction explicitly; do not silently add a new printed part. Stop on insulation damage, sharp contact, forcing or unrestrained wire.

A18-03: inspect the three former 5 mm LED positions and one former 4 mm speaker position through the 3 mm face plate. Record flatness/gaps/delamination. Trial the three illuminated buttons, LCD, knob, 3.4 mm fascia fixings and display bosses; rear collars/piezo seat are retained blind pockets. D10 is unused. This dry fit does not test lamp circuitry.

A18-04: review the actual combined R18 tower/fascia job for complete plate continuity, remaining supports, orientations, critical interfaces and imported units. Resolve warnings before accepted manufacture. Record printer/material/process, critical dimensions, STL hashes and full dry-assembly photographs, including water tube, relay terminals, service loops, screw access and planter lift. No numerical strength or fit tolerance is invented.

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A18-01 | ________________________ | Not tested / __________ |
| A18-02 | ________________________ | Not tested / __________ |
| A18-03 | ________________________ | Not tested / __________ |
| A18-04 | ________________________ | Not tested / __________ |

Owner: Unassigned for all A18 actions. Target dates: Not set. Test article/hashes: ____________________. Agreed criteria and instrument basis: ____________________. Deviations: ____________________. Retest evidence: ____________________.

## Close-out and disposition

| Action | Result | Evidence / owner / target |
| --- | --- | --- |
| A17-01 | Not tested / Open | ________________ |
| A17-02 | Open; registration Reported only | ________________ |
| A17-03 | Not tested / Open | ________________ |
| A17-04 | Not tested / Open | ________________ |
| A17-05 | Open; registration Reported only | ________________ |
| A17-06 | Not tested / Open | ________________ |
| A17-07 | Not tested / Open | ________________ |
| A17-08 | Not tested / Open | ________________ |
| A17-09 | Not tested / Open | ________________ |
| A17-10 | Not tested / Open | ________________ |
| A17-11 | Not tested / Open | ________________ |
| A17-12 | Not tested / Open | ________________ |
| A17-13 | Not tested / Open | ________________ |
| A18-01 | Not tested / Open | ________________ |
| A18-02 | Not tested / Open | ________________ |
| A18-03 | Not tested / Open | ________________ |
| A18-04 | Not tested / Open | ________________ |

Closed actions: None pre-populated. A17-01 to A17-13 remain open, alongside A18-01 to A18-04. Reported Arduino/relay registration is partial evidence only. Open deviations: ____________________. Reviewer/name/date: ____________________. Accepted article/configuration/limits: ____________________.

Current disposition: combined R18 prototype review with manufacturing, physical and electrical acceptance open. Each signed result applies only to the identified article and recorded criteria. Neither reported board fit nor digital geometry checks establish leak, power, ingress or unattended-operation acceptance.
