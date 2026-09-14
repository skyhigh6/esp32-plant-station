from pathlib import Path
import zipfile, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
files=list((ROOT/'mechanical/concept_rev13').rglob('*'))
files += [ROOT/'output/pdf/Plant_Station_R13_Kit_Assembly_Instructions.pdf',ROOT/'output/pdf/Plant_Station_R13_Design_Review.pdf',
ROOT/'docs/Plant_Station_R13_Kit_Assembly_Instructions.md',ROOT/'docs/Plant_Station_R13_Design_Review.md',
ROOT/'scripts/build_guide_r13.py',ROOT/'scripts/package_r13_illustrated.py',
ROOT/'docs/PROJECT_CONTROL.md',ROOT/'docs/ELECTRONICS.md',ROOT/'firmware/README.md']
files += list((ROOT/'mechanical/concept_rev8/references').rglob('*'))
files=[p for p in files if p.is_file() and '__pycache__' not in p.parts]
manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
out=ROOT/'ESP32_Plant_R13_Illustrated_Review.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(ROOT).as_posix())
 z.writestr('SHA256_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
print('PASS',out.name,len(files),'files',out.stat().st_size,'bytes')
