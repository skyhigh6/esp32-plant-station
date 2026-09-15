# R14 change note and verification disposition

Document ID: PLANT-CN-UNO-MOUNTS
15 Sep 2026 | Revision R14 | Status: issued for prototype review; physical acceptance open.

## Outcome and scope

The integrated R13 tower/sump is revised to support the Arduino Uno R3 four-hole pattern. This issue changes the board mounts only. User authority: request to redo the tower standoffs for an Uno, followed by completion of revision documentation and Git publication.

## Configuration and evidence

- Baseline: R13 `tower_sump_body.step`; original retained.
- Replacement: `stl/tower_sump_body_uno.stl` and matching STEP.
- Retained main parts: R13 fascia_charcoal, top_cover_sage and planter_sage. Existing knobs and other non-carrier accessories remain R13.
- Retire the SunFounder carrier fit coupon for this configuration; use `uno_mount_fit_coupon`.
- E01: `references/UNO-TH_Rev3e.brd`, official Arduino CAD, hole elements and board outline. Source and licence retained.
- E02: `build.py` and `verification.json`, CAD validity, STEP re-import and baseline comparison.
- E03: `independent_mesh_check.json`, final STL topology, dimensions and mount sections.
- E04: `preview.png` and `mount_section.png`, visually reviewed geometry.

## Findings

Confirmed: four asymmetric centres, 6 mm bosses, 2.8 mm pilots and 18 mm rear clearance are modelled. Body bounds remain 207 x 100 x 158 mm. CAD comparison found 0 mm3 added and 0 mm3 removed outside the union of old/new mount regions. The nominal board envelope has zero solid interference. Both exports are valid single CAD solids and re-import as valid single STEP solids.

Confirmed limitation: build printed PASS, then exited 1 without a traceback during shutdown. Cause is unknown; behaviour also occurs in R13. All recorded assertions completed before shutdown. This does not count as a clean build-process exit. The separate mesh checker must exit 0.

Assumed: supplied board follows Uno R3 geometry; 2.8 mm printed pilots suit the chosen M3 screw/tapping method. Neither is physically established. Connector, component and screw-head envelopes are not represented by the plain board envelope check.

## Design decision and impact

Replace mounts directly rather than add an adapter plate: fewer parts and preserved seating plane, but requires a replacement body print. Keep the existing enclosure interfaces to contain this change. No full assembly, continuous insertion, firmware or electrical requalification is claimed. Prior R13 checks remain historical evidence for retained geometry.

The USB opening remains the R13 carrier opening. Direct Uno plug access is unverified; closure requires a cable-fit trial. The four small seating faces reduce contact footprint but do not prove clearance from solder joints or components.

## Acceptance and open actions

Physical acceptance is governed by [ACCEPTANCE.md](ACCEPTANCE.md). No slicing, print, fit, strength, leak or powered-operation test was performed. R13 water-level and low sensor-entry restrictions remain applicable. This revision gives no approved fill level.

## Revision history

R14, 15 Sep 2026: Uno mounting conversion; new fit coupon, source CAD reference, export checks and release documentation. R13 remains the source for retained parts and earlier assembly guidance.
