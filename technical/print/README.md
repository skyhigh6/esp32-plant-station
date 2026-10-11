# Current print exports — R18 / D03

`manifest.json` identifies STL/STEP files, hashes, source revisions and selection status. Units: mm. STL has no explicit units metadata; check imported size.

## Select these parts

| Part | STL | Matching STEP |
|---|---|---|
| R18 tower/sump | [tower_open_pump_route_r18.stl](main_parts/stl/tower_open_pump_route_r18.stl) | [tower_open_pump_route_r18.step](main_parts/step/tower_open_pump_route_r18.step) |
| R18 fascia | [fascia_no_aux_apertures_r18.stl](main_parts/stl/fascia_no_aux_apertures_r18.stl) | [fascia_no_aux_apertures_r18.step](main_parts/step/fascia_no_aux_apertures_r18.step) |
| Retained R16 lid / R15 geometry | [top_cover_flush_r16.stl](main_parts/stl/top_cover_flush_r16.stl) | [top_cover_flush_r16.step](main_parts/step/top_cover_flush_r16.step) |
| Retained R13 planter | [planter_sage.stl](main_parts/stl/planter_sage.stl) | [planter_sage.step](main_parts/step/planter_sage.step) |

Choose **one** `knob_options/` variant for the actual shaft. Do not print all alternatives. Original `tower_sump_body_uno_ports_r17` and `fascia_charcoal` files are frozen predecessor inputs, not current R18 selections.

## Print and acceptance sequence

1. Check actual USB/DC hardware with [power_ports_fit_coupon_r17.stl](fit_trials/stl/power_ports_fit_coupon_r17.stl). Its estimated USB aperture/pilots and Ø10 mm DC opening remain the R18 interfaces.
2. Use [route_trial_r18.stl](fit_trials/stl/route_trial_r18.stl) / [STEP](fit_trials/step/route_trial_r18.step) optionally for local bundle width and lay-in clearance. Its 29 × 20 × 60 mm corner does not accept full-route retention/strength.
3. Select relevant retained boss, relay, lid and control trials. Kevin's reported Uno/relay fit does not close controlled test records.
4. Import current R18 main STLs, check size/orientation and inspect layers/supports for the actual material/process. The open route removes selected tunnel ceilings; other features may still need support.
5. Inspect printed edges and fascia continuity/flatness. Dry-fit all hardware and retained parts together; check smooth bends, service slack, retention and pinching. Record actual observations in the R18 sheets.

`plate_layout/r17_plate_layout.3mf` and files in `slicer_exports/` are **historical R17 projects/toolpaths**. Their prior geometry/metadata checks remain evidence. Prepare new R18 slicing; these files are not current R18 printer instructions. C01 comparison slices are also evidence only.

See the [assembly manual](../../docs/documents/AM_R18/PLANT-AM-001_R18_D03.pdf), [test sheets](../../docs/documents/TS_R18/PLANT-TS-001_R18_D03.pdf) and [project control](../../PROJECT_CONTROL.md). Print, dry fit, leak and electrical acceptance remain open.
