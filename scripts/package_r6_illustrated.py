"""Package R6 mechanical outputs and illustrated guidance; retain relative image paths."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
paths=[p for p in (ROOT/'mechanical/concept_rev6').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths.extend(ROOT/p for p in (
    'output/pdf/Plant_Station_R6_Illustrated_Assembly_Guide.pdf',
    'docs/ASSEMBLY_GUIDE_R6.md','docs/R6_DOCUMENTATION_QA.md','docs/PROJECT_CONTROL.md',
    'docs/ELECTRONICS.md','docs/BOM.md','firmware/README.md',
    'scripts/build_guide_r6.py','scripts/package_r6_illustrated.py'))
record=json.loads((ROOT/'mechanical/concept_rev6/independent_mesh_check.json').read_text())
for name,data in record['files'].items():
    assert hashlib.sha256((ROOT/'mechanical/concept_rev6/stl'/name).read_bytes()).hexdigest()==data['sha256']
archive=ROOT/'ESP32_Plant_R6_Illustrated_Review.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
    z.writestr('START_HERE.txt',
        'Plant Station R6 / documentation R6-A1\n'
        'Start with output/pdf/Plant_Station_R6_Illustrated_Assembly_Guide.pdf.\n'
        'Print files: mechanical/concept_rev6/stl (millimetres).\n'
        'Fit checks and source: mechanical/concept_rev6/README.md.\n'
        'Concept art is illustrative; hardware fit and electrical operation remain unverified.\n'
        'Firmware source remains in https://github.com/skyhigh6/esp32-plant-station .\n')
    for p in sorted(paths):z.write(p,p.relative_to(ROOT).as_posix())
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if n.endswith('.stl')])==8
    for p in paths:assert z.read(p.relative_to(ROOT).as_posix())==p.read_bytes(),p
print('PASS: archive CRC; every archived file matches source; eight STLs',flush=True)
