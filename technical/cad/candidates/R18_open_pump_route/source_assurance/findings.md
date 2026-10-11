# R18 source audit — 11 October 2026

Read-only inspection of released R17, the later user 3MFs and installed slicer. Evidence: `source_audit.json`, `audit_sources.py`, `bambu_cli_help.txt`.

## Confirmed source findings

- No tower geometry conflict in the examined files. The tower mesh member in the 30 September user `all plates r17.3mf` is byte-identical to the 28 September publication layout. Its 81,676 triangles match canonical R17 STL connectivity; maximum source-frame vertex disagreement is 0.000005787 mm.
- All four mesh XML members in those two four-plate projects are byte-identical. Part/build transforms are also equal. The tower is upright, spans 207 × 100 × 158 mm, and sits at print z=0.
- The 7 October `fascia_charcoal.3mf` contains 18 mixed Plant/TVC/Satcom parts. It has Plant fascia/lid geometry but no named Plant tower. Its Plant fascia/lid matches the released STL within 0.000007451 mm. Preserve this user file without rewriting it.
- Newer four-plate settings select PLA in filament slot 1, compared with ABS in the publication layout, with associated temperature, cooling and flow changes. Stored tower settings retain the X1 Carbon/0.4 mm profile, 0.2 mm layers, six walls, tree(auto) support, support on model surfaces and a 30 degree support setting.
- Both four-plate projects contain no G-code. Stored thumbnails/layer metadata do not prove current successful slicing.
- Released R17 STL is watertight, winding-consistent, one connected component, positive volume and no area-degenerate facets at the tested 1e-10 mm² threshold. Self-intersection checking was not performed.
- Installed Bambu Studio 02.05.00.66 supports a CLI. Captured help exits 0; `--slice`, `--export-3mf`, `--load-settings`, `--load-filaments` and `--info` are available. No slicing or machine operation was performed. Official reference: https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage

## Source hashes

| Source | SHA-256 |
|---|---|
| R17 tower STL | f598a7865bed6395d74d9a249cbfd3799a14e0e47ceb7b97f982f2658e0b827b |
| R17 tower STEP | e74c073986564771eb660b70b004969c20f2cf9501af87a1c6b3494666879352 |
| Later all plates r17.3mf | c8343ca833e78734466df041dc11677183dbe5941f2b859ea60ff4f0b57a7792 |
| Mixed fascia_charcoal.3mf | 8affac6f39286460068aaa49c8ff7c89dd5471ae7b13280b354badcfc6e41589 |
| Published r17_plate_layout.3mf | e6fc11e80708da4ea7c5d34030e66ae2a3d438bf6985524a4290dff3725e798c |

## Candidate acceptance checks

1. Reopen candidate STEP as one valid solid and STL as one watertight connected mesh with positive volume and consistent winding.
2. Compare candidate against canonical R17 with boolean differences: no added material; all removal inside the two declared route cutters. Board mounts, lid, left power ports and below-rim dry partition must match the baseline outside those cutters.
3. Section the wire path across the low vertical route and top crossover. Prove the side opening is continuous and the crossover is accessible from above, without a retained roof or sealed pocket.
4. Inspect the upright STL underside surfaces and compare a fresh slice using the same chosen profile. Digital underside area is not a support-volume result.
5. Dry-fit the actual terminated lead by laying it into the open path with the lid/fascia removable. Verify no pinching, sharp-edge damage, board/relay obstruction or loss of service access. Actual connector size and minimum bend radius remain unmeasured.
6. Water/leak and powered-system acceptance remain separate physical tests.

## Limitations

The physical printed part was identified as the newest by the user; this audit establishes file equality but cannot independently identify its print source. A later active CAD edit outside the examined files would need inspection. Slicer settings are stored values, not an approved material choice or print result. The R15-labelled lid in both four-plate projects has the same vertices/face count as R16 within 0.000002602 mm but differs in triangle connectivity; this non-target lid was not modified or promoted.
