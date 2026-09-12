# Plant Station R8

12 September 2026. Units: mm. Status: manufacturing preparation; physical first article pending.

## Changes from R7

- Carrier rotated 90 degrees anticlockwise viewed from the fascia. Both USB connectors point to the left wall. Reference 67 x 64 PCB becomes 64 x 67 installed. Reference 60 x 57 mounting pattern becomes 57 horizontal x 60 vertical. Centre remains (x=48, z=108.5).
- Carrier mounting coordinates x,z: (19.5,78.5), (76.5,78.5), (19.5,138.5), (76.5,138.5). Seating plane y=76; component stack projects towards the front.
- Roof closed, except its four fixing holes. Left-wall window 28 x 20, from y=49 to77 and z=98.5 to118.5. **Provisional: socket offsets and plug dimensions were not supplied. Measure before printing the tower.** Edit USB_YZ / USB_WH and rerun the builder/checker when actual dimensions are available.
- Upper fascia bosses joined to side walls by 10 mm wide, 9 mm deep webs with 45-degree lower edges. Existing front screw centres retained: x=9/87, z=10/148. Bottom bosses also have solid webs. Upper boss coupon reproduces the real left region.
- Piezo: user-specified 10 mm round body; provisional 10.4 ID x3 deep glue seat at x=67,z=45, with 4 mm sound outlet. Body height/type unknown. LED holes remain 5 nominal, with 5.4 ID x2 deep rear glue collars.
- Eight knob bore alternatives, 20 OD x14 high, 11 blind bore depth: round 5.0/5.2/6.0/6.2/6.35/6.55 and D 6.0/6.2. D-flat offsets 1.5/1.6 from axis (circle-to-flat 4.5/4.7). No splines or grub screws. Print closed face down, bore upwards.
- LCD mounting geometry, three 12 mm button holes, 7 mm pot bushing hole and wet module retained. The current project control record explicitly updates to three buttons, superseding earlier two-button notes. Firmware unchanged.

## Files

`stl/`: 22 files, mm. Seven assembly components; eight alternative knobs; six coupons (button, LCD, carrier, knob, piezo/LED, upper boss); one optional USB marking blank.

`step/`: corresponding editable BRep solids. `assembly.step` holds the seven enclosure parts; alternative knobs/coupons are separate. `pump_envelope_reference.step` is a provisional reference, not a printable pump.

`build.py`: parametric source, CadQuery 2.8. `check_exports.py`: independent mesh/section checks. `verification.json`, `independent_mesh_check.json`, `step_check.json`: actual verification evidence. `knob_options.json`: variant contract. PNG illustrations are current R8 CAD.

`references/` retains the R7 source drawings and attribution. Their dimensions are references, not confirmation that the actual purchased components match.

## Production preparation

Read [illustrated guide](../../docs/ASSEMBLY_GUIDE_R8.md), [PDF](../../output/pdf/Plant_Station_R8_Illustrated_Assembly_Guide.pdf), and [BOM](../../docs/BOM_R8.md). Print fit coupons first; choose actual screw family, test retention and select the knob bore before the full print. A 3 mm plastic thread-forming screw in a 2.8 mm pilot is a trial selection and may require a different pilot for the actual screw/material. No heat-set inserts are modelled.

USB marking blank: 34 x26 x1.2, flat, temporary tape attachment outside the window with 3 mm overlap. It is not a snap-in part or a certified seal. Mark/cut a measured aperture as appropriate; the base window itself may need moving/enlarging to suit the two plugs.

Assembly STLs retain common coordinates. Translate/orient each part on the bed; do not scale. Suggested trial process: 0.4 nozzle, 0.2 layers, four perimeters, five top/bottom layers. Tower base down requires slicer inspection/local supports at carrier bosses and USB roof. Upper webs remove the weak near-tangent attachment; they do not prove a support-free print. No slicing was performed.

Acceptance: both real USB cables fully engage; all mounting patterns fit without strain; screws retain after service cycle; knob grips without binding; glue retains LEDs and piezo while leaving optical/acoustic faces clear; wet module passes leak/drain-back tests before electronics are installed. Full route card and electrical hold points are in the guide. No production, strength, leak-tightness, ingress-protection or electrical commissioning claim is made.

## Rebuild

```powershell
python mechanical/concept_rev8/build.py
python mechanical/concept_rev8/check_exports.py
python mechanical/concept_rev8/check_step.py
python scripts/build_guide_r8.py
python scripts/package_r8_illustrated.py
```

Dependencies: CadQuery 2.8, trimesh, NumPy, VTK, ReportLab, PyMuPDF for document QA. Existing local `.tools/cad-runtime` is used when present and is not distributed. The local CadQuery import alone prints success but exits 1 at process shutdown; VTK import and independent STL checks exit 0. Do not treat exit 1 alone as verification: inspect the report and run independent checks. Actual modelling/assertion errors remain failures.
