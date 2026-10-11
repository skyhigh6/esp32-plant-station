from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import cadquery as cq
out=Path('.build/r18_fascia_audit');src=Path('technical/print/main_parts/step/fascia_charcoal.step');candidate=Path('technical/cad/candidates/R18_fascia_no_aux_apertures/exports/fascia_no_aux_apertures_r18_c02.step')
a=cq.importers.importStep(str(src)).val();b=cq.importers.importStep(str(candidate)).val()
def box(lo,hi):return cq.Solid.makeBox(*[y-x for x,y in zip(lo,hi)],cq.Vector(*lo))
def cyl(x,z,r,y,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(0,1,0))
aux=[(24,88,2.5),(48,88,2.5),(72,88,2.5),(67,45,2)]
patches=[cyl(x,z,r+.11,1,3) for x,z,r in aux];mask=patches[0]
for p in patches[1:]:mask=mask.fuse(p)
added=b.cut(a);removed=a.cut(b)
r={'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'baseline_valid':bool(a.isValid()),'candidate_valid':bool(b.isValid()),'candidate_solid_count':len(b.Solids()),'removed_mm3':removed.Volume(),'added_mm3':added.Volume(),'added_outside_small_aperture_regions_mm3':added.cut(mask).Volume(),'added_behind_plate_mm3':added.intersect(box((-1,4,-1),(100,20,160))).Volume(),'added_in_front_of_plate_mm3':added.intersect(box((-1,-1,-1),(100,1,160))).Volume()}
assert r['candidate_valid'] and r['candidate_solid_count']==1
for k in ['removed_mm3','added_outside_small_aperture_regions_mm3','added_behind_plate_mm3','added_in_front_of_plate_mm3']:assert r[k]<.001
r['closures']=[{'centre_xz_mm':[x,z],'nominal_diameter_mm':radius*2,'entire_plate_probe_missing_mm3':cyl(x,z,radius-.0001,1.0001,2.9998).cut(b).Volume()} for x,z,radius in aux]
assert all(p['entire_plate_probe_missing_mm3']<.001 for p in r['closures'])
# Retained bores by direct CAD circular probes and spatial difference.
retained=[('button1',24,72,6),('button2',48,72,6),('button3',72,72,6),('knob',32,48,3.5),('display_fixing1',10.5,97,1.5),('display_fixing2',10.5,128,1.5),('display_fixing3',85.5,97,1.5),('display_fixing4',85.5,128,1.5),('fascia_fixing1',9,10,1.7),('fascia_fixing2',9,148,1.7),('fascia_fixing3',87,10,1.7),('fascia_fixing4',87,148,1.7)]
r['retained_passage_overlap_mm3']={name:b.intersect(cyl(x,z,radius-.0001,1.0001,2.9998)).Volume() for name,x,z,radius in retained}
assert max(r['retained_passage_overlap_mm3'].values())<.001
lcd=box((12.31,1.001,100.21),(83.69,3.999,124.79));r['lcd_opening_overlap_mm3']=b.intersect(lcd).Volume();assert r['lcd_opening_overlap_mm3']<.001
rear_region=box((-1,4,-1),(100,20,160));ar=a.intersect(rear_region);br=b.intersect(rear_region)
r['rear_features_symmetric_difference_mm3']=ar.cut(br).Volume()+br.cut(ar).Volume();assert r['rear_features_symmetric_difference_mm3']<.001
r['tower_intersections_mm3']={}
for name,tf in [('R17','technical/print/main_parts/step/tower_sump_body_uno_ports_r17.step'),('R18_C01','technical/cad/candidates/R18_open_pump_route/exports/tower_open_pump_route_r18_c01.step')]:
 t=cq.importers.importStep(tf).val();r['tower_intersections_mm3'][name]=b.intersect(t).Volume();assert r['tower_intersections_mm3'][name]<.001
(out/'step_independent_checks.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2),flush=True)
