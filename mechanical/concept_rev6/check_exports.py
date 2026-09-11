"""Independent exported-mesh checks, without importing the CAD builder."""
from pathlib import Path
import sys, json, hashlib
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[1]/'.tools/cad-runtime'))
import trimesh
import numpy as np

report={'units':'mm','revision':'R6','files':{},'sections':{}}
meshes={}
for p in sorted((OUT/'stl').glob('*.stl')):
    mesh=trimesh.load_mesh(p,process=True)
    meshes[p.stem]=mesh
    incidence=np.bincount(mesh.edges_unique_inverse)
    rec={'closed':bool(mesh.is_watertight),'winding':bool(mesh.is_winding_consistent),
         'components':len(mesh.split()),'volume_mm3':float(mesh.volume),
         'bounds_mm':mesh.bounds.tolist(),'all_edges_two_faces':bool(np.all(incidence==2)),
         'degenerate_faces':int(np.count_nonzero(mesh.area_faces<1e-10)),
         'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    assert rec['closed'] and rec['winding'] and rec['components']==1 and rec['volume_mm3']>0
    assert rec['all_edges_two_faces'] and rec['degenerate_faces']==0
    report['files'][p.name]=rec

def bore_section(mesh, origin, normal, centres, axes, expected):
    section=mesh.section(plane_origin=origin,plane_normal=normal)
    assert section is not None
    result=[]
    for centre,diameter in zip(centres,expected):
        found=[]
        for loop in section.discrete:
            xy=loop[:,axes]
            radial=np.linalg.norm(xy-np.array(centre),axis=1)
            if np.max(np.abs(radial-diameter/2))<0.025:
                found.append({'centre_mm':centre,'nominal_diameter_mm':diameter,
                              'radial_min_mm':float(radial.min()),'radial_max_mm':float(radial.max())})
        assert len(found)==1,(centre,diameter,found)
        result.extend(found)
    return result

report['sections']['button_bores']=bore_section(meshes['fascia_charcoal'],[0,2,0],[0,1,0],
    [[24,72],[48,72],[72,72]],[0,2],[12,12,12])
report['sections']['coupon_bores']=bore_section(meshes['button_fit_coupon'],[0,0,1.5],[0,0,1],
    [[14,14],[38,14],[62,14]],[0,1],[12,12.2,12.4])
assert abs(meshes['sump_charcoal'].extents[2]-60)<1e-5
assert abs(meshes['tower_sage'].extents[2]-158)<1e-5
assert len(meshes)==8
report['result']='PASS'
report['limits']=['No slicing, material validation or physical fit/leak test','No full mesh self-intersection check']
(OUT/'independent_mesh_check.json').write_text(json.dumps(report,indent=2))
print('PASS: eight exported meshes; exact button/coupon sections; sump height',flush=True)
