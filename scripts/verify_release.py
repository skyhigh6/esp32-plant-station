"""Verify current export/input hashes, source equivalence and independent ports."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def contained(path: str) -> Path:
    result = (ROOT / path).resolve()
    if not result.is_relative_to(ROOT):
        raise ValueError(f'Manifest path outside release: {path}')
    return result

def main() -> None:
    prints = json.loads((ROOT / 'technical/print/manifest.json').read_text())
    inputs = json.loads((ROOT / 'technical/cad/inputs/manifest.json').read_text())
    for row in prints + inputs:
        if digest(contained(row['file'])) != row['sha256']:
            raise AssertionError(f'File changed: {row["file"]}')
    if len(prints) != 46:
        raise AssertionError('Expected 46 controlled print exports')
    evidence = json.loads((ROOT / 'docs/control/evidence_register.json').read_text())
    preserved_firmware = 0
    for row in evidence:
        snapshot = (ROOT / 'docs' / row['snapshot']).resolve()
        if not snapshot.is_relative_to(ROOT) or digest(snapshot) != row['sha256']:
            raise AssertionError(f'Frozen source mismatch: {row["source"]}')
        if row['source'].startswith('firmware/arduino/PlantUno/'):
            if digest(contained(row['source'])) != row['sha256']:
                raise AssertionError(f'Current UI v6 source changed: {row["source"]}')
            preserved_firmware += 1
    if preserved_firmware != 3:
        raise AssertionError('Expected three preserved Uno source files')
    for command in ([sys.executable, str(ROOT / 'technical/cad/check_exports.py')],
                    [sys.executable, str(ROOT / 'docs/tooling/validate_set.py')]):
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'Check failed: {Path(command[1]).name}\n{result.stdout}\n{result.stderr}')
        print(result.stdout.strip())
    report = {'date':'2026-09-28', 'status':'PASS', 'print_export_hashes':len(prints),
              'frozen_cad_input_hashes':len(inputs), 'source_basis_hashes':len(evidence),
              'current_firmware_files_preserved':preserved_firmware, 'independent_mesh_checker_exit':0,
              'pdf_validator_exit':0, 'engineering_scope':'No geometry, firmware or issued PDF content change',
              'physical_acceptance':'Open; no hardware or printer test performed'}
    (ROOT / 'verification/release_checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: release integrity and relocated independent checks')

if __name__ == '__main__':
    main()
