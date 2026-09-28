# Plant Station R17 - Test and Acceptance Sheets

**PLANT-TS-001 / R17 / D02 / 28 September 2026**

Issued for prototype review; physical acceptance open

Current mechanical configuration: R17 integrated body, R16 lid (R15 geometry), R13 fascia and planter. Electrical reference: frozen Uno UI v6 source and 27 September interface record. Fit, powered wet operation and unattended operation remain unaccepted.

## Revision control

- R5-R13 / source history: Earlier assembly and mechanical changes remain traceable through the preserved D01 matrix. Missing document editions are not invented.
- TS family / D02: PLANT-TS-001 assigned for this test-sheet set. Prior tests are source evidence; no earlier same-family controlled test-sheet issue is asserted.
- R15 / 27 Sep 2026: Reinforced Uno bosses, thicker recessed-head lid and additional pump relief; source changes incorporated at R17, physical trials open.
- R16 / 27 Sep 2026: Four relay bosses below Uno; source change incorporated at R17; actual underside and hole pitch unmeasured.
- UI v6 / 27 Sep 2026: Three buttons and integrated lamps, enabled active-HIGH relay, 1-4 s request, soil display and 60 s backlight timeout. Firmware revision is independent of mechanical R17.
- R17 / 28 Sep 2026: Mounted USB-C cut and pilots, adjacent diameter 10 DC extension hole; estimated dimensions authorised; coupon fit required.
- D02 / 28 Sep 2026: Integrated current R17 document issue. Uses the established enhanced template, controls and cumulative revision bars. No R15/R16 manual issues created.

R5 is the earliest located assembly guide. R1-R4 and R9-R12 PDFs were not located in the previous inventory. R15/R16 are evidenced mechanical prototype changes, incorporated here without fictitious intermediate PDF/manual editions. Margin labels identify documentary changes, not physical test passes.

## 01 Test article, prerequisites and recording rules

Test article: one R17 prototype using the controlled selected print files and frozen Uno UI v6 source. This sheet set defines future physical tests; it records no new physical passes. Link each action to a build ID, source hash, operator/date, actual configuration and retained evidence.
*Revision labels: R17; change IDs: T17-4.*

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

**CAUTION:** Before electrical work disconnect every supply. Before powered logic/upload checks confirm the separate pump supply is OFF. No upload, printer operation or powered test is executed by this document.

Use Pass / Fail / Not tested / Deferred with evidence. A blank actual result remains Not tested. Acceptance tolerances not supplied must be agreed and recorded before assessing that test; do not invent acceptable duration, volume, torque or leak rates.

## 02 Mechanical coupons and dry assembly

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-01 | USB/DC fit coupon | USB shell and screw pattern fit; plug engages; DC thread/nut span 6 mm; no cracks | Not tested |
| A17-02 | Uno screws and board | 2.8 pilot trial takes actual screws; all four centres register without PCB bowing | Not tested |
| A17-03 | Flush lid | Heads sit flush/below surface; pockets intact; lid seats; engagement verified | Not tested |
| A17-04 | Pump route | Actual pump/tube clear relief; no kink; dry partition preserved | Not tested |
| A17-05 | Relay fit | Four-hole registration; solder, screws, terminals and service removal clear | Not tested |
| A17-06 | Fascia and full dry build | LCD/buttons/pot fit; wiring untrapped; planter lifts clear; all fasteners retain | Not tested |

A17-01: print the port coupon in the intended material; measure both mounting centres and each cut; trial connectors, fasteners, actual plugs, DC nut and solder/wire access together.
*Revision labels: R17; change IDs: T17-4.*

A17-02: trial actual screws in full-length 2.8 mm bosses; measure engagement and remaining pilot-depth margin. Inspect splitting/retention and all four Uno holes before approving a body change.
*Revision labels: R17; change IDs: T17-4.*

A17-03/04: trial actual lid heads and pump with attached tube against matching coupons, then check seat, clearances, removal and dry boundary in the body.
*Revision labels: R17; change IDs: T17-4.*

A17-05/06: measure relay hole pitch/underside; fit all four screws. Dry-build fascia, boards, wiring and planter; inspect tool access, contact/solder clearance and full removal travel.
*Revision labels: R17; change IDs: T17-4.*

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-01 | ________________________ | Not tested / __________ |
| A17-02 | ________________________ | Not tested / __________ |
| A17-03 | ________________________ | Not tested / __________ |
| A17-04 | ________________________ | Not tested / __________ |
| A17-05 | ________________________ | Not tested / __________ |
| A17-06 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## 03 Power interface and relay reset acceptance

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-07 | USB/barrel electrical interface | Exact USB pins/CC/power/data, DC polarity/voltage and source behaviour identified | Open design hold |
| A17-08 | Relay default OFF | Coil/input/contact ratings recorded; OFF through reset and both supply sequences | Not tested |

A17-07: identify USB-C part/pins and intended power/data adaptation; inspect configuration-channel provision. Measure actual DC extension polarity, mating dimensions and grip. Freeze the approved input diagram and source selection before energising it.
*Revision labels: R17; change IDs: T17-4.*

Record USB input, board rails and barrel input voltages/current under the agreed load. Record the intended supply arrangement and unwanted coupling tests appropriate to it. Define numerical pass limits from matching component specifications first.
*Revision labels: R17; change IDs: T17-4.*

A17-08: with pump disconnected, identify coil/input/contact ratings and measure contact state through board reset, open logic input and both source power-up orders. Expected contact state is OFF throughout inhibit conditions; stop on any transient closure.
*Revision labels: R17; change IDs: T17-4.*

Verify an accessible physical pump-power disconnect, selected fuse/wire/contact ratings and motor suppression. Do not substitute a software OFF message for measured contact state.
*Revision labels: R17; change IDs: T17-4.*

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-07 | ________________________ | Not tested / __________ |
| A17-08 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## 04 LCD, controls and dose measurements

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-09 | LCD and controls | Display stable, buttons/lamps verified, dose return and full 60 s timeout observed | Partial serial record only |
| A17-10 | Dose and volume | Actual contact/pump durations and volume measured at selected endpoints | Not measured |

A17-09: with pump supply OFF, verify each switch and lamp; stable LCD status 0 and visible pages; STOP/release lockout; 1-4 s indicated endpoints; safe soil-index/fault test inputs; no automatic request from moisture.
*Revision labels: R17; change IDs: T17-4.*

Observe and record the actual LCD backlight after 60 s idle, button/knob wake and 60 s after completed/cancelled requests. Confirm immediate soil Status return at request end. Retain video/timed observation and serial as separate evidence.
*Revision labels: R17; change IDs: T17-4.*

A17-10: after power/reset protections pass, run a supervised measured pump trial using the approved supply and installed tube/lift. Measure contact ON duration and delivered volume at 1.0/4.0 s settings and intermediate points required by the intended use.
*Revision labels: R17; change IDs: T17-4.*

Timing and volume acceptance tolerances: Not yet defined. Record instrumentation resolution, repetitions, individual readings, mean/range and failures. Do not mark a test Pass without the pre-set numerical criteria.
*Revision labels: R17; change IDs: T17-4.*

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-09 | ________________________ | Not tested / __________ |
| A17-10 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## 05 Leak/fill, print configuration and CAD exception

| Action ID | Test | Expected acceptance | Existing status |
| --- | --- | --- | --- |
| A17-11 | Leak/fill and wet route | Leak, drain-back, tilt/splash evidence; fill limit below unsealed openings recorded | Not tested |
| A17-12 | Material/print configuration | Material, slicer layers, orientation, local fit/strength recorded | Unknown |
| A17-13 | CAD shutdown anomaly | Clean CAD process log or isolated dependency defect with retained evidence | Open; build exits 1 |

A17-11: define leak-test duration, fill candidate, containment and acceptance first. Record actual water level, drain-back headspace, soil/drain condition, planter movement, tilt/splash exposure and dry-tower inspection. Fill mark acceptance needs physical evidence.
*Revision labels: R17; change IDs: T17-4.*

A17-12: record material and printing process, orientation/supports, layer inspection and measured critical holes. Representative screw and connector coupons must match the material/process of the intended body.
*Revision labels: R17; change IDs: T17-4.*

A17-13: retain the build output and exit code. Current R17 builder prints PASS but exits 1 during shutdown; independent STL checker exits 0. Closing this exception needs a clean process or isolated dependency-defect evidence; it never closes physical fit.
*Revision labels: R17; change IDs: T17-4.*

| Action ID | Actual result / evidence | Verdict / operator / date |
| --- | --- | --- |
| A17-11 | ________________________ | Not tested / __________ |
| A17-12 | ________________________ | Not tested / __________ |
| A17-13 | ________________________ | Not tested / __________ |

Owner: Unassigned. Target date: Not set. Deviations and corrective action: ____________________. Retest configuration/evidence: ____________________.

## 06 Close-out and disposition

| Action | Result | Evidence / owner / target |
| --- | --- | --- |
| A17-01 | Not tested / Open | ________________ |
| A17-02 | Not tested / Open | ________________ |
| A17-03 | Not tested / Open | ________________ |
| A17-04 | Not tested / Open | ________________ |
| A17-05 | Not tested / Open | ________________ |
| A17-06 | Not tested / Open | ________________ |
| A17-07 | Not tested / Open | ________________ |
| A17-08 | Not tested / Open | ________________ |
| A17-09 | Not tested / Open | ________________ |
| A17-10 | Not tested / Open | ________________ |
| A17-11 | Not tested / Open | ________________ |
| A17-12 | Not tested / Open | ________________ |
| A17-13 | Not tested / Open | ________________ |

Closed actions: None pre-populated. Open defects/deviations: ____________________. Reviewer/name/date: ____________________. Accepted configuration and limits: ____________________.
*Revision labels: R17; change IDs: T17-4.*

**CAUTION:** Current disposition remains prototype review with physical acceptance open. A signed worksheet closes only the identified test article and recorded criteria; it does not infer an ingress rating, certification or unattended-operation acceptance.
