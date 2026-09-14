# R12 release verification

14 September 2026. Model and source review performed 13 September; final release checks 14 September. Baseline R11.

- Five main printable parts; 20 exported meshes pass independent closure, winding, component, volume, edge-incidence and degenerate-face checks. Independent checker exit 0; current export hashes rechecked for release.
- 20 STEP files reopened as valid single solids; five-solid assembly. STL dimensions/volumes agree. Known CadQuery shutdown exit 1 follows passing CAD and STEP assertions; no clean process exit claimed.
- Ten main-part pair intersections clear. 61 planter lift positions at 2 mm steps through 120 mm clear. Divider continuity, supported riser, battery space and tie-tunnel checks pass.
- Exported sections verify 10 mm tube bore, 8 mm pump-wire bore, independent 8 mm sensor entry and retained 6 x 2.5 mm tie slot. CAD envelopes check an 8 mm tube, two 2.5 mm insulated wires and a 4 mm sensor lead. These are provisional fit envelopes, not verified actual component sizes or bend-radius tests.
- Actual-STL tube/wire and sensor-entry sections visually reviewed. Sensor entry lower edge z124 is 8 mm above planter top z116; tube exit z128 is 12 mm above planter. Pump-wire crossover lower edge z77 is 17 mm above sump rim z60. Water tubing remains outside the electronics cavity.
- No slicing, printing, strain-relief, actual connector/lead/tube fit, water-level, leak, strength or powered electrical tests.

Changed STL hashes from R11: planter_sage.stl, tower_sump_body.stl, upper_boss_print_coupon.stl.
