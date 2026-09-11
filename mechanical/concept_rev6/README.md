# Plant station R6 — sump pump and 12 mm button inserts

11 September 2026. Units: millimetres. Geometry checked, provisional hardware fit. R5 retained unchanged.

## Changes

- Sump external height increased from 40 to **60 mm**, retaining its 106 × 100 mm main footprint and 4 mm floor. Internal depth is **56 mm**; interior plan envelope remains 94 × 88 mm with rounded corners.
- Planting module raised **20 mm**, retaining its 90 × 60 × 50 mm soil compartment, exactly two Ø6 mm drains and mating lip. Assembly height remains 161 mm because the electronics tower is unchanged.
- Checked space for the shortlisted **38.5 × 25.5 × 43 mm** pump body, with 3 mm lateral/top allowance. This is the COM3700 envelope from the sourcing register, not a measurement of Kev's pump. Pump body top is 13 mm below the main planter underside and 10 mm below the peripheral lip level. Outlet fittings, cable bend, minimum submersion and suction feet must fit within the remaining space.
- Three **Ø12.0 mm through-holes** for the purchased button inserts, on 24 mm centres. Hole positions: x=24/48/72, z=72; fascia thickness 3 mm. R5 already had nominal Ø12 bores, so the fascia was retained and explicitly checked for the insert envelopes.
- Provisional insert clearances checked behind each hole: Ø20 mm nut envelope for the first 5 mm, then Ø16 mm body/wiring envelope to 35 mm behind the panel. Adjacent Ø20 mm nuts have 4 mm separation. These envelopes do not identify the actual purchased switches.
- Hose clip bore increased from 7.0 to **8.4 mm**, comprising 8.0 mm tube OD plus 0.4 mm diametral allowance. Clip throat remains open; retention requires a physical test.
- Rear service notch widened to **18 mm** and extended through the skirt top, with independent clear paths for an 8.4 mm hose envelope and a 4 mm cable envelope. The notch remains outside the soil cavity. It is open, not a watertight gland.
- Added a 3 mm-thick button fit coupon with Ø12.0, Ø12.2 and Ø12.4 mm holes. The corner notch identifies the Ø12.0 end; sizes increase away from it. The production fascia remains Ø12.0 without silent print compensation.

## Component contract

| Dimension | Value | Evidence/status |
|---|---|---|
| Button panel holes | 12.0 mm | User specified 11 September |
| Button style | Metal inserts, ring illumination, red/green/yellow purchase images | Photo; selected diameter, momentary/latching variant, LED voltage, rear depth and nut dimensions are not visible |
| Button rear/nut space | 35 mm projection, 20 mm nut diameter | Design allowance, unmeasured |
| Pump body | 38.5 L × 25.5 W × 43 H mm | Shortlisted COM3700 dimensions in parts register; assumed intended pump |
| Pump mounting | Loose placement on sump floor | No exact retention mount claimed; suction feet or removable restraint require actual pump dimensions |
| ESP32 carrier mounting centres | 60 × 55 mm | Preserved user measurement |
| LCD mounting centres/aperture | 73 × 30 mm / 70 × 25 mm | Preserved user measurements |
| Tube | 8 mm OD | Sourcing candidate; actual hose unmeasured |

The photo does not confirm the switches are momentary or that their illumination works at the controller supply. This mechanical revision does not change the firmware or button wiring. Existing separate LED holes are retained.

## Files and replacement guidance

`stl/` contains seven assembly parts plus the coupon. `step/` contains each editable solid and coupon; `assembly.step` preserves assembly coordinates. `pump_envelope_reference.step` is a rectangular reference volume, not a printable part or manufacturer CAD.

For an already printed R5 assembly, replace **sump_charcoal**, **planter_sage** and **hose_clip** together. The tower, fascia, lid and battery tray retain their R5 geometry. Reprint the fascia only if not already available or if physical insert testing shows compensation is needed. R5 and R6 sump/planter heights must not be mixed.

All assembly STLs retain common coordinates. Import as millimetres without auto-arrange to inspect the assembly; orient and place individual parts on the print bed for slicing. Printer, material, supports and print envelope remain unverified.

## Verification

- CadQuery 2.8.0: seven valid single-body assembly solids; all 21 pairwise intersections zero within 0.00001 mm³, with a 500 mm³ positive overlap control.
- Required bores, LCD aperture, drains, sump floor, pump clearance, button insert envelopes, rear passages and hose clip opening checked directly against CAD solids.
- Independent mesh reader reopens all eight exported STLs: closed, consistent winding, positive volume, one component each; all mesh edges shared by two faces, no degenerate faces.
- Cross-sections of exported fascia and coupon confirm the intended button diameters within tessellation tolerance; exported sump height is 60 mm.
- Assembly and section previews visually inspected. See `verification.json` and `independent_mesh_check.json` for results and STL hashes.
- Local CAD process again printed PASS after exports and checks, then exited with code 1 during shutdown without traceback, as in R5. This is recorded rather than represented as a clean process exit. The independent mesh checker exits successfully.

Not performed: slicing, physical fit, full self-intersection analysis, leak/strength/material tests, electrical commissioning. No pump or switch operational approval is implied.

## First checks on the bench

1. Print the button coupon; confirm body passage, thread engagement through 3 mm material and retaining-nut size. Test the actual selected momentary/latching action separately.
2. Measure the pump including outlet/feet/cable; compare with the reference envelope before printing the full sump. Check minimum working water level and hose bend under the planting module.
3. Test the enlarged hose clip on the actual tube. Avoid crushing the bore; verify retention.
4. Print and fit the sump/planter pair. Use appropriate removable inlet/drain screens and prove water containment before installing electronics. Leave headspace for drain-back; the geometric cavity is not a recommended fill volume.
5. Fit the buttons from the outside, tighten nuts inside with the fascia removed, route wiring, then install the fascia. Confirm wiring clears the PCB and LCD envelopes.
