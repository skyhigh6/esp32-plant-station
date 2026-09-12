# R8 documentation and release QA

12 September 2026 | R8-A1 | Manufacturing preparation, first article pending.

## Results

- Seven valid single-solid enclosure parts; all 21 pairwise CAD intersections below 0.00001 mm3. Positive overlap control 500 mm3.
- Twenty-two reopened STL meshes: closed, consistent winding, positive volume, one component, every edge incident to two faces and zero degenerate faces. Independent checker exit code 0.
- Exported sections verify 57 x60 installed carrier pattern, retained LCD/button interfaces, 28 x20 left USB window, 10.4 piezo seat, 5.4 LED collars, six round knob bores and two D profiles. Closed roof volume agrees with the independent analytic shape calculation.
- Twenty-two STEP part files re-import as valid single solids; assembly STEP contains seven solids. STEP/STL extents agree within 0.03 mm and volumes within 0.2 percent.
- OpenCascade trailing whitespace in STEP serialization was normalised for Git; the builder repeats this formatting step. STEP re-import checks were repeated on the formatted files. No geometry was repaired or scaled.
- R7 and R8 sump, planter, battery tray and hose clip STL SHA-256 values match exactly. The three changed enclosure parts are tower, fascia and roof.
- Fresh R8 exterior, internal, exploded, fascia rear and knob renders reviewed. Internal green board is an outline-only reference, seated on the front of the standoffs; assembly view shows one illustrative knob.
- All ten PDF pages rendered and visually reviewed. No clipping, page overflow or overlapping content found. Quantity-column wrapping on page 7 was corrected, then pages 7-10 re-rendered and reviewed. Other pages were unchanged. Automated word bounds, page count, footer and key-dimension checks pass.
- The guide includes the actual 22-file breakdown, provisional USB measurements, knob coupon map, adhesive process, fastener quantities/engagement, print orientation, consumables, assembly route and blank first-article acceptance record.

## Runtime exception

The local CAD builder prints PASS after completing assertions, exports and rendering, then returns exit code 1. A minimal process containing only CadQuery import reproduces success output followed by exit 1. A minimal VTK import exits 0. The independent STL checker exits 0. The STEP re-import checker completes assertions and writes its PASS report, then exhibits the same CadQuery exit behaviour. This isolates the issue to the local CadQuery import/runtime path; the exact native teardown cause remains unknown. It is not silently treated as a clean command exit.

## Evidence files

- `mechanical/concept_rev8/verification.json`
- `mechanical/concept_rev8/independent_mesh_check.json` (per-STL SHA-256)
- `mechanical/concept_rev8/step_check.json`
- `mechanical/concept_rev8/knob_options.json`
- `scripts/check_guide_r8.py`; local raster QA outputs under ignored `output/pdf/qa/r8/`
- `scripts/package_r8_illustrated.py` checks archive CRC, STL hashes, exact STL count and every archived file against source.

## Open acceptance

Actual USB socket offsets, plug insertion/overmould clearances, pot shaft/bushing and piezo body height/type are unknown. Screw family/pilot fit, print material/settings, slicer layers, strength, glue compatibility, leak tests, complete self-intersection analysis and powered commissioning are not verified. Knob fit requires physical trials. The compact USB window may need moving/enlarging before the full tower print. R8 changes no firmware and does not approve any electrical pin map or charging arrangement.

Current project control explicitly specifies three buttons, superseding the earlier two-button design. The R8 guide preserves that recorded scope.
