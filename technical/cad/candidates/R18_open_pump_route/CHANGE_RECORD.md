# R18 C01 — open pump-wire route candidate

11 Oct 2026. Status: local review candidate; R17 remains the issued baseline. Units: mm. Scope: pump-wire route only.

## Outcome and source

R17's wire riser and crossing are opened so an already terminated lead can be laid in. No terminal must pass through the former enclosed 8 mm bore. The optional route trial is a test artefact, not a new assembly part. No electronics or additional hardware is introduced.

GitHub and local main both resolve to `16e4ad7651115d4fda5e9024cfb1815945fa96a0` after fetch. Frozen R17 STEP SHA-256: `e74c073986564771eb660b70b004969c20f2cf9501af87a1c6b3494666879352`. The newer user `all plates r17.3mf` has the same tower mesh connectivity as the released STL, with maximum vertex discrepancy 0.000005787 mm. The newer mixed fascia project contains no tower. Original files and issued exports are preserved.

**Reported:** Kevin printed the newest tower and says the Arduino and relay both fit perfectly. The fitted pump-wire terminations cannot pass the existing route. This is a reported successful board-fit observation, not independently measured fit or operational acceptance; see `reported_first_article.json`.

## Decision

| Option | Trade-off | Disposition |
|---|---|---|
| Enlarge enclosed bore | Still depends on terminal dimensions and inaccessible internal ceilings | Rejected for this candidate |
| Open front riser and upward crossing | Lead can be laid in; eliminates wire-tunnel roofs; leaves route less enclosed | Selected candidate |
| Separate removable channel cover | Can capture cable but adds assembly parts and fixings | Outside authorised scope |

The vertical front cut spans x106.5–114, y82–96, z52–129. Nominal front mouth width is 7.5 mm, based on inherited route geometry, not a measured cable. The open-top crossing spans x89–114, y88–96, z77–159: 8 mm nominal fore/aft width. Clear probe corridors cover a 4 mm-wide internal route and a 5 mm-wide front approach (x108–113/y70–94), including z53–60 and z61–128, connecting the wire channel to the open top. Actual cable bundle and minimum bend radius remain unknown.

The crossing retains its z77 floor, 17 mm above the z60 sump rim. The existing water-tube column at x123 is retained. The below-rim wet/dry partition up to x106.5, sump floor, board mounting region, and rear-right lid fixing have zero removed solid volume. The nominal rear band y96–100 is preserved wherever the rounded R17 body contained material; this is not a uniform 4 mm measured wall-thickness claim. CAD continuity is not strength or leak testing. Local wet-side riser material is removed between z52 and z60, outside the protected divider; there is no new below-rim dry-entry opening.

## Assembly and service sequence

1. With power isolated, remove lid and planter to expose the route; remove fascia if needed for access to the dry tower.
2. Keep the fitted terminations attached to the lead. Place the pump-side end and the dry-side termination in their respective spaces, then lay the intermediate wire into the open front channel and lower it into the upward-open crossing. Do not force a termination through a bore.
3. Leave service slack and a smooth free bend at the change of direction. Inspect/deburr the exposed printed edges before contact with wire insulation. No qualified cable bend radius or positive strain-relief mechanism is claimed.
4. Check that the existing lid, planter, tube, relay terminals and other wiring clear the lead. Refit the retained parts while observing for pinching or lifting out of the channel. Existing parts are retained; their retention of this lead must be checked physically.
5. Confirm removal/reinstallation is possible without disturbing accepted board mounts or removing the terminations.

## Verification and manufacturing implications

`geometry_checks.json` records two valid CAD solids, valid STEP re-imports, protected-region checks and clear access probes. `independent_checks.json` records closed, wound, positive-volume single-component meshes with two faces per edge and no degenerate triangles. All eight Uno/relay pilot sections retain their centres and 2.8 mm diameters. Body envelope remains 207 x 100 x 158.

In the upright build orientation, downward-facing route surface area selected by the declared 30-degree geometry threshold falls from 226.97 mm2 to 0 mm2. This establishes removal of the selected tunnel ceilings; the entire tower is not support-free. A Bambu Studio 2.5.0.66 comparison using copied versions of the same upright user PLA project generated both slices with exit 0. Feature-tagged support deposition fell from 19,218 to 18,809 mm3 (2.13%, approximately 0.52 g at the stored density). This is commanded extrusion, not observed consumption. Both runs emitted missing-system-preset warnings, ZFiller error messages and a bed-temperature/filament warning; generated timing metadata also contains an implausible candidate first-layer time. These outputs are comparison evidence only and are not issued printer files. The sampled z84.7 and z87.7 layers show support/interface in the old route and none in the candidate opening. A support-motion midpoint metric inside the declared cutters changes from 111.47 mm of filament over 180 layers to zero; this is a location metric, not a rigorous boundary-clipped material volume. Adjacent tube and rear-wall toolpaths remain visible. See source_assurance/route_layer_comparison.png and slice_comparison.json; the profile and complete layers require review before manufacture. The existing board bosses and other features still need layer/support review. Later user settings specify PLA, while the published project used ABS; the actual printed material is unknown.

The CAD process prints PASS then exits 1 without a returned traceback during shutdown. The independent mesh checker exits 0. See `process_record.json`; no clean CAD process exit is asserted. No full mesh self-intersection test, physical print, strength, leak or electrical test was performed for C01.

## Open acceptance actions

Owners: Unassigned. Target dates: Not set.

| ID | Action | Closure evidence |
|---|---|---|
| C01-A01 | Check actual bundle fits by laying in, without terminal removal or forcing | Actual cable dimensions and route-trial observation |
| C01-A02 | Establish smooth bends, edge condition and strain relief; wire stays seated with cover/planter fitted | Dry assembly photographs and service/removal trial |
| C01-A03 | Review upright layers, remaining supports and rear-wall stiffness for actual material/process | Slicer layer review and print inspection |
| C01-A04 | Check retained tube, lid, planter and all fitted hardware/wiring together | Dry fitted-assembly inspection |
| C01-A05 | Confirm physical leak and powered-operation acceptance separately before use | Relevant existing controlled acceptance records |

C01 is ready for geometry review and an optional route trial. It is not promoted into the R17 release or published to GitHub.
