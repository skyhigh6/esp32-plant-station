# R18 / D03 control scheme

Issued 11 October 2026 for prototype review. Current instruction set; print/dry-fit, electrical and wet acceptance remain open.

## Identity and baseline

PLANT-AM-001 (assembly manual), PLANT-TR-001 (design review) and PLANT-TS-001 (test/acceptance sheets) are issued at design R18 and document issue D03. Uno firmware remains UI v6. These are separate configuration identities.

The immediate predecessor for all three documents is R17/D02, retained in `docs/documents/*_R17/` with its R17 release. Older AM R14/D01 and TR R13/D01 history is retained; TS was first assigned at R17/D02. No R15/R16 manual editions are invented. Frozen C01/C02 candidate records describe their original review-stage status; their changes are now combined in R18.

## Format and change bars

A4 portrait; 40 mm binding/history zone; Helvetica; grey table rules; revision/control pages; every-page effective issue; section/page navigation; numbered header/footer. Bars apply only to source-backed surviving paragraphs/rows and resolve to `change_matrix.json`. Configuration captions identify the source geometry in illustrations. Historical labels do not make superseded instructions current.

T18-1 identifies the open pump-wire route, T18-2 the four fascia aperture closures, and T18-3 reported board-fit evidence plus combined configuration/documentation and unresolved manufacturing/acceptance. Integrated button openings/LED wiring remain current. Historical standalone LED and speaker seats are no longer installation instructions; only their four front apertures are closed, with unused rear geometry retained.

## Status

All action owners: Unassigned; target dates: Not set. A17-01–A17-13 remain open. A18-01 checks lay-in route fit; A18-02 checks bends/edges/retention/service; A18-03 checks fascia face and controls dry fit; A18-04 checks full dry assembly and slicer/print review. Actual-result fields remain blank/Not tested.

Kevin's reported successful latest R17 Uno/relay fit is partial first-article evidence only. Digital geometry checks retain nominal mounts; they do not establish physical acceptance. Source candidate builders printed PASS then returned exit 1. Current regeneration reproduced all three STL hashes, with child shutdown status `0xC0000374` and wrapper exit 1; independent checks return 0. Historical software/serial evidence is labelled and does not close powered tests.

The retained R17 plate project and printer files are predecessor evidence, not R18 toolpaths. R18 needs new layer/support review and slicing. No hardware upload, printer operation or physical acceptance is performed by the document issue.

## Deliverables and rebuild

Each R18 document folder contains PDF, editable JSON, Markdown companion, self-contained assets, placements, renders and review records. Rebuild with `docs/tooling/build_document.py`; validate the set and run `scripts/rebuild_documents.py`. See `docs/README.md` for commands. Source-backed changes preserve R17 sources and originals; the current print manifest distinguishes R18 selections from frozen predecessor exports.
