# Current CAD authority — R18 combined prototype

11 October 2026. Units: mm; x right, y rear, z up.

Read [R18_CONFIGURATION.md](R18_CONFIGURATION.md) for the current editable sources, rebuild, geometry evidence and limitations. R18 combines the open pump-wire tower with the fascia having four obsolete apertures closed. Retained Uno/relay mounts, lid, planter and illuminated-button interfaces are unchanged.

- `build_r18.py`: builds both changes into `.build/r18_regeneration`; never overwrites issued exports.
- `candidates/`: hash-guarded C01/C02 editable sources and reviewed exports/evidence.
- `parameters.json` and `build.py`: inherited R17 power-port parameters and predecessor generator; retained for provenance.
- `check_exports.py`: independent current R18 tower and retained R17 port-coupon topology and six port sections.
- `../../verification/cad/r18_combined_check.py`: export promotion, eight board pilots and combined four-part STEP assembly checks; use `--mesh-only` for the separate mesh check.
- `../../verification/cad/r18_regeneration_process.json`: recorded scratch rebuild; identical regenerated STL hashes, abnormal CAD shutdown.
- [Frozen R17 CAD note](../../verification/source_basis/notes/R17_cad_README.md): preceding geometry, estimates and historical rebuild instructions.

Current exports are selected explicitly by `../print/manifest.json`. Do not print the frozen predecessor tower/fascia or every knob/coupon. R17 plate projects and supplied machine files are historical. No accepted R18 machine toolpath or physical print is issued here.

Estimated USB aperture 9.8 x 4.2 mm, 15.2 mm pilot pitch and the user-requested 10 mm DC bore remain inherited. Fit actual connectors to the retained port coupon before accepting these interfaces. Actual wire terminations, bends and retention require the new R18 test records. Digital geometry evidence and the reported board fit do not close physical or electrical acceptance.
