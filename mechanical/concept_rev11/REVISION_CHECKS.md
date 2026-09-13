# R11 validation

User rejected the R10 spanning trough and requested the battery saddle integrated with a tie slot.

- Five main parts; 20 STL/STEP exports. Combined tower/sump/battery saddle is one valid solid and one connected closed mesh.
- All 20 meshes: consistent winding, positive volume, every edge shared by two faces, zero degenerate faces. Independent checker exit 0.
- Reopened STEP parts: 20 valid single solids; five-solid assembly; dimensions/volumes agree with STL. CAD and STEP assertions pass followed by the known CadQuery shutdown exit 1.
- Ten assembly pairs clear; retained full-height wet/dry wall and continuous riser support material probes pass. Old trough absence probe passes.
- Provisional 4 mm cable path probes, battery tie through-path and roof material probes, and unchanged holder-space probe pass. Exported sections verify 8 mm riser bore and 6 x 2.5 mm tie slot.
- 61 planter lift positions (2 mm steps, 0 to 120 mm) clear. Cable/tie sections and isolated interactive body visually reviewed.
- No slicing, material/strength, holder/tie/cable fit, bending, leak or electrical tests. Fill level and actual cable/tie dimensions remain unknown.

Changed STL hashes relative to R10: planter_sage.stl, tower_sump_body.stl, upper_boss_print_coupon.stl. Separate battery_tray.stl and .step are retired in R11.
