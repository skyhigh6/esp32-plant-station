"""Package exactly the R8 CAD outputs and manufacturing preparation documents."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
CAD=ROOT/'mechanical/concept_rev8'
paths=[p for p in CAD.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths.extend(ROOT/p for p in (
    'output/pdf/Plant_Station_R8_Illustrated_Assembly_Guide.pdf',
    'docs/ASSEMBLY_GUIDE_R8.md','docs/BOM_R8.md','docs/R8_DOCUMENTATION_QA.md',
    'docs/PROJECT_CONTROL.md','docs/ELECTRONICS.md','firmware/README.md',
    'scripts/build_guide_r8.py','scripts/check_guide_r8.py','scripts/package_r8_illustrated.py'))
record=json.loads((CAD/'independent_mesh_check.json').read_text())
assert record['result']=='PASS' and len(record['files'])==22
assert json.loads((CAD/'step_check.json').read_text())['result']=='PASS'
for name,data in record['files'].items():
    assert hashlib.sha256((CAD/'stl'/name).read_bytes()).hexdigest()==data['sha256']
archive=ROOT/'ESP32_Plant_R8_Illustrated_Review.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
    z.writestr('START_HERE.txt','Plant Station R8 / R8-A1, 12 September 2026\n'
        'Start with output/pdf/Plant_Station_R8_Illustrated_Assembly_Guide.pdf.\n'
        'BOM: docs/BOM_R8.md. Print files: mechanical/concept_rev8/stl (mm).\n'
        '22 STL files: seven enclosure parts, eight knob alternatives, six coupons, one marking blank.\n'
        'Measure USB/shaft/piezo/fasteners and print coupons before large parts.\n'
        'Geometry verified; physical fit, slicing, leak testing and electrical commissioning pending.\n')
    for p in sorted(paths):z.write(p,p.relative_to(ROOT).as_posix())
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if n.endswith('.stl')])==22
    for p in paths:assert z.read(p.relative_to(ROOT).as_posix())==p.read_bytes(),p
print('PASS: R8 ZIP CRC, 22 STLs, all archived files match source; sha256='+hashlib.sha256(archive.read_bytes()).hexdigest())
