# Plant Station — R17

Arduino Uno plant station prototype. Current design **R17**, controlled document issue **D02**, firmware **Uno UI v6**. Physical fit and electrical acceptance remain open.

## Start here

- [Project control and acceptance gates](PROJECT_CONTROL.md)
- [Illustrated assembly manual — PLANT-AM-001](docs/documents/AM_R17/PLANT-AM-001_R17_D02.pdf)
- [Design review — PLANT-TR-001](docs/documents/TR_R17/PLANT-TR-001_R17_D02.pdf)
- [Test and acceptance sheets — PLANT-TS-001](docs/documents/TS_R17/PLANT-TS-001_R17_D02.pdf)
- [Complete R17 download](releases/R17/Plant_Station_R17_D02.zip)
- [Document index](docs/START_HERE.html) and [operator wiring view](docs/operator_view.html) — download and open locally

## Repository structure

| Folder | Contents |
|---|---|
| `technical/cad/` | Current R17 generator, parameters, frozen STEP input and independent checker |
| `technical/print/` | 4 main parts, 11 fit trials, 8 knob choices; matching STL and STEP, with source hashes |
| `firmware/` | Current Uno sketch, adjacent headers, host assertions and build instructions |
| `docs/` | Three illustrated PDFs, editable JSON/Markdown, assets, page renders and document controls |
| `references/` | Supplied USB dimension image and illustration provenance |
| `verification/` | CAD/document results, selected predecessor source basis and release checks |
| `releases/R17/` | Frozen complete package and SHA-256 manifest |
| `scripts/` | Portable document rebuild, export verification and packaging tools |

The tower replaces the broad USB cable opening with an estimated **9.8 × 4.2 mm** USB-C aperture, **Ø2.8 mm** fixing pilots at **15.2 mm** pitch, and an adjacent **Ø10 mm** DC-extension hole. Print the port coupon first. USB dimensions are authorised estimates; actual fit has not been tested.

Use the R17 tower, retained R16 lid carrying R15 geometry, retained R13 fascia/planter and **one** suitable knob. Revision suffixes identify part provenance. Do not print all alternatives.

## Traceability

`PROJECT_CONTROL.md` is the single current baseline pointer. The D02 manuals carry revision history, effective-page lists and source-backed change bars. The [print manifest](technical/print/manifest.json) identifies every selected export. The [evidence register](docs/control/evidence_register.json) identifies the documentary source basis; snapshot records are historical evidence, not current instructions.

Superseded release folders and archives have been removed from the current branch tree. Git history retains published predecessors; a verified external local backup preserves unpublished work. Repository visibility and existing history are unchanged.

## Rebuild and verify

See [document instructions](docs/README.md), [CAD instructions](technical/cad/README.md), [firmware instructions](firmware/README.md) and [verification scope](verification/README.md).

```powershell
python scripts/rebuild_documents.py
python scripts/verify_release.py
python scripts/package_release.py
```

Requires Python 3.12 and the libraries listed in `requirements-docs.txt` and `requirements-cad.txt`. The CAD runtime has a recorded shutdown exit-code anomaly; the independent export checker remains a separate gate. No physical, powered, wet or printer acceptance is implied by publication.
