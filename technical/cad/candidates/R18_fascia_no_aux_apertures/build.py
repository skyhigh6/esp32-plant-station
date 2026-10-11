"""R18 C02 fascia-only candidate: close three LED bores and one sound bore."""
from pathlib import Path
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'.tools/cad-runtime'))
import cadquery as cq
import trimesh

SOURCE=ROOT/'technical/print/main_parts/step/fascia_charcoal.step'
EXPECTED='659f2b4dccc36b2a2557f485f04079922de0ce02b9f36d2cac726a22ef2eeda4'
OUT=HERE/'exports'
V=cq.Vector
PLATE_Y=(1.0,4.0)
# Nominal bores from current source. The 0.1 mm radial overlap ensures union;
# material is added only where an original aperture is empty within the plate.
APERTURES=[('LED1',24.,88.,5.),('LED2',48.,88.,5.),('LED3',72.,88.,5.),('speaker',67.,45.,4.)]

def cyl(x,z,r,y,length):
    return cq.Solid.makeCylinder(r,length,V(x,y,z),V(0,1,0))

def main():
    actual=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if actual!=EXPECTED:raise ValueError('Fascia source hash changed; inspect current edited CAD')
    old=cq.importers.importStep(str(SOURCE)).val()
    assert old.isValid() and len(old.Solids())==1
    patches=[cyl(x,z,d/2+.1,PLATE_Y[0],PLATE_Y[1]-PLATE_Y[0]) for _,x,z,d in APERTURES]
    mask=patches[0]
    new=old
    for p in patches:new=new.fuse(p).clean()
    for p in patches[1:]:mask=mask.fuse(p).clean()
    assert new.isValid() and len(new.Solids())==1
    added=new.cut(old)
    removed=old.cut(new).Volume()
    outside=added.cut(mask).Volume()
    assert removed<.001 and outside<.001
    closures={}
    for name,x,z,d in APERTURES:
        probe=cyl(x,z,d/2-.01,1.001,2.998)
        missing=probe.cut(new).Volume()
        assert missing<.001,(name,missing)
        closures[name]={'centre_xz_mm':[x,z],'original_diameter_mm':d,'full_plate_missing_mm3':missing}
    # Assert unchanged entire outer bounding envelope, not just a front view.
    a,b=old.BoundingBox(),new.BoundingBox()
    for attribute in ('xmin','xmax','ymin','ymax','zmin','zmax'):
        assert abs(getattr(a,attribute)-getattr(b,attribute))<1e-6
    matings={}
    towers={'R17':ROOT/'technical/print/main_parts/step/tower_sump_body_uno_ports_r17.step',
            'R18_C01_route_only':HERE.parent/'R18_open_pump_route/exports/tower_open_pump_route_r18_c01.step'}
    for label,path in towers.items():
        tower=cq.importers.importStep(str(path)).val()
        before=old.intersect(tower).Volume()
        after=new.intersect(tower).Volume()
        assert before<.001 and after<.001
        matings[label]={'before_mm3':before,'after_mm3':after,'tower_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    OUT.mkdir(exist_ok=True)
    name='fascia_no_aux_apertures_r18_c02'
    cq.exporters.export(new,str(OUT/(name+'.step')))
    cq.exporters.export(new,str(OUT/(name+'.stl')),tolerance=.025,angularTolerance=.1)
    reopened=cq.importers.importStep(str(OUT/(name+'.step'))).val()
    assert reopened.isValid() and len(reopened.Solids())==1
    assert abs(reopened.Volume()-new.Volume())<.01
    m=trimesh.load_mesh(OUT/(name+'.stl'))
    assert m.is_watertight and m.is_winding_consistent and len(m.split())==1 and m.volume>0
    report={'revision':'R18 C02 fascia-only local candidate','date':'2026-10-11','units':'mm','cadquery':cq.__version__,
            'source':str(SOURCE.relative_to(ROOT)),'source_sha256':actual,
            'plate_front_rear_y_mm':list(PLATE_Y),'obsolete_apertures':closures,
            'change':{'added_mm3':added.Volume(),'removed_mm3':removed,'added_outside_aperture_patches_mm3':outside},
            'retained':'All geometry outside four aperture patches; rear collars/seat, all buttons, knob, display and fixings',
            'tower_intersections':matings,'STEP_readback':'valid single solid','mesh':{'closed':True,'winding':True,'components':1,'volume_mm3':float(m.volume),'bounds_mm':m.bounds.tolist()}}
    (HERE/'geometry_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: four filled apertures, no removals, retained envelope and zero tower interference',flush=True)

if __name__=='__main__':main()
