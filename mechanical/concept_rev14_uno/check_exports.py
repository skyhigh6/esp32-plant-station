"""Independent exported-mesh checks, without importing the CAD builder."""
from pathlib import Path
import sys, json, hashlib
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[1]/'.tools/cad-runtime'))
import trimesh
import numpy as np

report={'units':'mm','revision':'R14 Uno','files':{},'sections':{}}
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

report['sections']['mount_pilots']=bore_section(meshes['tower_sump_body_uno'],[0,80,0],[0,1,0],[[79.75,107.56],[79.75,79.62],[28.95,122.8],[27.68,74.54]],[0,2],[2.8]*4)
report['sections']['mount_outsides']=bore_section(meshes['tower_sump_body_uno'],[0,80,0],[0,1,0],[[79.75,107.56],[79.75,79.62],[28.95,122.8],[27.68,74.54]],[0,2],[6]*4)
report['sections']['coupon_holes']=bore_section(meshes['uno_mount_fit_coupon'],[0,0,1],[0,0,1],[[66.04,35.56],[66.04,7.62],[15.24,50.8],[13.97,2.54]],[0,1],[3.2]*4)
assert np.allclose(meshes['tower_sump_body_uno'].extents,[207,100,158],atol=.01)
(OUT/'independent_mesh_check.json').write_text(json.dumps(report,indent=2))
print('PASS: two meshes, edge incidence, no degenerate faces, bounds and 12 mount circles')
