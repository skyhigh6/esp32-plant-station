# Independent combined R18 assurance

11 October 2026. The combined R18 tower and fascia promotion preserves the independently checked C01/C02 geometry. No new physical acceptance is inferred.

## Confirmed

- All six promoted STL/STEP files (tower, fascia and optional route trial) are byte-identical to their reviewed candidate exports. Both candidate manifests and the 52-entry print manifest match all recorded file hashes.
- All three promoted STLs reopen as one connected, watertight, consistently wound component with positive volume and no tested area-degenerate faces.
- Current tower/fascia, retained lid/planter and predecessor STEP files reopen as valid single solids.
- All eight nominal Ø2.8 board pilots retain their exact R17 centres and 11 mm depth (y76–87). Board geometry remains unchanged.
- Pump-route changes remove 12,580.991927 mm³ only within the two declared cutters, add no material, retain the rear band, below-rim partition, sump floor, tube column and lid fixing, and leave front lay-in/top crossover corridors clear.
- Fascia changes add 214.413698608 mm³ solely in the four obsolete through-plate aperture regions, remove no material and retain all rear geometry exactly. All four bore closure probes are filled. Other passages/interfaces remain unchanged outside the four patches; preceding C02 section/probe checks remain applicable because the promotion is byte-identical.
- Every one of the six assembly pair intersections (tower/fascia/lid/planter) is zero in both baseline and combined R18. There is no baseline clash concealed by the comparison.
- The two original user 3MF projects and both local candidate review ZIPs are confirmed ignored for publication. User projects contain account/financial metadata; the C01 local ZIP retains an original personal path. Publication text now contains no detected personal absolute path or common API-key/token pattern. This is a bounded pattern check, not a claim to discover every possible secret.

## Actual process result and limits

The full combined checker printed both passing summaries and saved complete STEP/mesh evidence, then exited 1 without a traceback during the existing CAD-runtime shutdown anomaly. It is not a clean process exit. The separate `--mesh-only` reopening, topology, hash and manifest check exited 0.

No additional slicing, hardware operation, publishing or Git mutation was performed by this assurance task. Prior comparative slice warnings/errors remain documented. Actual terminated-lead size/bend radius, revised-route dry fit, new fascia print quality, leak/strength and electrical acceptance remain physical gates. The user-reported R17 board fit is preserved geometry evidence and does not establish R18 physical acceptance.

Evidence: `r18_combined_checks.json`; reproducible checker: `r18_combined_check.py` (`--mesh-only` bypasses CAD-runtime shutdown).
