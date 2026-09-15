# R14 — Arduino Uno tower mounts

15 September 2026. Units: mm. Derived from R13; original exports retained.

## Change
Four original carrier bosses replaced with the asymmetric Arduino Uno R3 mounting pattern. Components face the front fascia; USB faces left. The board lower-left datum is x13.71/z72; underside seats at y76. Rear wall is y94: 18 mm clearance. Bosses are diameter 6 with R0.6 roots, 0.3 tip chamfers and diameter 2.8 blind pilots, 11 mm deep from the seating face. Pilot fit is provisional for M3 screws; test/tap as appropriate rather than forcing a screw into the complete tower.

| Mount | x | z |
|---|---:|---:|
| 1 | 79.75 | 107.56 |
| 2 | 79.75 | 79.62 |
| 3 | 28.95 | 122.80 |
| 4 | 27.68 | 74.54 |

Source: Arduino UNO-TH_Rev3e.brd, board/plain/hole elements, downloaded from the official Arduino Uno R3 CAD resources on 15 September 2026. Native hole centres: (66.04,35.56), (66.04,7.62), (15.24,50.8), (13.97,2.54); holes diameter 3.2. CAD board envelope: 68.58 x 53.34. Source board and its CC BY-SA 4.0 licence retained in references/.
https://docs.arduino.cc/hardware/uno-rev3

## Files
- stl/tower_sump_body_uno.stl: replacement integrated tower/sump.
- step/tower_sump_body_uno.step: editable solid export.
- stl/uno_mount_fit_coupon.stl: full board-size hole gauge with one pilot boss for screw-fit testing. Place against board underside with coupon boss facing away.
- build.py: dimensioned CadQuery source, standalone within this workspace.
- verification.json: actual exported geometry checks.
- preview.png and mount_section.png: model and exported-mesh mount sections.

Use R13 fascia, roof and planter. Only the board mount geometry changes. USB aperture is retained: actual Uno connector and plug access, headers, wiring, screw-head clearance and component envelopes remain unverified. Do not assume the old carrier port cutout provides direct Uno USB access. The mounting coupon establishes hole registration and pilot fit before a full tower print; it does not establish those other clearances.

Rebuild: python mechanical/concept_rev14_uno/build.py

Checks assert CAD and imported STEP validity, one solid, watertight positive-volume single-component meshes, mounting pilot openings and blind ends, board-envelope clearance, and no changed solid volume outside the old/new mount regions. No slicing, physical fit, strength or leak tests have been performed.

Validation result: all assertions passed and both previews were visually reviewed. No volume changed outside the mount regions. The process printed PASS then returned exit code 1 without a traceback during runtime shutdown, consistent with the R13 runtime behaviour; this is not recorded as a clean process exit. Export files and the verification record were produced before shutdown.

## Controlled revision documents

- [Change note and verification disposition](REVISION_CHECKS.md)
- [Assembly supplement and configuration list](ASSEMBLY.md)
- [Acceptance and open actions](ACCEPTANCE.md)
- [Independent mesh checks](independent_mesh_check.json)
- [Release manifest](release_manifest.json)

Complete mechanical review package: [Plant_Station_R14_Uno_Review.zip](../../Plant_Station_R14_Uno_Review.zip). Includes R14 files and the retained R13 model set and kit guide; the R14 supplement takes precedence for board mounting.

Independent final-STL checker: PASS, exit 0 on 15 Sep 2026. Both meshes have two faces per edge, no degenerate triangles, consistent winding and one connected component. Section checks confirmed four 2.8 mm pilots, four 6 mm bosses and four 3.2 mm coupon holes within 0.025 mm radial tolerance.
