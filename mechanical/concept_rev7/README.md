# Plant Station R7 - corrected carrier, LCD and USB access

11 September 2026. Millimetres. R7 supersedes R6 for the tower, fascia and top cover. R6 sump, planter, holder tray, hose clip and button coupon are retained unchanged.

## Corrected dimensions and evidence

| Interface | R6 | R7 | Basis |
|---|---|---|---|
| SunFounder mounting centres | 60 x 55 | **60 x 57** | Manufacturer dimensioned drawing on the user-linked page |
| Carrier board outline | Assumed 76 x 67 envelope | **67 x 64** PCB outline | Same drawing; front stack allowance remains assumed |
| LCD mounting centres | 73 x 30 | **75 x 31** | Main annotated LCD drawing in user image |
| LCD PCB outline | 80 x 36 assumed | **80 x 36** reference | Same LCD image |
| LCD fixing holes | 2.4 | **3.0 nominal** | Image; select M2.5 or smaller through-fixings and verify actual hole |
| LCD aperture | 70 x 25 | **71.4 x 24.6** | 71 x 24.2 bezel plus 0.4 total clearance (0.2 per side) |
| LCD visible area | Not used | 64.4 x 14.5 reference only | The optical visible area is not the bezel cutout |
| USB | Incorrect rear-facing opening | **72 x 46 top access opening** | Both Micro USB connectors must face the same side; installation rotates that edge upwards |

The new references supersede earlier user-measured 60 x 55 and 73 x 30 values for this revision. This is not proof the physical units match those references; use the fit coupons before printing the enclosure. The lower thumbnails in the LCD screenshot depict other modules and are not used.

Source: [SunFounder ESP32 Camera Extension](https://docs.sunfounder.com/projects/esp-cam-kit/en/latest/component_esp32_extension.html), with [dimensioned board drawing](https://docs.sunfounder.com/projects/esp-cam-kit/en/latest/_images/esp32_camera_extension_size.png). Reference copies and source notes are in `references/`. The screenshot is the user-provided LCD reference, not an identified manufacturer's production drawing.

## Installed orientation and coordinates

Datum: x right, y rear, z up, with tower front-left-bottom at zero. Board component side faces the removable fascia. Rotate the carrier 180 degrees in its own plane relative to the SunFounder dimensioned drawing so the charging USB and installed ESP32 programming USB face upwards. They are separate ports, not interchangeable.

- Carrier PCB outline: x=14.5 to 81.5, z=76.5 to 140.5. Standoff face y=76. Mount centres: (18,80), (78,80), (18,137), (78,137) in x,z. Upper pair moved up 2 mm from R6.
- Carrier standoffs: OD 8, blind pilot 2.8, face-to-rear-wall separation 18. Mount hole diameter and underside solder clearance are not specified by the manufacturer diagram; select screws from the actual board, not a drawing-scale estimate.
- Conservative front-facing carrier/module stack: y=44.4 to 76 (31.6 total, assumed). This leaves 10.8 to the assumed LCD rear envelope. Actual header/module/terminal heights require measurement.
- LCD PCB centred x=48, z=112.5; outline x=8 to 88, z=94.5 to 130.5. Hole centres: (10.5,97), (85.5,97), (10.5,128), (85.5,128).
- LCD aperture: x=12.3 to 83.7, z=100.2 to 124.8. Pads OD 6, bores 3, seating face y=12; 8 mm separation from fascia rear remains a provisional depth. Head diameter limit 5.5 mm; no oversized washers at aperture corners.
- USB cover opening: x=12 to 84, y=40 to 86, through z=158 to 161. The former rear-wall opening is closed.

## What the USB opening does and does not establish

The source gives port direction but no connector-centre offsets, board stack height, socket projection or cable overmould dimensions. R7 therefore uses a broad shared top access well rather than fabricated precision port holes. The cover is removable for inspection and insertion. A 67 x 38 mm vertical passage above the carrier clears printed parts; the lower central entry region also clears the standoffs. Actual plug fit and finger access remain physical checks.

The top opening is intentionally large and open. It has no splash seal, strain relief or close-fitting blanking plate. Keep it dry. A smaller cable insert needs the measured charge/programming connector and cable positions. Do not route water tubing through this opening. It does not authorise simultaneous USB/battery operation.

## Print and assemble

1. Print `carrier_fit_coupon.stl` (60 x 57 centres), `lcd_fit_coupon.stl` (75 x 31 centres, 71.4 x 24.6 aperture), and the retained button coupon. Check against the actual components without power. Never scale the entire model to correct one fit.
2. Replace the **tower, fascia and top cover** as one R7 set. Retain R6 wet parts, holder tray and hose clip. Three 12 mm button holes are unchanged.
3. Fit the carrier with both USB ports up. Confirm module orientation against the SunFounder instructions before insertion. Trial-insert each actual USB cable separately through the top well, then check cover removal and harness access.
4. Trial-fit the LCD through the aperture. The bezel must clear without loading the glass or bending the PCB. Check the real bezel-to-PCB depth and backpack envelope before tightening the provisional fasteners.
5. Complete the [R7 illustrated guide](../../output/pdf/Plant_Station_R7_Illustrated_Assembly_Guide.pdf) and its acceptance worksheet. Electrical pin assignment, pump voltage/current and leak tests remain open.

## Delivered and checked

Seven assembly STLs/STEPs plus three fit coupons; assembly STEP; CAD previews; editable source; independent mesh checks. STL units are mm; assembly parts retain common coordinates.

All seven assembly CAD solids valid and single-body; 21 assembly-pair intersections zero within 0.00001 mm3. Direct CAD checks cover corrected mounts, aperture, USB passage and retained pump/buttons. Independent exported-mesh checks cover closure, winding, positive volume, single component, edge incidence and degenerate faces; sections check carrier/LCD/button bores and centres, LCD aperture and USB opening. See JSON evidence.

CAD builder prints PASS then exits with code 1 during local runtime shutdown, as in R6. Independent mesh checking exits successfully. No slicing, physical assembly, structural/watertightness test, full self-intersection analysis, upload or powered operation is claimed.
