# R18 C02 fascia independent assurance

11 October 2026. Read-only comparison against released R17 fascia. All source STL/STEP and user 3MF hashes were rechecked and remain unchanged. Both user fascia meshes retain the prior proven equality with the canonical STL; no source conflict was found.

## Verified result

- Candidate STL is watertight, winding-consistent, one connected component, positive volume and free from tested area-degenerate faces. Bounding envelope remains unchanged.
- Candidate STEP reopens as one valid solid. Added volume is 214.413698608 mm³; removed volume is zero. Added material lies entirely in four small aperture regions within fascia plate y1–4 mm, with none in front of or behind that plate.
- The three nominal Ø5 auxiliary LED holes at x24/48/72,z88 and nominal Ø4 speaker hole at x67,z45 are filled throughout the plate.
- The three Ø12 button passages, Ø7 knob passage, four display-fixing holes, four fascia-fixing holes and LCD opening remain clear. Digital difference checks preserve all geometry outside the four patches, including rear collars/seats and tower interfaces.
- Complete rear geometry at y>=4 mm has zero symmetric difference from the baseline. Intersection volume remains zero against both R17 tower and the separate R18 C01 tower candidate.
- Exported STL sections at y1.01,2.5,3.99 mm each change from 18 to 14 loops: exactly the four obsolete openings disappear. Remaining section curves coincide within 1.42e-14 mm sampled point-to-polyline distance. The nominal Ø12 holes measure approximately 11.9963 × 12 mm in the tessellated sections, identical to baseline.
- `fascia_section_comparison.png` was visually inspected and shows the intended four closures with controls and fixings retained.

## Process and limits

Final mesh/section checker and preview generation exited 0. The STEP checker wrote and printed complete passing results, then exited 1 without a traceback during the existing CAD-runtime shutdown issue; this is not a clean process exit. The first mesh-check attempt encountered an unavailable Shapely import; its final version uses the existing NumPy runtime and exits 0, with no dependency installed.

No slicing, printing, publishing, hardware operation or modification of original files was performed. This is digital geometry assurance; physical print quality and fitted component acceptance are not established. R18 C02 fascia remains separate from R18 C01 pump-route candidate.
