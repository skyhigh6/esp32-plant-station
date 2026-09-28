# Verification and source basis

| Location | Meaning |
|---|---|
| `cad/` | Original R17 digital records, independent mesh/section checks and actual-STL previews |
| `documents/` | PDF control/layout validation and clean rebuild results |
| `source_basis/` | Selected predecessor controls and frozen technical snapshots supporting revision bars |
| `REORGANISATION.json` | Scope, pre-cleanup baseline, publication transforms and exclusions |
| `release_checks.json` | Current print/input/firmware integrity and export check results |
| `firmware_host_tests.json` | Actual host assertion execution for this release |
| `plate_layout.json` | User-created 3MF source/publication hashes, metadata removal and comparison to all four current main models |
| `slicer_exports.json` | Four operator-supplied printer files; archive hashes, price/account metadata removal, executable-command preservation and G-code MD5 checks |
| `publication_review.json` | Outgoing publication-surface audit |

Snapshot path names identify their original configuration. Old links and rebuild commands in those records are historical; use the root README and PROJECT_CONTROL for current instructions. Some publication copies convert Windows-1252 text to UTF-8, remove private absolute paths and pin old GitHub links. The evidence register preserves original and publication hashes with the transformation record.

`source_basis/generators/` preserves the inherited R13/R15/R16 generation sources for traceability only. Their former checkout paths are no longer advertised as executable commands. Current R17 regeneration uses `technical/cad/build.py` and its frozen input. Inherited final STEP models remain editable under `technical/print/`.

Digital checks do not establish physical fit, strength, leakage, slicing suitability, calibrated volume or electrical acceptance. Original CAD runtime shutdown exit 1 remains an open anomaly. All physical actions A17-01–A17-13 remain open.
