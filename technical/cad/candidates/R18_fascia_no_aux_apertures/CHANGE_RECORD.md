# R18 C02 — fascia auxiliary-aperture closure

11 Oct 2026. Status: local fascia-only review candidate. Units: mm. R17 remains the issued project baseline; R18 C01 remains the separate pump-wire candidate.

## Request and outcome

Kevin requests closure of the THREE standalone LED holes and the speaker opening because those devices are no longer used; illumination is integrated into the existing buttons. This is user-reported configuration intent. The final correction specifies removal of the holes, not removal of buttons or their integrated LEDs.

C02 fills the three 5 mm LED bores at x24/48/72, z88, and the one circular 4 mm sound bore at x67, z45. The actual current CAD has a single circular speaker aperture, not a grille. Fill is confined to the existing face plate, y1–4 (3 mm thick); the face is continuous and flush at those positions. The 0.1 mm radial overlap used for robust solid union is within existing surrounding plate material and produces no external thickening.

## Source and preservation

Authority: current user-edited print geometry was checked before choosing the released editable STEP. Both newer local user 3MF files retain the same fascia mesh as the released STL within 0.000007450 mm; their hashes still match the preceding inspection. No fascia source conflict was found. Source: `technical/print/main_parts/step/fascia_charcoal.step`, R13 lineage retained in the current R17 set, SHA-256 `659f2b4dccc36b2a2557f485f04079922de0ce02b9f36d2cac726a22ef2eeda4`. Detailed evidence is in `source_assurance/source_recheck.json`.

Retained: three 12 mm button openings and their positions; 71.4 x 24.6 mm display opening; display bosses/pilots; 7 mm knob opening; four fascia fixing locations; perimeter, face thickness and mating geometry. Unused rear LED collars and speaker seat are preserved in accordance with the holes-only scope; their pockets now terminate against the filled plate. No firmware or electronics change is made.

The tower is not edited. Arduino/relay fit was previously reported successful by Kevin, not independently measured; the fitted mounting geometry is unaffected. Intersections are checked against both R17 and the separate C01 tower as compatibility evidence only. This does not promote or physically accept C01, whose wire-route trial remains open.

## Verification

| Check | Actual result | Evidence |
|---|---|---|
| STEP solid and readback | One valid solid | geometry_checks.json |
| Changed volume | 214.413698608 mm3 added; zero removed | geometry_checks.json; source_assurance/step_independent_checks.json |
| Addition outside four aperture regions | 0 mm3 | Same |
| Four original bore regions through complete plate | Filled; missing volume 0 mm3 | Same |
| Rear geometry from y4 onward | Symmetric difference 0 mm3 | Independent STEP record |
| R17 and C01 tower intersection | 0 mm3 before and after | Both STEP records |
| Exported mesh | Closed, consistently wound, positive volume, one component, two faces per edge, no degenerate triangles | independent_checks.json |
| Retained sections | All 12 button/knob/fixing circular passages and display opening preserved | Independent section records |
| Near-front, middle and near-rear plate sections | Four obsolete holes disappear; retained contours coincide | source_assurance mesh/section record |
| Preview | Before/after actual-STL section visually reviewed | before_after_fascia.png |

Envelope remains nominally 89.2 x 11 x 151.2 mm, including rear bosses. STL is intended as millimetres and contains no unit declaration. No resizing or mesh repair was used.

The CAD generator prints PASS and produces verified files, then returns exit 1 without a traceback during the existing runtime shutdown anomaly; it is not a clean process success. The separate exported-mesh checker exits 0. CadQuery 2.8 / trimesh 5.1 were used. No slicing, printing or physical fit test was performed for C02.

## Proportionate acceptance actions

Owners: Unassigned. Target dates: Not set.

1. Inspect the chosen fascia orientation and layers in the actual slicer: all four former holes show continuous plate material, no unsupported isolated insert or unintended cavity, and rear bosses retain their existing treatment. New blank areas do not change fastening dimensions.
2. After printing, check face flatness and inspect the closed positions for gaps, delamination or sink marks. Check imported dimensions before printing.
3. Dry-fit the existing buttons, display, knob and all fasteners to the printed cover. Confirm the illuminated buttons retain their existing mounting and access; this does not test illumination electrically.
4. Fit the cover to the actual tower without forcing or bending it. Confirm seating, screw access, internal hardware/wire clearance and service removal. Record actual observations; no current physical acceptance is asserted.

A new coupon is not required for this scoped aperture fill because fit-defining dimensions are preserved. C02 is a replacement fascia candidate, not an extra assembly part. Original sources and user 3MFs are unchanged. No commit, push or release promotion is performed.
