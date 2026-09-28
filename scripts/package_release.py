"""Package the explicit current technical tree and verify every archived hash."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / 'releases/R17'
FOLDERS = ('technical', 'firmware', 'docs', 'references', 'verification', 'scripts')
ROOT_FILES = ('README.md', 'PROJECT_CONTROL.md', '.gitignore', '.gitattributes',
              'requirements-docs.txt', 'requirements-cad.txt')
SUFFIXES = {'.md','.json','.py','.cpp','.ino','.h','.html','.png','.jpg','.stl','.step','.pdf','.3mf'}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    layout = json.loads((ROOT / 'verification/plate_layout.json').read_text())
    slicer = json.loads((ROOT / 'verification/slicer_exports.json').read_text())['records']
    approved_projects = {layout['published_file']} | {row['file'] for row in slicer}
    approved_exports = {row['file'] for row in json.loads((ROOT / 'technical/print/manifest.json').read_text())}
    files = [ROOT / name for name in ROOT_FILES]
    for folder in FOLDERS:
        for path in (ROOT / folder).rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            if path.suffix.lower() not in SUFFIXES:
                raise ValueError(f'Unexpected publication type: {path.relative_to(ROOT)}')
            relative = path.relative_to(ROOT).as_posix()
            if path.suffix.lower() == '.3mf' and relative not in approved_projects:
                raise ValueError(f'Unreviewed 3MF project; add controlled evidence first: {relative}')
            if path.suffix.lower() in ('.stl','.step') and path.is_relative_to(ROOT / 'technical/print') and relative not in approved_exports:
                raise ValueError(f'Uncontrolled print export: {relative}')
            files.append(path)
    manifest = {p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in sorted(files)}
    RELEASE.mkdir(parents=True, exist_ok=True)
    manifest_bytes = (json.dumps({'revision':'R17','document_issue':'D02','files':manifest}, indent=2) + '\n').encode()
    (RELEASE / 'manifest.json').write_bytes(manifest_bytes)
    archive = RELEASE / 'Plant_Station_R17_D02.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in manifest:
            info = zipfile.ZipInfo(name, (2026,9,28,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, (ROOT / name).read_bytes())
        info = zipfile.ZipInfo('releases/R17/manifest.json', (2026,9,28,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, manifest_bytes)
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or set(z.namelist()) != set(manifest) | {'releases/R17/manifest.json'}:
            raise AssertionError('Archive membership/CRC failure')
        for name, expected in manifest.items():
            if digest(z.read(name)) != expected:
                raise AssertionError(f'Archive hash mismatch: {name}')
        if z.read('releases/R17/manifest.json') != manifest_bytes:
            raise AssertionError('Archived manifest changed')
    (RELEASE / 'SHA256SUMS.txt').write_text(f'{digest(archive.read_bytes())}  {archive.name}\n{digest(manifest_bytes)}  manifest.json\n')
    print(json.dumps({'status':'PASS','archive':archive.relative_to(ROOT).as_posix(),
                      'files':len(manifest)+1,'bytes':archive.stat().st_size,'sha256':digest(archive.read_bytes())}))

if __name__ == '__main__':
    main()
