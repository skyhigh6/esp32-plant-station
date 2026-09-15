# R14 acceptance and open-action record

Document ID: PLANT-TS-UNO-MOUNTS
15 Sep 2026 | Revision R14 | Status: issued for prototype review; physical acceptance open.

## Recorded digital checks

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
