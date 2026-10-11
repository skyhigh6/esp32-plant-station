# Plant Station — R18

Arduino Uno plant station prototype. Current design **R18**, document issue **D03**, dated **11 October 2026**. Firmware remains **Uno UI v6**. New print/dry-fit, electrical and wet-operation acceptance remain open.

## Start here

- [Project control and acceptance gates](PROJECT_CONTROL.md)
- [Illustrated assembly manual — PLANT-AM-001](docs/documents/AM_R18/PLANT-AM-001_R18_D03.pdf)
- [Design review — PLANT-TR-001](docs/documents/TR_R18/PLANT-TR-001_R18_D03.pdf)
- [Test and acceptance sheets — PLANT-TS-001](docs/documents/TS_R18/PLANT-TS-001_R18_D03.pdf)
- [Complete R18 download](releases/R18/Plant_Station_R18_D03.zip)
- [Document index](docs/START_HERE.html) and [operator wiring view](docs/operator_view.html) — download and open locally

## Current print selection

Use four main parts and **one** knob selected for the actual shaft. Matching STEP files accompany these STLs; suffixes retain part provenance.

| Part | Current STL |
|---|---|
| Tower and sump | [tower_open_pump_route_r18.stl](technical/print/main_parts/stl/tower_open_pump_route_r18.stl) |
| Fascia | [fascia_no_aux_apertures_r18.stl](technical/print/main_parts/stl/fascia_no_aux_apertures_r18.stl) |
| Retained lid | [top_cover_flush_r16.stl](technical/print/main_parts/stl/top_cover_flush_r16.stl) |
| Retained planter | [planter_sage.stl](technical/print/main_parts/stl/planter_sage.stl) |

R18 opens the pump-wire riser and top crossing so the lead can be laid in with fitted terminations attached. It closes only three standalone LED apertures and the dedicated speaker aperture. The three illuminated-button openings and their LED wiring remain; firmware behaviour is unchanged.

Kevin **reports** that the latest R17 Uno and relay mounts fit perfectly. Their nominal mounting geometry is retained. This report closes no controlled hardware or electrical test. New route retention, bend clearance, printed fascia quality and combined dry fit remain open.

Check the retained [R17 port coupon](technical/print/fit_trials/stl/power_ports_fit_coupon_r17.stl) before accepting the estimated USB/DC interfaces. The [optional R18 route trial](technical/print/fit_trials/stl/route_trial_r18.stl) checks local lay-in clearance; it cannot accept the full assembly or cable retention. Review current STL layers and prepare new R18 slicing. The R17 plate project and supplied printer files contain predecessor geometry and are **historical evidence**, not current R18 toolpaths.

## Repository structure and traceability

| Folder | Contents |
|---|---|
| `technical/cad/` | Combined R18 rebuild entry, frozen inputs, C01/C02 source records and independent checker |
| `technical/print/` | Current and frozen predecessor exports, optional trials and knob choices; selection and hashes in the manifest |
| `firmware/` | Unchanged Uno UI v6 sketch, headers, host assertions and build instructions |
| `docs/` | R18/D03 manuals, editable sources and controls; preserved R17/D02 set |
| `verification/` | CAD/document evidence, documentary source basis and release checks |
| `releases/R18/` | Current package and SHA-256 manifest |
| `releases/R17/` | Preserved previous release |

`PROJECT_CONTROL.md` is the current baseline pointer. The [print manifest](technical/print/manifest.json) distinguishes current selected parts from frozen predecessors. The [evidence register](docs/control/evidence_register.json) and change matrix support document bars. Historical snapshots and candidate records describe their issue-time status.

## Rebuild and verify

See [document instructions](docs/README.md), [CAD instructions](technical/cad/README.md), [firmware instructions](firmware/README.md) and [verification scope](verification/README.md).

```powershell
python technical/cad/build_r18.py
python technical/cad/check_exports.py
python scripts/rebuild_documents.py
python scripts/verify_release.py
python scripts/package_release.py
```

Use the recorded compatible Python runtime and `requirements-docs.txt` / `requirements-cad.txt`. Current R18 regeneration prints PASS and reproduces the three STL hashes, but child processes end with Windows status `0xC0000374`; the wrapper returns 1. Source candidate builders also recorded a shutdown exit 1. Independent export checks remain a separate gate. Publication does not establish physical, powered, wet or printer acceptance.
