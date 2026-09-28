# Controlled documentation — R17 / D02

Open [START_HERE.html](START_HERE.html) locally. The three manuals contain 40 pages in total: assembly 20, design review 11, test sheets 9.

Each `documents/` folder contains an illustrated PDF, canonical editable `document.json`, generated Markdown companion, image assets, page-placement manifest, page renders and visual/content review records. Edit JSON and assets, then rebuild. Generated Markdown edits do not update the PDF.

`control/` holds document identities, the cumulative change matrix and source register. Validation results are in `../verification/documents/`. Historical snapshots under `../verification/source_basis/` support lineage; they are not current operating instructions.

```powershell
python docs/tooling/build_document.py docs/documents/AM_R17/document.json
python docs/tooling/build_document.py docs/documents/TR_R17/document.json
python docs/tooling/build_document.py docs/documents/TS_R17/document.json
python docs/tooling/validate_set.py
python scripts/rebuild_documents.py
```

Run from the repository root. Install `requirements-docs.txt` in an isolated Python environment. `rebuild_documents.py` uses a temporary directory and compares every page image and placement record against the delivered set. PDF container metadata may vary; rendered content is the comparison basis. Re-render and inspect changed pages before updating review records.
