# R7-A1 documentation verification

12 September 2026. Seven-page PDF and matching Markdown guide.

- PDF reopened with pypdf: seven pages with extractable text; six link annotations.
- All seven pages rendered with Poppler and visually reviewed: no observed clipping, overlap, missing images or illegible tables. Unused font-map warnings did not affect the rendered Helvetica text.
- CAD assembly, exploded and section views are R7 outputs. Reference drawing and LCD screenshot dimensions are distinguished from assumed depth and USB allowances.
- Ten exported STL hashes match the independent verification record. Independent checker exits 0. CAD generator shutdown exit 1 is recorded separately; no physical fit, leak or electrical test is claimed.
- Archive packaging checks CRC, ten STL entries and byte-for-byte agreement with source files.

## R6 to R7 STL comparison

- battery_tray.stl: unchanged
- button_fit_coupon.stl: unchanged
- fascia_charcoal.stl: changed
- hose_clip.stl: unchanged
- planter_sage.stl: unchanged
- sump_charcoal.stl: unchanged
- top_cover_sage.stl: changed
- tower_sage.stl: changed
