"""R18 candidate: open lay-in pump-wire route on frozen R17 geometry, mm."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / '.tools/cad-runtime'))
import cadquery as cq
import trimesh
import numpy as np

OUT = HERE / 'exports'
SOURCE = ROOT / 'technical/print/main_parts/step/tower_sump_body_uno_ports_r17.step'
EXPECTED_SOURCE_SHA256 = 'e74c073986564771eb660b70b004969c20f2cf9501af87a1c6b3494666879352'
V = cq.Vector

def box(lo, hi):
    return cq.Solid.makeBox(*(b-a for a,b in zip(lo,hi)), V(*lo))

def difference_volume(a, b):
    return a.cut(b).Volume()

def main():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise ValueError('R17 source changed; review the latest CAD before rebuilding')
    OUT.mkdir(exist_ok=True)
    old = cq.importers.importStep(str(SOURCE)).val()
    if not old.isValid() or len(old.Solids()) != 1:
        raise ValueError('Expected one valid R17 body')
    # Existing wire bore is centred x110/y92. Open its front face, then open
    # the horizontal crossing upwards so a terminated lead can be laid in.
    front = box((106.5,82,52),(114,96,129))
    crossing = box((89,88,77),(114,96,159))
    mask = front.fuse(crossing).clean()
    body = old.cut(mask).clean()
    if not body.isValid() or len(body.Solids()) != 1:
        raise ValueError('Open routing cut invalidated or disconnected the body')
    changed = old.cut(body)
    assert difference_volume(body, old) < .001
    assert changed.cut(mask).Volume() < .001
    # Protect all previously fitted board mounts, rear wall and underside space.
    protected = {
        'uno_and_relay':box((15,70,25),(86,101,140)),
        'below_rim_wet_dry_partition':box((-1,-1,-1),(106.5,101,60)),
        'sump_floor':box((-1,-1,-1),(208,101,4)),
        'tube_column':box((117,85,4),(132,101,130)),
        'lid_rear_right_fixing':box((89,81,151),(96,88,159)),
    }
    checks = {}
    for name, region in protected.items():
        overlap = changed.intersect(region).Volume()
        if overlap > .001:
            raise ValueError(f'Cut entered protected {name}: {overlap} mm3')
        checks[name+'_removed_mm3'] = overlap
    # A vertical extraction corridor reaches the open top continuously.
    # Probe diameter 4 inherited cable allowance, not measured fitted lead.
    corridor = box((90,90,78),(113,94,160))
    assert body.intersect(corridor).Volume() < .001
    assert body.intersect(box((108,82,53),(112,94,129))).Volume() < .001
    # Retain continuous floor under the above-rim crossover.
    floor = box((96,89,76),(105,95,77))
    assert floor.cut(body).Volume() < .001
    checks['lay_in_corridor_solid_overlap_mm3'] = body.intersect(corridor).Volume()
    checks['crossing_floor_min_z_mm'] = 77
    checks['crossing_floor_above_sump_rim_mm'] = 17
    checks['rear_wall_remaining_band_y_mm'] = [96,100]
    # Optional test artefact: actual route corner, translated only for printing.
    # No added assembly parts or hardware; print only if a route trial is needed.
    trial = body.intersect(box((88,80,70),(117,100,130))).clean()
    assert trial.isValid() and len(trial.Solids()) == 1
    trial = trial.translate((-88,-80,-70))
    report = {'revision':'R18 candidate C01', 'date':'2026-10-11', 'units':'mm',
              'source_step':str(SOURCE.relative_to(ROOT)), 'source_sha256':digest,
              'cadquery':cq.__version__, 'change_removed_mm3':changed.Volume(),
              'cuts_xyz_mm':{'front':[[106.5,82,52],[114,96,129]],
                             'open_top_crossing':[[89,88,77],[114,96,159]]},
              'preservation':checks, 'parts':{}}
    for name,shape in [('tower_open_pump_route_r18_c01',body),('route_trial_r18_c01',trial)]:
        cq.exporters.export(shape,str(OUT/(name+'.step')))
        cq.exporters.export(shape,str(OUT/(name+'.stl')),tolerance=.025,angularTolerance=.1)
        m=trimesh.load_mesh(OUT/(name+'.stl'))
        assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1
        reopened=cq.importers.importStep(str(OUT/(name+'.step'))).val()
        assert reopened.isValid() and len(reopened.Solids())==1
        assert abs(reopened.Volume()-shape.Volume()) < .01
        report['parts'][name]={'valid_single_solid':True,'mesh_one_component':True,
                              'watertight':True,'winding':True,'volume_mm3':m.volume,
                              'extents_mm':m.extents.tolist(),'STEP_readback':'PASS'}
    (HERE/'geometry_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: R18 exports, protected mounts/wet floor/tube/lid, lay-in corridors',flush=True)

if __name__ == '__main__':
    main()

