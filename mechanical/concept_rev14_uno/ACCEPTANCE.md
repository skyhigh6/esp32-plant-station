# R14 acceptance and open-action record

Document ID: PLANT-TS-UNO-MOUNTS
20 Sep 2026 | Geometry R14 | Documentation issue R14-D2 | Status: issued for prototype review; physical acceptance open.

## Recorded digital checks

CAD/STEP and preview results below are retained evidence from 15 September 2026; the CAD builder was not rerun for R14-D2. Physical checks remain open.

| Check | Result | Evidence |
|---|---|---|
| Two exported closed positive-volume single-component meshes | Pass | verification.json; independent_mesh_check.json |
| Two valid single-solid STEP re-imports | Pass | verification.json |
| Board envelope versus body | 0 mm3 interference | verification.json |
| Geometry change outside mount regions | 0 mm3 added / removed | verification.json |
| Preview and section review | Completed | preview.png; mount_section.png |
| Build process exit | 1 after PASS; shutdown cause unknown | REVISION_CHECKS.md |

## Physical test and action register

All owners: Unassigned. All target dates: Not set. Do not infer completion from the digital results above.

| ID | Action / acceptance criterion | Required evidence | Status |
|---|---|---|---|
| R14-A01 | Identify actual Uno; all four coupon holes register without force or board distortion | Board markings, coupon photograph, hole measurements | Open |
| R14-A02 | Establish M3 screw/tap method; no cracked boss, stripped thread, contact with components or bottoming | Screw specification, engagement measurement, trial result | Open |
| R14-A03 | Confirm usable USB plug insertion/removal and cable route with fascia fitted; no forced bends or connector side load | Plug dimensions, photographs and clearance measurements | Open |
| R14-A04 | Verify board, headers, wiring and screw-head clearance; board rests on all four faces without bowing | Installed inspection and measured minimum gaps | Open |
| R14-A05 | Record slicer settings and inspect boss/root layers; printed supports intact | Slicer file, material/process record and print inspection | Open |
| R14-A06 | Repeat applicable enclosure leak/flow checks before wet operation; establish fill limit below unsealed entries | Controlled physical test record and approved operating limit | Open |
| R14-A07 | Diagnose CAD runtime shutdown exit 1 before claiming reproducible clean builds | Clean process log or isolated dependency defect evidence | Open |

## Test record

Test date: Not performed. Operator: Not assigned. Printer/material: Unknown. Actual board revision: Unknown. Fastener specification: Unknown. Photos/measurements: Not supplied. Physical disposition: Open.

Geometry is available for prototype manufacture preparation. This record does not release the assembly for unattended or powered wet operation.

## First-article evidence worksheet

Complete one copy per actual board/print configuration. Blank fields are unknown, not passes.

| Field | Recorded value |
|---|---|
| Test date / operator / evidence location | Not recorded |
| Board manufacturer / model / revision | Not recorded |
| Source STL SHA-256 / documentation issue | Not recorded / R14-D2 |
| Printer / slicer version / saved job | Not recorded |
| Material / nozzle / layer height / orientation / supports | Not recorded |
| Coupon registration result / photograph | Not recorded |
| Screw type / length / washer / thread preparation | Not recorded |
| Measured engagement / remaining blind-depth margin | Not recorded |
| Minimum component / screw-head / wiring clearances | Not recorded |
| USB plug identity / insertion and removal / cable route | Not recorded |
| Leak/flow procedure / result / established fill limit | Not recorded |
| Action IDs closed / evidence references / residual defects | None closed |
| Disposition / reviewer / date | Open / not assigned / not recorded |

R14-D2 verification, 20 September 2026: independent STL checker rerun, PASS with exit 0. Results match the retained mesh report, including both source-file hashes. CAD/STEP was not rebuilt; no physical tests were performed.
