# R13 annotated mechanical revision

14 September 2026. Supersedes R12; prior files preserved. Units: mm; x right, y rear, z up.

## Changes

1. Removed the separate hose clip, tower shelf and clip pilot.
2. Supported hose riser now uses R7 vertical outside rounds and R3 top rounds. Separate 10 mm tube and 8 mm pump-wire passages retained.
3. Both lower fascia screw supports now have full feet and added concave R2 floor roots. Rounded-away lower support profiles removed.
4. Removed obsolete battery screw bores and dry-floor fixing pads/pilots. Integrated 72 x 22 mm holder saddle and 6 x 2.5 mm tie tunnel retained.
5. Independent sensor entry lowered to y65/z64, diameter 8: lower edge level with the z60 sump rim. Matching local planter skirt relief clears the sensor lead outside the soil cavity. Pump-wire crossover remains y92/z81.

The organic treatment changes the riser's external shape; actual hose bend radius and retention require a physical trial. The low sensor opening is not a sealed gland or an approved maximum fill level.

## Parts and assembly

Four main parts: tower_sump_body, fascia_charcoal, top_cover_sage and planter_sage. Body 207 x 100 x 158; assembled roof height 161. Nineteen STL/STEP exports include eight knob options, six fit coupons and a USB marking blank. Print only the selected knob.

Replace R12 body and planter. Fascia, roof and existing accessory geometries are retained. Remove the old hose clip. Do not use old battery/clip screws.

See the separate customer-format kit manual and design review under output/pdf. Electronics remain a prototype: exact carrier pin mapping, power path, component identity, third-control role, LCD operation and commissioning are open. No powered operation is authorised by a CAD check.

## Validation

verification.json: four valid main solids, six zero-volume pair intersections, positive/negative feature probes and 61 sampled planter lift checks in 2 mm increments through 120 mm.
independent_mesh_check.json: 19 closed, consistently wound, positive-volume one-component meshes, two faces per edge, no degenerate faces; mount, route and accessory sections checked.
step_check.json: 19 re-imported valid single solids; four-solid assembly; STL bounds within 0.03 mm and volume within 0.2 percent.

Build completed with PASS and no assertion traceback, followed by the existing CadQuery shutdown exit 1. Re-import checker likewise passed then exited 1. Independent mesh and section rendering completed with exit 0. No slicing, full mesh self-intersection, continuous swept-lift, physical fit, strength, leak or electrical tests performed.

## Radius review

Reviewed the source treatments for cavity floor/vertical edges, shell rim, upper supports, PCB root fillets and tip chamfers, USB chamfers, sump/planter/lip vertical corners and service riser. Concave cavity and standoff roots add material to the assembled body; outer corner rounds remove material intentionally. The lower foot treatment was the identified root error and is replaced on both sides. Geometry validity and preview review are not strength verification.

## Rebuild and inspect

Run build.py, check_exports.py, check_step.py and render_cable_section.py using a Python environment containing CadQuery 2.8, trimesh, NumPy, VTK, matplotlib and networkx. Run scripts/build_guide_r13.py with ReportLab after the illustration is present. The builder imports the workspace-local .tools/cad-runtime when present.

Viewer: python -m http.server 8770 --bind 127.0.0.1 --directory mechanical/concept_rev13
Open http://127.0.0.1:8770/viewer/

Source dimensional references remain mechanical/concept_rev8/references and docs/PROJECT_CONTROL.md. This revision changes no firmware. AI_IMAGE_PROVENANCE.md records the generated illustration and its limitations.
