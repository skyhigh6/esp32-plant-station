# R9 verification record

13 September 2026. Changed STL hashes: tower_sage.stl and upper_boss_print_coupon.stl. Other 20 STLs are byte-identical to R8.

- 22 meshes independently checked: closed, consistent winding, positive volume, one component, two faces per edge and no degenerate faces. Dimensional section checks pass; checker exit 0.
- 22 STEP parts reopened as valid single solids and seven-solid assembly; dimensions and volume agree with STL. CAD assertions and STEP assertions report PASS then the known CadQuery shutdown exits 1.
- 21 assembly intersection checks report zero. Upper gap closure volume probes pass on both sides. Existing component envelopes, mounting holes and tool access probes pass.
- Internal CAD render and isolated tower in interactive viewer visually reviewed. Viewer loads seven parts; R9 tower remains selected for review.
- No slicing, physical fit, strength or leak testing. Functional interface edges are excluded from general rounding.
