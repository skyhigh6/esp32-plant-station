"""Reopen every STEP part, compare with STL extents and require valid single solids."""
from pathlib import Path
import sys,json
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[1]/'.tools/cad-runtime'))
import cadquery as cq
import trimesh
import numpy as np

report={'revision':'R12','units':'mm','files':{}}
for p in sorted((OUT/'step').glob('*.step')):
    sh=cq.importers.importStep(str(p)).val()
    assert sh.isValid() and len(sh.Solids())==1,p
    bb=sh.BoundingBox();dims=[bb.xlen,bb.ylen,bb.zlen]
    mesh=trimesh.load_mesh(OUT/'stl'/(p.stem+'.stl'))
    assert np.allclose(dims,mesh.extents,atol=.03),p
    assert abs(sh.Volume()-mesh.volume)/sh.Volume()<.002,p
    report['files'][p.name]={'valid':True,'solids':1,'bounds_mm':dims,'volume_mm3':sh.Volume()}
assert len(report['files'])==20
assy=cq.importers.importStep(str(OUT/'assembly.step')).val()
assert assy.isValid() and len(assy.Solids())==5
report['assembly_solids']=5
report['result']='PASS'
(OUT/'step_check.json').write_text(json.dumps(report,indent=2))
print('PASS: reopened 20 STEP single solids and five-part assembly; STL bounds/volumes agree',flush=True)
