"""Check a clean, isolated rebuild against all delivered rendered pages."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    outcomes = {}
    with tempfile.TemporaryDirectory(prefix='plant-r17-document-rebuild-') as temp:
        fresh = Path(temp) / 'docs'
        (fresh / 'control').mkdir(parents=True)
        (fresh / 'tooling').mkdir()
        shutil.copy2(DOCS / 'control/change_matrix.json', fresh / 'control/change_matrix.json')
        shutil.copy2(DOCS / 'tooling/build_document.py', fresh / 'tooling/build_document.py')
        for key in ('AM_R17', 'TR_R17', 'TS_R17'):
            original = DOCS / 'documents' / key
            target = fresh / 'documents' / key
            shutil.copytree(original / 'assets', target / 'assets')
            shutil.copy2(original / 'document.json', target / 'document.json')
            result = subprocess.run([sys.executable, str(fresh / 'tooling/build_document.py'),
                                     str(target / 'document.json')], capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f'{key}: rebuild failed\n{result.stdout}\n{result.stderr}')
            if json.loads((original / 'placements.json').read_text()) != json.loads((target / 'placements.json').read_text()):
                raise AssertionError(f'{key}: page placements changed')
            pages = sorted((original / 'rendered').glob('page-*.png'))
            if len(pages) != len(list((target / 'rendered').glob('page-*.png'))):
                raise AssertionError(f'{key}: page count changed')
            for page in pages:
                if digest(page) != digest(target / 'rendered' / page.name):
                    raise AssertionError(f'{key}: rendered page changed: {page.name}')
            outcomes[key] = {'exit_code':0, 'pages':len(pages), 'placement_manifest_equal':True,
                             'all_rendered_png_hashes_equal':True}
    (ROOT / 'verification/documents/rebuild_verification.json').write_text(json.dumps(outcomes, indent=2) + '\n')
    print(f'PASS: clean document rebuild, {sum(x["pages"] for x in outcomes.values())} pages')

if __name__ == '__main__':
    main()
