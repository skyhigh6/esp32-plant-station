# Plant Station mechanical R5

09 September 2026. Current mechanical review revision; earlier revisions preserved.

## Changes
- Followed the supplied sage/charcoal concept, with a full-height hollow planter skirt.
- Moved the hose clip fully outside the tower wall and made its shelf pilot accessible. R4 intersected the wall and contained a sealed pilot cavity.
- Added four 8 mm LCD standoffs: OD 5 mm, through-hole 2.4 mm for provisional M2 fixings, maximum head diameter 4 mm.
- Preserved PCB centres 60 x 55 mm, LCD centres 73 x 30 mm and aperture 70 x 25 mm.
- Added a 0.4 mm-clearance sump locating lip and rear tube/cable service notch.
- Repositioned top-cover pilots for improved wall margin.

## Verified geometry
Seven STL files each have one connected closed mesh, consistent winding and positive volume. CAD solids are valid and single-body. All 21 assembled solid-pair intersections are zero to the 1e-5 mm3 threshold; positive overlap control measures 500 mm3. Direct probes verify mounting holes, LCD aperture, drainage and sump floor. No mesh repair or scaling was applied.

PCB fasteners have 7 mm-diameter driver access with the front panel removed. Rear stand-off is 18 mm to the wall. Assumed PCB/LCD component envelopes clear the printed parts and leave 20.8 mm between each other. Assumed PCB edge margin is 4 mm, LCD 2 mm. LCD bosses clear the display aperture by at least 0.415 mm; 4 mm heads clear it by 0.915 mm. See verification.json for dimensions, assumptions and STL SHA-256 hashes.

All seven STLs retain common assembly coordinates (mm). Import together without auto-arrange to inspect the installed positions. For printing, load individually, select orientation and place on the bed. assembly.step is for assembly inspection; step/ contains individual editable solids. build.py is the parametric construction source using the local CadQuery runtime. Previews are rendered from the actual geometry.

## Limits
Actual PCB outline, underside components, LCD backpack, screw heads, holder, pump, USB cable, buttons, sounder and tube size need physical measurement. These assumptions are not confirmed fits. The LCD margin requires a trial fit before full printing. No slicer, material/process validation, thread retention, structural load or leak test has been performed. Full mesh self-intersection analysis was not performed. Extra auxiliary boards still need measured insulating mounts.

The tube clip is nominally 7 mm bore (supersedes the older 8 mm placeholder); confirm actual tube OD. The rear USB window is provisional. The dovetail is not a positive carrying lock; support both modules. Camera/lens geometry is not dimensioned and has not been invented from the art. Firmware remains manual-only with no implemented LCD text output.

CAD runtime note: the local Windows Python/CadQuery process printed PASS after all assertions and exports, then returned code 1 during shutdown without a traceback. Exported results were independently reopened and checked with a separate mesh reader. Do not interpret that shutdown status as a clean process exit; geometry checks and export validation are recorded separately.

## Build guide
See ../../output/pdf/Plant_Station_R5_Illustrated_Build_Guide.pdf for illustrated assembly, mechanical checks, electrical block diagrams, logical pinout, conditional upload steps and acceptance worksheet. Its pinout is compile-review only, not a physical SunFounder header diagram.
