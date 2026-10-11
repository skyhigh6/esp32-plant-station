# R18 C02 fascia-only candidate

Three standalone LED apertures and the dedicated speaker aperture are closed. All three illuminated-button mounting openings remain.

- [Printable STL](exports/fascia_no_aux_apertures_r18_c02.stl).
- [Editable STEP](exports/fascia_no_aux_apertures_r18_c02.step).
- [Before/after view](before_after_fascia.png).
- [Change record and physical checks](CHANGE_RECORD.md).
- [CAD evidence](geometry_checks.json), [independent mesh evidence](independent_checks.json) and [source assurance](source_assurance/source_recheck.json).
- `build.py`: dimensioned, frozen-source modification; `check_and_render.py`: exported-mesh inspection and preview.

From the project root, with the existing CadQuery/trimesh/NumPy/matplotlib runtime:

```powershell
python technical/cad/candidates/R18_fascia_no_aux_apertures/build.py
python technical/cad/candidates/R18_fascia_no_aux_apertures/check_and_render.py
```

R17 remains issued. C02 is local and separate from C01 pump-wire routing. No new print, fitted-hardware test or electrical acceptance has been performed.
