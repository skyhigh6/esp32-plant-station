# R18 C01 candidate — pump-wire lay-in route

[Change record and acceptance actions](CHANGE_RECORD.md) · [Reported first-article fit](reported_first_article.json)

- [Tower STL](exports/tower_open_pump_route_r18_c01.stl) and [STEP](exports/tower_open_pump_route_r18_c01.step).
- [Optional route trial STL](exports/route_trial_r18_c01.stl) and [STEP](exports/route_trial_r18_c01.step): 29 x 20 x 60 mm actual-route corner; use only for width/lay-in and local slicing trials, not full retention/strength acceptance.
- [Sliced route comparison](source_assurance/route_layer_comparison.png).
- [Section comparison](before_after_section.png) and [route detail](before_after_route.png).
- [CAD checks](geometry_checks.json), [independent mesh checks](independent_checks.json), [process status](process_record.json).
- [Source and independent assurance](source_assurance/findings.md), including [slice comparison](source_assurance/slice_comparison.json).
- `build.py`: frozen-source, dimensioned candidate. `check_and_render.py`: exported-mesh verification and previews.

Rebuild from the project root with a Python runtime containing CadQuery 2.8, trimesh 5.1, NumPy and matplotlib (local .tools/cad-runtime is used):

```powershell
python technical/cad/candidates/R18_open_pump_route/build.py
python technical/cad/candidates/R18_open_pump_route/check_and_render.py
```

R17 remains the issued configuration. C01 changes only the route and preserves reported-fitted mounting geometry. No publish or printer operation was performed.
