"""Rebuild both R18 changes into scratch files without modifying issued exports.

Candidate sources remain frozen and hash-guard their R17 inputs. Each subprocess
gets a scratch HERE for reports and an explicit export directory. Process failure
is recorded even when geometry/export checks completed before runtime shutdown.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.build/r18_regeneration'
SOURCES = (
    ('R18_open_pump_route', ('tower_open_pump_route_r18_c01', 'route_trial_r18_c01')),
    ('R18_fascia_no_aux_apertures', ('fascia_no_aux_apertures_r18_c02',)),
)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for key, names in SOURCES:
        source = ROOT / 'technical/cad/candidates' / key / 'build.py'
        scratch = OUT / key
        exports = scratch / 'exports'
        exports.mkdir(parents=True, exist_ok=True)
        # Load source definitions with their original paths, then redirect output.
        # C02 also locates its preceding C01 input relative to HERE.
        code = """import importlib.util, pathlib
spec=importlib.util.spec_from_file_location('r18',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.HERE=pathlib.Path(SCRATCH);m.OUT=pathlib.Path(EXPORTS)
m.main()
"""
        code = 'SOURCE=' + repr(str(source)) + '\nSCRATCH=' + repr(str(scratch)) + '\nEXPORTS=' + repr(str(exports)) + '\n' + code
        result = subprocess.run([sys.executable, '-c', code], cwd=ROOT,
                                capture_output=True, text=True, timeout=180)
        record = {'source': source.relative_to(ROOT).as_posix(), 'exit_code': result.returncode,
                  'stdout': result.stdout, 'stderr': result.stderr, 'exports': {}}
        for name in names:
            for ext in ('stl', 'step'):
                path = exports / f'{name}.{ext}'
                if not path.is_file():
                    raise RuntimeError(f'Missing regenerated file {path}; exit {result.returncode}')
                record['exports'][path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            original = source.parent / 'exports' / f'{name}.stl'
            if hashlib.sha256(original.read_bytes()).digest() != hashlib.sha256((exports / f'{name}.stl').read_bytes()).digest():
                raise AssertionError(f'Regenerated STL differs: {name}')
        record['stl_hashes_match_candidate'] = True
        record['geometry_report'] = json.loads((scratch / 'geometry_checks.json').read_text())
        records.append(record)
    report = {'revision': 'R18', 'records': records,
              'status': 'Geometry/export checks completed; process anomaly remains' if any(x['exit_code'] for x in records) else 'PASS',
              'physical_acceptance': 'Open; no hardware operation'}
    (OUT / 'process_record.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'report': str(OUT / 'process_record.json')}), flush=True)
    if any(x['exit_code'] for x in records):
        sys.exit(1)

if __name__ == '__main__':
    main()
