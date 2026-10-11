# R18 combined geometry — 11 October 2026

The R18 tower and fascia are byte-for-byte promotions of the reviewed C01 open
pump-wire route and C02 fascia candidates. The retained lid, planter and knob
options are unchanged. `technical/print/manifest.json` identifies the four current
main parts, retained options and four frozen predecessor exports.

## Editable authority

- `candidates/R18_open_pump_route/build.py`: two named route cuts on the frozen
  R17 STEP. Opens the vertical route at the front and the crossover at the top.
  The crossover floor is at z77 mm, 17 mm above the sump rim; the separate water
  tube, dry partition, sump floor, Uno/relay mounts and lid fixing are retained.
- `candidates/R18_fascia_no_aux_apertures/build.py`: fills three standalone LED
  bores and one speaker bore through the 3 mm plate. Rear blind collars/seat
  remain. LCD, three illuminated buttons, knob and fixing passages are retained.
- `parameters.json` and `build.py`: inherited R17 power-port authority and
  predecessor rebuild. Their R17 label is intentional, not the current tower.
- `build_r18.py`: rebuilds both changes into `.build/r18_regeneration`, never
  overwrites the issued exports, and records actual process exit codes.

## Rebuild and checks

```powershell
python technical/cad/build_r18.py
python technical/cad/check_exports.py
python verification/cad/r18_combined_check.py
```

The scratch rebuild reproduced all three candidate STL hashes and its STEP
readbacks and local geometric checks completed. The CAD runtime then terminated
abnormally: route exit `3221226356` (`0xC0000374`); fascia exit recorded in
`verification/cad/r18_regeneration_process.json`. The wrapper exits 1 to preserve
this limitation. This is not a clean CAD process success. Independent exported
mesh and port checks are recorded separately; they do not establish physical fit.

The actual terminated cable dimensions, bend radius and retention remain
unmeasured. Lay the lead into the route during an unpowered dry assembly, check
cover/planter clearance, edges and service access, then record results on the R18
test sheets. The user's report of successful Uno and relay fit applies to the
preceding printed tower. No R18 print or machine toolpath is accepted here.
