# R10 verification record

13 September 2026; baseline R9 checked from actual workspace.

- 21 closed, consistently wound, positive-volume, single-component STL meshes; two faces per edge and no degenerate faces. Independent checker exit 0.
- 21 reopened valid STEP single solids and six-solid assembly; STL bounds/volumes agree. Known CadQuery shutdown exits 1 after passing assertions; not claimed as a clean process exit.
- Six main parts; 15 volumetric pair checks all clear within 0.00001 mm3. Positive 500 mm3 intersection control passes.
- Integrated body continuity and full-height wet/dry wall material probes pass. Connected 4 mm cable route probes pass. 61 planter lift positions, every 2 mm from 0 to 120 mm, have zero overlap with the fixed body.
- Actual STL section at y90.5 and internal CAD view reviewed. Interactive viewer loads six parts and permits combined-body isolation. The schematic cable turn does not validate real bend radius.
- No slicing, physical fit, leak, strength, cable abrasion/retention or electrical operation tests. Actual cable, connector and maximum operating water level remain unknown.

New or changed files: planter_sage.stl, tower_sump_body.stl, upper_boss_print_coupon.stl.

Byte-identical to R9: battery_tray.stl, button_fit_coupon.stl, carrier_fit_coupon.stl, fascia_charcoal.stl, hose_clip.stl, knob_D_6p0.stl, knob_D_6p2.stl, knob_fit_coupon.stl, knob_round_5p0.stl, knob_round_5p2.stl, knob_round_6p0.stl, knob_round_6p2.stl, knob_round_6p35.stl, knob_round_6p55.stl, lcd_fit_coupon.stl, piezo_led_fit_coupon.stl, top_cover_sage.stl, usb_marking_blank.stl.
