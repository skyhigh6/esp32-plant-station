"""Independent exported-mesh checks, without importing the CAD builder."""
from pathlib import Path
import sys, json, hashlib
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[1]/'.tools/cad-runtime'))
import trimesh
import numpy as np

report={'units':'mm','revision':'R10','files':{},'sections':{}}
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
report['sections']['LCD_bores']=bore_section(meshes['fascia_charcoal'],[0,2,0],[0,1,0],
    [[10.5,97],[85.5,97],[10.5,128],[85.5,128]],[0,2],[3]*4)
report['sections']['PCB_pilots']=bore_section(meshes['tower_sump_body'],[0,80,0],[0,1,0],
    [[19.5,78.5],[76.5,78.5],[19.5,138.5],[76.5,138.5]],[0,2],[2.8]*4)
def rectangular_opening(mesh,origin,normal,axes,expected):
    section=mesh.section(plane_origin=origin,plane_normal=normal)
    matches=[]
    for loop in section.discrete:
        a=loop[:,axes];bounds=np.array([a.min(axis=0),a.max(axis=0)])
        if np.allclose(bounds,np.array(expected),atol=.02):matches.append(bounds.tolist())
    assert len(matches)==1,(expected,matches)
    return matches[0]
report['sections']['LCD_aperture']=rectangular_opening(meshes['fascia_charcoal'],[0,2,0],[0,1,0],[0,2],[[12.3,100.2],[83.7,124.8]])
report['sections']['USB_access']=rectangular_opening(meshes['tower_sump_body'],[3,0,0],[1,0,0],[1,2],[[49,98.5],[77,118.5]])
report['sections']['piezo_seat']=bore_section(meshes['fascia_charcoal'],[0,5,0],[0,1,0],[[67,45]],[0,2],[10.4])
report['sections']['LED_glue_collars']=bore_section(meshes['fascia_charcoal'],[0,5,0],[0,1,0],[[24,88],[48,88],[72,88]],[0,2],[5.4]*3)
roof_expected=(96*100-(4-np.pi)*7**2)*3-4*np.pi*1.7**2*3
assert abs(meshes['top_cover_sage'].volume-roof_expected)<2, 'Unexpected solid roof volume'
report['sections']['closed_roof']={'analytic_volume_mm3':roof_expected,'mesh_volume_mm3':meshes['top_cover_sage'].volume}
for n,d in [('5p0',5),('5p2',5.2),('6p0',6),('6p2',6.2),('6p35',6.35),('6p55',6.55)]:
    report['sections']['knob_'+n]=bore_section(meshes['knob_round_'+n],[0,0,8],[0,0,1],[[0,0]],[0,1],[d])
for n,d,f in [('6p0',6,1.5),('6p2',6.2,1.6)]:
    mesh=meshes['knob_D_'+n]
    loops=mesh.section(plane_origin=[0,0,8],plane_normal=[0,0,1]).discrete
    inner=[p for p in loops if max(np.linalg.norm(p[:,:2],axis=1))<4]
    assert len(inner)==1
    assert abs(inner[0][:,1].max()-f)<.025
    assert abs(inner[0][:,1].min()+d/2)<.025
    report['sections']['knob_D_'+n]={'diameter_mm':d,'flat_offset_mm':f,'result':'PASS'}

assert abs(meshes['tower_sump_body'].extents[2]-158)<1e-5
report['sections']['LCD_coupon_bores']=bore_section(meshes['lcd_fit_coupon'],[0,0,1.5],[0,0,1],
    [[4.5,4.5],[79.5,4.5],[4.5,35.5],[79.5,35.5]],[0,1],[3]*4)
report['sections']['carrier_coupon_bores']=bore_section(meshes['carrier_fit_coupon'],[0,0,1],[0,0,1],
    [[6.5,6.5],[66.5,6.5],[6.5,63.5],[66.5,63.5]],[0,1],[2.8]*4)
assert len(meshes)==21
report['result']='PASS'
report['limits']=['No slicing, material validation or physical fit/leak test','No full mesh self-intersection check']
(OUT/'independent_mesh_check.json').write_text(json.dumps(report,indent=2))
print('PASS: 21 exported meshes; rotated mount pattern, USB opening, piezo/LED seats and knob sections',flush=True)
