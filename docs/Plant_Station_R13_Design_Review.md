# R13 | Design change and verification

14 September 2026 / Supersedes R12 mechanical geometry / Units: mm

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\product_ai.png)

Five browser annotations implemented. Four main enclosure parts; selected knob and fit coupons are separate. The illustration is generated appearance guidance; the exported CAD remains dimensional authority.

Body: 207 x 100 x 158 mm. Overall roof height: 161 mm. Changes are local to the combined body and planter; fascia, roof and knob interfaces are retained.

# Annotation disposition and radius audit

1. <b>Clip:</b> removed the separate hose clip, its shelf and shelf pilot. The tower has no retained clip attachment point.

2. <b>Hose route appearance:</b> enlarged vertical outside rounds from R1 to R7 and added R3 top rounds to the supported riser. Separate 10 mm tube and 8 mm pump-wire bores remain. Physical tubing bend radius is still unknown.

3. <b>Screw block:</b> replaced the rounded lower support profile with full feet and added concave R2 floor roots on both sides. Material probes verify the feet are filled. Audited cavity floor/vertical, shell rim, upper webs, board roots/tips, USB chamfers, sump/planter/lip and riser edge treatments; no further inverted root treatment identified in the source review.

4. <b>Battery:</b> removed both old holder bores and underlying unused pad/pilot features. The integrated saddle and tie tunnel remain.

5. <b>Sensor lead:</b> entry centre lowered from z128 to z64; its 8 mm hole starts at the z60 sump rim. A local skirt relief avoids a cable clash. This interpretation targets the separate sensor entry, not the pump-wire crossover, which remains at z81.

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\internal.png)

Nominal datum: x right, y rear, z up; fascia faces forward. All new radii and route clearances are design choices, not measured component values.

# Geometry evidence and remaining acceptance

![](C:\Users\kevin\Documents\ChatGPT\plant\mechanical\concept_rev13\sensor_entry_section.png)

Export checks: 19 STL meshes, 19 single-solid STEP parts, four-solid assembly; six main-part pair intersections; 61 sampled planter lift positions from 0 to 120 mm. See accompanying JSON records for measured results and hashes.

Checks include closed meshes, consistent winding, two faces per edge, no degenerate faces, positive volumes, STEP validity, matching bounds/volumes, feature sections and positive/negative solid probes. Sampled lift checks do not constitute a continuous swept-volume proof.

Physical fit, slicing, support removal, loads, water tightness, cable bend/retention and powered operation remain unverified. Full mesh self-intersection checking has not been performed. The local CadQuery runtime may exit 1 during shutdown even after assertions pass; distinguish that from any assertion traceback.

The low sensor entry is not a seal or approved fill level. Validate capillary, splash and drain-back behaviour before wet operation. Existing electrical uncertainties and provisional third-control role remain unchanged.

Deliverables: editable build.py, STL/STEP exports, assembly STEP, actual CAD images and sections, AI illustration/prompt, viewer, this review and the separate customer-format kit instructions. R12 is preserved.