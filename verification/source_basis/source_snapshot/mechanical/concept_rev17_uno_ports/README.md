# R17 left USB-C and DC power panel — prototype

28 September 2026. Units: mm. Derived from the R16 Uno/relay tower STEP; earlier files are preserved.

**Current prototype instructions:** [R17 enhanced document set, issue D02](../../output/pdf/Plant_Controlled_Set_R17/START_HERE.html), incorporating R15/R16 mechanical changes and the current Uno UI v6 interface. It replaces the R14 instructions for this prototype build; historical R14 issue records remain preserved. The new documents do not close the physical gates below.

## Requested change and authority

Replace the left rectangular USB cable pass-through with a cut and fixing holes for the photographed solderable USB-C module. Add an adjacent **Ø10 mm** hole for a panel extension to the Uno barrel-power input. The user explicitly authorised best guesses and fixing holes matching the other PCBs. This authorises provisional mechanical geometry; it does not establish actual component fit.

The R17 body carries forward the R16 relay mounts and R15 Uno bosses, thicker flush-head lid interface and pump clearance. Retain the R16 lid and R13 fascia/planter; they are not re-exported here. The change is confined to the left wall.

## Dimension contract

Datum: x right, y towards rear, z up. Left outside wall x=0; inside wall x=6. Connectors mount from the outside. Their cables/wiring enter the dry tower.

| Feature | Nominal dimension / position | Evidence |
| --- | --- | --- |
| Old USB opening | 28 × 20, lower-left y49/z98.5 | R16 inherited geometry; closed, including chamfers |
| USB centre | y63 / z108.5 | Engineering placement; retains old opening centre |
| USB rounded rectangular cut | **9.8 × 4.2**, R1.2 corners | Authorised estimate; no measured shell size |
| USB fixing centres | y55.4 and y70.6 / z108.5; **15.2** pitch | Authorised estimate; actual flange pitch unknown |
| USB printed fixing pilots | **Ø2.8 through** | Same nominal diameter as Uno/relay pilots; wall is 6 thick |
| Power-jack extension centre | y35 / z108.5 | Engineering placement; 28 from USB centre, towards front |
| Power-jack cut | **Ø10.0 through**, no added allowance | User-specified; thread and nut unmeasured |
| USB flange width / PCB width / depth | 20.1 / 9.1 / 14.5 | Supplied image dimension labels; actual component unmeasured |
| USB flange height / thickness / component fixing holes | 7.0 / 1.5 / Ø3.1 | Review-only guesses; not claimed as measured |
| DC external nut / internal length proxies | Ø20 / 20 | Review-only clearance guesses; actual unit unknown |

The Ø2.8 USB pilots pass through the **6 mm side wall**. They do not have the existing board mounts' 11 mm blind depth or reinforced cones. Select screw length for the actual flange and this wall; long screws will project into the tower. Approximately 1.3 mm minimum nominal material remains between each USB pilot and the aperture. Check screw insertion and local wall integrity on the coupon.

The USB reference flange has 12.95 mm nominal clearance to the Ø10 cut. Its nearest edge has 7.95 mm clearance to the guessed Ø20 nut envelope. Confirm the actual nut/flange and plug bodies together. Barrel jack grip range must accommodate 6 mm wall; no recess is assumed until its dimensions are known.

## Files and print order

- **Print first:** `stl/power_ports_fit_coupon_r17.stl` — 6 mm thick × 60 × 24, same cuts and pitch as the tower. Matching STEP in `step/`.
- **Provisional tower:** `stl/tower_sump_body_uno_ports_r17.stl`. Matching STEP in `step/`. Do not use for the full print until the port coupon and earlier physical trials pass.
- `parameters.json` — dimensions, image references, guesses and authority. Change guesses here after measuring the component, then rebuild both exports.
- `reference/usb_c_supplied_dimension_image.png`, `reference/source_record.json` — preserved original user image, labelled dimensions and SHA-256; image text is evidence, not task authority.
- `build.py`, `check_exports.py`, `render_review.py` — editable generation, independent exported-mesh checks and actual-STL previews.
- `verification.json`, `independent_mesh_check.json` — recorded digital evidence. Consult process output as well: the existing CAD runtime has a known shutdown exit-code anomaly; a printed PASS alone is not a clean process exit.
- `r17_left_panel_detail.png`, `r17_assembled_review.png` — actual exported geometry; no fitted-connector claim.

The detail preview clips away material at x>6.01 to expose the left-wall holes. The assembled preview shows the complete geometry. Position the coupon's broad 60 × 24 face on the print bed, with its 6 mm thickness and bore axes vertical; inspect the chosen slicer orientation before printing.

### Recorded digital result

Both exported STLs passed the independent checker with exit 0: single connected components, closed two-face edge topology, consistent winding, positive volume and zero degenerate faces. Six sections at x0.5/x3/x5.5 across the tower and coupon verify the USB rounded profile, both pilots and the Ø10 bore. Measured mesh-section USB size was 9.800 × 4.200 mm; centre-section bore was 9.998 mm due to tessellation. Both STEP exports reopened as single valid solids; no added or removed volume was found outside the named left-wall region.

The CAD builder printed PASS but exited **1** during the existing runtime shutdown anomaly. This is not a clean process exit. The independent exported-mesh checker and preview renderer both exited **0**. Slicing and physical fit have not been performed.

## Acceptance criteria

1. Fit the actual USB connector to the coupon: shell enters without forcing; flange seats flat; both holes align; actual USB plug fully engages.
2. Insert the chosen screws: no splitting, no loose retention, no unacceptable protrusion. Verify solder pads and wire strain relief remain accessible.
3. Fit the actual barrel-jack extension: thread passes Ø10; shoulder/nut seat; grip range spans 6 mm; cable and mating plug clear USB hardware.
4. Measure and revise any failed dimensions in `parameters.json`. Rebuild and rerun export checks before the tower print.
5. Complete the separate R15/R16 board, screw, lid, relay and pump trials, then review slicing and assembled dry fit. Physical strength, leaks and electrical commissioning remain open.

The two openings provide mechanical access for alternative USB and barrel-input supply connections. No supply voltage, polarity, simultaneous-source behaviour or USB-C negotiation circuit is approved by these CAD files. The image's 6-pin/5 A text is supplier information, not a verified electrical rating.

## Rebuild

```powershell
python mechanical/concept_rev17_uno_ports/build.py
python mechanical/concept_rev17_uno_ports/check_exports.py
python mechanical/concept_rev17_uno_ports/render_review.py
```

Scope is this local R17 prototype. This does not supersede the issued R14 baseline or close any physical acceptance gate.
