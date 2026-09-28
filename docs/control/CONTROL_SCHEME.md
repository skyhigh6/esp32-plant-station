# R17 / D02 control scheme

Issued 28 September 2026 for prototype review. Current instruction set; physical and electrical acceptance remain open.

## Identity and baseline

PLANT-AM-001 (assembly manual), PLANT-TR-001 (design review), PLANT-TS-001 (test/acceptance sheets). Design R17 is distinct from document issue D02 and Uno firmware UI v6. D02 incorporates new current technical content using the prior D01 enhanced format; it is not cosmetic restyling alone.

AM predecessor: R14 D01. TR predecessor: R13 D01. TS is newly assigned; no earlier TS issue is asserted. R15/R16 are source-backed mechanical changes incorporated here without intermediate manual issues. Prior originals are retained in Git history and the external local backup; selected D01 control records are retained in verification/source_basis.

## Format and change bars

A4 portrait; 40 mm binding/history zone; Helvetica; grey table rules; revision/control pages; every-page effective issue; section/page navigation; numbered header/footer. Bars apply only to source-backed surviving paragraphs/rows. Mixed illustrations remain unbarred and carry configuration captions. Every bar resolves to change_matrix.json. R17 electrical labels mark incorporation into the manual, not the date of software introduction.

## Status

All physical action owners: Unassigned; target dates: Not set. Actions A17-01 through A17-13 remain open. Serial/software/digital evidence is labelled; test actuals are blank/Not tested. CAD shutdown exit 1 is retained as an anomaly. No printer, hardware, upload or external publication is performed by the documentation issue.

## Deliverables and rebuild

Each document folder contains PDF, editable JSON, Markdown companion, image assets, placement manifest, renders and content/visual audit. Build the PDFs with tooling/build_document.py using Python with reportlab, pymupdf and pillow. Assets and JSON are self-contained. The current JSON and assets are the editable document sources. Superseded checkout-dependent authoring scripts remain in the external backup. Selected STL/STEP files are preserved byte-for-byte in technical/print; do not print every option.
