from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import trimesh,numpy as np

out=Path('.build/r18_fascia_audit');src=Path('technical/print/main_parts/stl/fascia_charcoal.stl');candidate=Path('technical/cad/candidates/R18_fascia_no_aux_apertures/exports/fascia_no_aux_apertures_r18_c02.stl')
a=trimesh.load(src,force='mesh');b=trimesh.load(candidate,force='mesh')
aux=[(24,88),(48,88),(72,88),(67,45)]
def sections(m,y):
 p=m.section(plane_origin=[0,y,0],plane_normal=[0,1,0]);return [d[:,[0,2]] for d in p.discrete]
def centre(v):return (v.min(axis=0)+v.max(axis=0))/2
def point_line_distance_max(v,w):
    starts=w[:-1];edges=w[1:]-w[:-1];denom=(edges*edges).sum(axis=1);denom=np.maximum(denom,1e-30)
    frac=np.clip(((v[:,None,:]-starts[None,:,:])*edges[None,:,:]).sum(axis=2)/denom[None,:],0,1)
    distances=np.linalg.norm(v[:,None,:]-(starts[None,:,:]+frac[:,:,None]*edges[None,:,:]),axis=2)
    return float(distances.min(axis=1).max())
def sampled_hausdorff(v,w):return max(point_line_distance_max(v,w),point_line_distance_max(w,v))
r={'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'watertight':bool(b.is_watertight),'winding_consistent':bool(b.is_winding_consistent),'components':len(b.split(only_watertight=False)),'positive_volume':bool(b.volume>0),'volume_mm3':float(b.volume),'bounds_mm':b.bounds.tolist(),'degenerate_faces':int((b.area_faces<1e-10).sum()),'sections':[]}
assert r['watertight'] and r['winding_consistent'] and r['components']==1 and r['positive_volume'] and r['degenerate_faces']==0
for y in [1.01,2.5,3.99]:
 old=sections(a,y);new=sections(b,y);retained=[v for v in old if not any(np.linalg.norm(centre(v)-c)<.1 for c in aux)]
 assert len(old)-len(retained)==4
 assert len(new)==len(retained),(y,len(new),len(retained))
 distances=[]
 for v in retained:
  matched=min(new,key=lambda n:np.linalg.norm(centre(n)-centre(v)));distances.append(sampled_hausdorff(v,matched))
 assert max(distances)<.001,(y,max(distances))
 absent=all(not any(np.linalg.norm(centre(v)-c)<.1 for v in new) for c in aux);assert absent
 buttons=[]
 for x in [24,48,72]:
  button=min(new,key=lambda n:np.linalg.norm(centre(n)-[x,72]));buttons.append({'centre_xz_mm':centre(button).tolist(),'section_diameters_xz_mm':np.ptp(button,axis=0).tolist()})
 r['sections'].append({'y_mm':y,'baseline_loops':len(old),'candidate_loops':len(new),'four_obsolete_passages_absent':absent,'max_retained_section_sampled_polyline_distance_mm':max(distances),'buttons':buttons})
(out/'mesh_and_section_checks.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2),flush=True)

