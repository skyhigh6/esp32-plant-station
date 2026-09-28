# Plant Station R17 - Design Review

**PLANT-TR-001 / R17 / D02 / 28 September 2026**

Issued for prototype review; physical acceptance open

Current mechanical configuration: R17 integrated body, R16 lid (R15 geometry), R13 fascia and planter. Electrical reference: frozen Uno UI v6 source and 27 September interface record. Fit, powered wet operation and unattended operation remain unaccepted.

## Revision control

- R5-R13 / source history: Earlier assembly and mechanical changes remain traceable through the preserved D01 matrix. Missing document editions are not invented.
- R14 / preceding manual: AM R14 D01: Uno mounting and motor-disabled bench v2. TR's latest located same-family PDF is R13 D01; no TR R14 PDF is assumed.
- R15 / 27 Sep 2026: Reinforced Uno bosses, thicker recessed-head lid and additional pump relief; source changes incorporated at R17, physical trials open.
- R16 / 27 Sep 2026: Four relay bosses below Uno; source change incorporated at R17; actual underside and hole pitch unmeasured.
- UI v6 / 27 Sep 2026: Three buttons and integrated lamps, enabled active-HIGH relay, 1-4 s request, soil display and 60 s backlight timeout. Firmware revision is independent of mechanical R17.
- R17 / 28 Sep 2026: Mounted USB-C cut and pilots, adjacent diameter 10 DC extension hole; estimated dimensions authorised; coupon fit required.
- D02 / 28 Sep 2026: Integrated current R17 document issue. Uses the established enhanced template, controls and cumulative revision bars. No R15/R16 manual issues created.

R5 is the earliest located assembly guide. R1-R4 and R9-R12 PDFs were not located in the previous inventory. R15/R16 are evidenced mechanical prototype changes, incorporated here without fictitious intermediate PDF/manual editions. Margin labels identify documentary changes, not physical test passes.

## 01 Current state and incorporated changes

![Actual assembled STL review; electronic hardware omitted.](assets/r17_assembled_review.png)

Actual assembled STL review; electronic hardware omitted.

R17 incorporates R14 Uno registration, R15 splitting/lid/pump rectifications, R16 relay mounting and the R17 two-port panel. Current firmware scope is Uno UI v6. Digital geometry is available for prototype trials; physical fit and powered wet acceptance remain open.
*Revision labels: R17; change IDs: T17-4.*

R14 was the reported printed baseline. Its Uno supports split during screw insertion. The user requested a thicker recessed-head roof and removal of the pump/tube obstruction; R15 records these changes. Screw dimensions, printed material and causal strength evidence are still absent.
*Revision labels: R15; change IDs: T15-1, T15-2, T15-3.*

This is the next located design-review document after TR R13 D01. R14-R16 geometry/evidence is incorporated without asserting missing same-family PDFs. R17 documents supersede their current assembly instructions, not the retained historical evidence.

## 02 Known constraints and configuration contract

| Interface | Current basis | Evidence status |
| --- | --- | --- |
| Body | 207 x 100 x 158; integrated tower/sump | Confirmed export bounds |
| Lid | 99 x 100 x 5.5; top z163.5 | Confirmed retained R15/R16 CAD |
| Uno | Four asymmetric R14 centres; y76 seat | Source-verified; actual variant fit open |
| Bosses | 8.5 tip / 10 root / 19 projection; 2.8 x 11 pilot | Prototype; physical screw fit open |
| Relay | 50 x 26 PCB; 44.5 x 20.5 pitch | Seller/photo nominal; underside unknown |
| USB panel | 9.8 x 4.2 R1.2, 2.8 pilots at 15.2 pitch | Authorised best guesses |
| DC panel | Diameter 10; centre 28 from USB | User hole size; nut/grip unknown |
| Wet route | 4 floor; separate tube/wire paths; sensor edge z60 | Geometry checked; no fill limit |

Preserve the wet/dry partition, planter serviceability, fascia interface and asymmetric board registration. Physical hardware measurements outrank the provisional proxy dimensions. No new firmware modification is included in R17 documentation.

## 03 Mount, lid and pump options

| Feature | Options and trade-off | Selected prototype / gate |
| --- | --- | --- |
| Uno mount | Thicker/tapered bosses retain four-screw assembly; inserts/captive nuts improve repeated service but need new fit/access data | R15 reinforced bosses retained. Coupon required; splitting cause is unproven |
| Lid | Thicker pocketed lid gives flush heads; unchanged thin roof preserves old shape but misses request | R15 5.5 thick, 6.6 x 2.5 pockets; head/engagement trial |
| Pump route | Rotate pump may avoid relief but restrict service; lower local relief removes reported ledge | R15 relief x106.5-132/y83-94/z4-52; actual attached tube trial |
| Relay placement | Vertical below Uno consumes nominal height; side wall conflicts with access; rear-wall horizontal gives service space | R16 horizontal, 12 mm above saddle and 13 below Uno; terminal/wire fit open |

Recommendation: retain the selected R15/R16 geometry for representative trials. Do not switch fastener architecture or widen pilots in the body without actual trial evidence and regenerated exports. Fit and retention are separate from digital solid validity.

## 04 USB-C and barrel panel decision

![Left-wall mesh detail; both openings are at z108.5.](assets/r17_left_panel_detail.png)

Left-wall mesh detail; both openings are at z108.5.

| Option | Benefit | Trade-off |
| --- | --- | --- |
| Integral wall cuts (selected) | Matches requested fixed panel; no extra printed part | Estimated USB fit and 6 mm DC grip must pass coupon |
| Replaceable connector insert | Easier later adjustment to another USB/DC component | Adds fastening, seams and another controlled part |
| Retain broad cable opening | Accepts direct original cable access | Does not implement requested fixed sockets |

The user requested the fixed USB/DC panel and explicitly authorised best guesses with PCB-sized holes. Integral wall cuts are selected for this prototype. USB shell cut 9.8 x 4.2 R1.2; pilots 2.8 through at 15.2 pitch; DC diameter 10. USB y63, DC y35, common z108.5.
*Revision labels: R17; change IDs: T17-1.*

Estimated pilot-to-cut material is 1.3 mm. Image flange width 20.1 gives 12.95 mm to the DC cut; a guessed diameter-20 nut would leave 7.95 mm. These calculations depend on unmeasured component envelopes and do not establish fit or strength.
*Revision labels: R17; change IDs: T17-1.*

**CAUTION:** Recommendation: coupon both actual connectors together, including mating plugs, nut grip, screw tips and solder service. Keep the electrical pin/power interface open until characterised; no USB-C rating or source behaviour follows from the cut.
*Revision labels: R17; change IDs: T17-5.*

## 05 Electrical and firmware configuration impact

R14 disabled-motor bench v2 and spare third switch are historical. Current source enables active-HIGH D9 relay requests and uses D2/D3/D4 switches; D5/D6/D7 red/yellow/green lamps. A4/A5 serve LCD; A0/A1 serve probe/pot; D10 is unused.
*Revision labels: R17; change IDs: T17-2.*

Dose requests are 1-4 s, knob sampled once. Yellow cycles pages/holds lamp test/cancels; STOP cancels and two-second hold clears session counters. Sensor is advisory; below 25% red blink, at/above green, raw <=20 fault. Software STOP and sensor fault do not provide hardware isolation.
*Revision labels: R17; change IDs: T17-3.*

UI v6 commands soil Status return at request end and I2C backlight off after 60 s idle, waking on buttons or >=8 ADC pot-count change. Serial OFF/ON and LCD status 0 were recorded on 27 September; earlier communication failures and visual/post-dose checks remain open.
*Revision labels: R17; change IDs: T17-3, T17-4.*

**CAUTION:** Relay module/pump rating, current, supply behaviour and reset default-OFF are unmeasured. USB-C pins/configuration and barrel polarity/grip are unresolved. CAD provision does not accept a new power system. Keep a physical pump disconnect.

## 06 Evidence and digital verification limits

| Evidence | Recorded result | Limit |
| --- | --- | --- |
| R15 independent checker | Six final meshes/sections passed | Fastener, pump and leak physical gates open |
| R16 independent checker | Three single-component meshes and relay sections passed | Nominal board envelope only; underside unmeasured |
| R17 STEP/readback | Both exports reopened as one valid solid | Builder process still exits 1 on shutdown |
| R17 independent STL | Two closed consistently wound meshes; all edges two-face; no degenerate faces | Full mesh self-intersection not checked |
| R17 sections | Six wall sections: USB 9.800 x 4.200, DC approx 9.998 centre section, pilots approx 2.800 | Tessellated mesh dimensions; not printed-hole readings |
| R17 change scope | 0 added/removed mm3 outside left-wall mask | Does not establish physical insertion or strength |
| UI v6 source and record | Current SHA-256 matches 27 September upload record | No new hardware run in this documentation task |

Nominal module proxies have zero digital interference with the body/board proxies. Actual component fronts, solder, plug bodies and service loops are not represented accurately enough for physical acceptance. No slicing, physical print, continuous swept-lift or wet test is claimed.

## 07 Risks, unknowns and closure actions

| ID / type | Condition and effect | Mitigation / closure |
| --- | --- | --- |
| RI17-01 / Issue | USB cut/pitch and jack grip unmeasured; mismatch could require a body reprint | A17-01 coupon plus actual measurements |
| RI17-02 / Issue | Reported R14 boss splitting; R15 reinforcement physically untested | A17-02 screw/material/orientation trial; inspect root and tip |
| RI17-03 / Risk | Relay solder/terminals and fascia services may collide | A17-05/06 full assembled dry fit and removal trial |
| RI17-04 / Issue | LCD intermittent communication faults; screen may fail under load | A17-09 supply/I2C/suppression investigation and repeat observations |
| RI17-05 / Risk | Relay closure through boot/reset or welded contacts may leave pump running | A17-08 measured default-OFF; physical disconnect |
| RI17-06 / Issue | Fill/leak/material limits unknown; ingress into electronics possible | A17-11/12 material qualification and controlled leak/drain-back/splash evidence |
| RI17-07 / Issue | USB/barrel wiring and rating unresolved | A17-07 identified source diagram, continuity and load evidence |
| RI17-08 / Issue | CAD exit code 1 prevents a clean-build claim | A17-13 isolate shutdown cause or retain explicit exception |

Risk ratings are qualitative; no likelihood/severity matrix was supplied. All owners are Unassigned, target dates Not set, and all entries remain Open. USB guesses, relay nominal dimensions, screw torque, printer/material, supply/load limits and acceptance tolerances remain Unknown or Assumed as identified.

## 08 Acceptance recommendation and next actions

1. Print and fit the R17 port coupon; in parallel complete the matching Uno, lid, pump and relay trials. Record measurements and photographs. 2. Correct failed dimensions and re-export only affected geometry. 3. Complete full-body slicing review and dry serviceability fit. 4. Close the electrical interface and relay default-OFF evidence before supervised powered testing. 5. Close leak/fill and dose-volume evidence before accepted supervised wet use.
*Revision labels: R17; change IDs: T17-4.*

PLANT-TS-001 contains testable A17-01 to A17-13 records. A recommendation is not an acceptance signature. Current disposition: prototype review; digital evidence recorded; physical/electrical acceptance open.

References are frozen in the package evidence register. Prior enhanced D01 scheme/matrix is retained alongside the extended R17 change matrix. No R15/R16 manual issues or missing early PDFs were created.
