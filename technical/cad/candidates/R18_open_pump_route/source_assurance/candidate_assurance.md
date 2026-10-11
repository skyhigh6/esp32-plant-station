# Independent R18 C01 assurance — 11 October 2026

## Result

The candidate provides an open front lay-in route and open-top crossover, removes local tunnel supports in the comparative slice, and preserves the tested R17 fitted interfaces. It remains a physically untested candidate.

- Exported STL: 79,680 faces; one connected watertight mesh; consistent winding; positive volume 551,091.729 mm³; zero area-degenerate facets; original 207 × 100 × 158 mm envelope.
- Reopened STEP: one valid solid; 12,580.991927 mm³ removed; zero added material; zero removal outside the two declared cutters.
- Exact difference-volume checks preserve geometry left of x89, right of x114, rear band y96–100, geometry below z52, remaining below-rim partition, left USB/DC ports and rear-right lid fixing. This includes board mounts and the adjacent tube column.
- Intended front approach from y70 into the channel at y94 is clear at x108–113 over z53–60 and z61–128. Vertical wire corridor and top-access crossing have zero solid overlap. The larger straight lateral probes cross the preserved tube column; they are not the intended assembly approach or a failure.
- The retained crossover floor and below-rim partition material probes are filled. A full rear-wall cube probe is not required: original wall/riser geometry is curved and terminates locally. Exact rear-band preservation versus R17 passes.
- Optional route-trial STEP is the same cropped body after rigid translation: symmetric difference 0 mm³.

## Sliced support evidence

Copied before/after projects use the same stored user PLA settings and upright build transform; only candidate tower mesh/statistics were substituted. Originals remain untouched.

Bambu Studio 02.05.00.66 completed baseline slicing with exit 0 in 51.7 s and candidate retry with exit 0 in 39.0 s. The first candidate attempt failed with exit -6 because of copied XML namespace serialisation; that copy was repaired without changing geometry/settings.

Support plus support-interface commanded deposition falls from approximately 24.215 g to 23.699 g: 0.516 g / 2.13% less for the whole tower. This is derived from positive feature-tagged XY extrusion, respecting M82/M83/G92, using the stored 1.75 mm filament diameter and 1.26 g/cm³ density; it excludes retractions/E-only primes and is not observed material consumption.

`route_layer_comparison.png` was visually inspected. At z84.7 mm the baseline carries support/interface under the crossing; at z87.7 mm it carries interface inside the wire riser. Both disappear in the opened candidate route. Adjacent tube/rear-wall paths are retained. The support-motion midpoint metric inside the declared route cutters falls from 111.4709 mm filament across 180 layers to zero across zero layers.

Both slicer runs report ZFiller errors, missing full machine/process preset files and a bed-temperature-too-high-for-filament warning. Baseline logged 31 error lines; candidate logged 29. Candidate first-layer-time metadata is implausible. These toolpaths are comparative evidence, not files cleared to print. Inspect/reconcile the actual printer/material/profile and complete a full layer review before manufacture. No printer operation occurred.

## Process and remaining gates

Independent mesh checks, slice preparation, slice parsing and layer plotting exited 0. The STEP check scripts wrote complete results, then exited 1 during CAD-runtime shutdown; this is not a clean process exit. Parent-side independent exported checker separately provides exit-0 checks.

Actual terminated-lead dimensions and bend radius remain unknown. With planter/fascia/lid removed as required, dry-fit the actual lead by laying it into the channel; verify no pinching, sharp-edge damage, hardware obstruction or loss of service access. The optional exact-geometry route trial reduces full-print commitment. Leak/strength and powered-system acceptance remain separate physical gates.
