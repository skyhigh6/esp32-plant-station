"""Package the R14 mechanical review with its retained R13 configuration."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'mechanical/concept_rev14_uno'
files=[p for folder in [OUT,ROOT/'mechanical/concept_rev13',ROOT/'mechanical/concept_rev8/references'] for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='release_manifest.json']
files += [ROOT/'docs/PROJECT_CONTROL.md',ROOT/'docs/Plant_Station_R13_Kit_Assembly_Instructions.md',ROOT/'docs/Plant_Station_R13_Design_Review.md',ROOT/'output/pdf/Plant_Station_R13_Kit_Assembly_Instructions.pdf',ROOT/'output/pdf/Plant_Station_R13_Design_Review.pdf',Path(__file__).resolve()]
files=sorted(set(files))
for p in files:
    if not p.is_file():raise FileNotFoundError(p)
manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
record={'revision':'R14 Uno','scope':'Mechanical review; R14 supplement takes precedence over R13 carrier mounting instructions','sha256':manifest}
(OUT/'release_manifest.json').write_text(json.dumps(record,indent=2),newline='\n')
archive=ROOT/'Plant_Station_R14_Uno_Review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
    z.write(OUT/'release_manifest.json','mechanical/concept_rev14_uno/release_manifest.json')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,name
print(f'PASS: {len(files)} files, all archive hashes verified; {archive.name} ({archive.stat().st_size} bytes)')
