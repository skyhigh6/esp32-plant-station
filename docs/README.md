# Controlled documentation — R18 / D03

Open [START_HERE.html](START_HERE.html) locally. The current set is PLANT-AM-001, PLANT-TR-001 and PLANT-TS-001 at **R18 / D03**, dated **11 October 2026**. Actual page counts and effective-page lists are in each delivered PDF and placement manifest.

Each `documents/*_R18/` folder contains an illustrated PDF, canonical editable `document.json`, generated Markdown companion, self-contained assets, page-placement manifest, renders and review records. Edit JSON/assets, then rebuild. Generated Markdown edits do not update the PDF. The `*_R17/` folders preserve the previous R17/D02 issued set; they are not current instructions.

`control/` holds identities, cumulative change matrix, source register and readiness actions. Validation is in `../verification/documents/`. Historical snapshots under `../verification/source_basis/` and C01/C02 records under `../technical/cad/candidates/` support lineage; candidate issue-time status statements are historical after R18 incorporation.

```powershell
python docs/tooling/build_document.py docs/documents/AM_R18/document.json
python docs/tooling/build_document.py docs/documents/TR_R18/document.json
python docs/tooling/build_document.py docs/documents/TS_R18/document.json
python docs/tooling/validate_set.py
python scripts/rebuild_documents.py
```

Run from the repository root using the compatible Python runtime with `requirements-docs.txt`. Clean rebuild compares page images and placements. PDF container metadata may vary; rendered content is the comparison basis. Inspect changed pages before updating review records. A17-01–A17-13 remain open; A18-01–A18-04 add print, lay-in route, retention and combined dry-fit checks. Document validation does not close physical acceptance.
