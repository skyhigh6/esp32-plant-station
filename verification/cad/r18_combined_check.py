"""Independent combined R18 promotion/assembly checks. Units mm; no hardware claims."""
from pathlib import Path
import argparse,hashlib,json,itertools,re,sys,zipfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.tools/cad-runtime'))
import trimesh
REPORT=ROOT/'verification/cad/r18_combined_checks.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(mesh_only=False):
    report=json.loads(REPORT.read_text()) if REPORT.exists() else {}
    report['date']='2026-10-11';report['units']='mm'
    promoted={
      'tower':('technical/print/main_parts','tower_open_pump_route_r18','technical/cad/candidates/R18_open_pump_route/exports/tower_open_pump_route_r18_c01'),
      'fascia':('technical/print/main_parts','fascia_no_aux_apertures_r18','technical/cad/candidates/R18_fascia_no_aux_apertures/exports/fascia_no_aux_apertures_r18_c02'),
      'route_trial':('technical/print/fit_trials','route_trial_r18','technical/cad/candidates/R18_open_pump_route/exports/route_trial_r18_c01')}
    hashes={};meshes={}
    for label,(directory,name,cand) in promoted.items():
        for ext in ['stl','step']:
            p=ROOT/directory/ext/(name+'.'+ext);c=ROOT/(cand+'.'+ext)
            equal=sha(p)==sha(c);assert equal,(str(p),'promotion changed bytes')
            hashes[str(p.relative_to(ROOT))]={'sha256':sha(p),'candidate_sha256':sha(c),'byte_identical':equal}
        p=ROOT/directory/'stl'/(name+'.stl');m=trimesh.load(p,force='mesh')
        result={'watertight':bool(m.is_watertight),'winding_consistent':bool(m.is_winding_consistent),'components':len(m.split(only_watertight=False)),'volume_mm3':float(m.volume),'bounds_mm':m.bounds.tolist(),'degenerate_faces_area_lt_1e_10':int((m.area_faces<1e-10).sum())}
        assert result['watertight'] and result['winding_consistent'] and result['components']==1 and result['volume_mm3']>0 and result['degenerate_faces_area_lt_1e_10']==0
        meshes[label]=result
    report['promotion_hashes']=hashes;report['exported_mesh_checks']=meshes
    manifests={}
    for p in (ROOT/'technical/cad/candidates').glob('*/manifest.json'):
        data=json.loads(p.read_text());bad=[f for f,h in data['sha256'].items() if not(p.parent/f).exists() or sha(p.parent/f)!=h]
        manifests[str(p.relative_to(ROOT))]={'entries':len(data['sha256']),'mismatches':bad};assert not bad
    print_manifest=json.loads((ROOT/'technical/print/manifest.json').read_text());bad=[d['file'] for d in print_manifest if not(ROOT/d['file']).exists() or sha(ROOT/d['file'])!=d['sha256']]
    manifests['technical/print/manifest.json']={'entries':len(print_manifest),'mismatches':bad};assert not bad
    report['manifests']=manifests
    findings=[]
    for p in (ROOT/'technical/cad/candidates').rglob('*'):
        if p.is_file() and p.suffix in ['.json','.md','.py','.txt','.log']:
            text=p.read_text(encoding='utf8',errors='ignore');kinds=[]
            if re.search(r'C:[\\/]+Users[\\/]+kevin',text,re.I):kinds.append('personal absolute filesystem path')
            if re.search(r'(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_-]{30,}|ghp_[A-Za-z0-9]{20,})',text):kinds.append('possible secret pattern')
            if kinds:findings.append({'file':str(p.relative_to(ROOT)),'findings':kinds})
    report['publication_text_metadata_findings']=findings
    report['publication_exclusions']=['Original two user 3MF projects: DesignerUserId account metadata and filament_cost fields','Local candidate review ZIPs: duplicate archives, C01 contains original unredacted failed-attempt log','All .build comparison toolpaths/projects: local validation outputs']
    REPORT.write_text(json.dumps(report,indent=2)+'\n');print('PASS: promotion hashes, mesh topology and manifests',flush=True)
    if mesh_only:return
    import cadquery as cq
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    V=cq.Vector
    def load(p):
        s=cq.importers.importStep(str(ROOT/p)).val();assert s.isValid() and len(s.Solids())==1;return s
    def box(lo,hi):return cq.Solid.makeBox(*[b-a for a,b in zip(lo,hi)],V(*lo))
    def cyl(x,z,r,y,h):return cq.Solid.makeCylinder(r,h,V(x,y,z),V(0,1,0))
    oldtower=load('technical/print/main_parts/step/tower_sump_body_uno_ports_r17.step');tower=load('technical/print/main_parts/step/tower_open_pump_route_r18.step')
    oldfascia=load('technical/print/main_parts/step/fascia_charcoal.step');fascia=load('technical/print/main_parts/step/fascia_no_aux_apertures_r18.step')
    lid=load('technical/print/main_parts/step/top_cover_flush_r16.step');planter=load('technical/print/main_parts/step/planter_sage.step')
    def pilots(shape):
        found=[]
        for face in shape.Faces():
            if face.geomType()!='CYLINDER':continue
            c=BRepAdaptor_Surface(face.wrapped).Cylinder();ax=c.Axis();p=ax.Location();d=ax.Direction();bb=face.BoundingBox()
            if abs(c.Radius()-1.4)<1e-6 and abs(abs(d.Y())-1)<1e-6 and 15<p.X()<86 and 25<p.Z()<140 and bb.ymin>60:
                found.append({'centre_xz_mm':[round(p.X(),6),round(p.Z(),6)],'diameter_mm':round(2*c.Radius(),6),'y_extent_mm':[round(bb.ymin,6),round(bb.ymax,6)]})
        return sorted(found,key=lambda c:tuple(c['centre_xz_mm']))
    before_pilots=pilots(oldtower);after_pilots=pilots(tower);assert len(before_pilots)==8 and before_pilots==after_pilots,(before_pilots,after_pilots)
    removed=oldtower.cut(tower);tmask=box((106.5,82,52),(114,96,129)).fuse(box((89,88,77),(114,96,159)))
    route={'removed_mm3':removed.Volume(),'added_mm3':tower.cut(oldtower).Volume(),'removed_outside_cutter_mm3':removed.cut(tmask).Volume(),'rear_band_removed_mm3':removed.intersect(box((-1,96,-1),(208,101,159))).Volume(),'below_rim_partition_removed_mm3':removed.intersect(box((96,-1,4),(106.5,101,60))).Volume(),'sump_floor_removed_mm3':removed.intersect(box((-1,-1,-1),(208,101,4))).Volume(),'tube_column_removed_mm3':removed.intersect(box((117,85,4),(132,101,130))).Volume(),'lid_fixing_removed_mm3':removed.intersect(box((89,81,151),(96,88,159))).Volume(),'front_lay_in_corridor_overlap_mm3':tower.intersect(box((108,70,53),(113,94,128))).Volume(),'top_crossover_overlap_mm3':tower.intersect(box((90,90,78),(113,94,159))).Volume()}
    assert all(v<.001 for k,v in route.items() if k!='removed_mm3')
    aux=[(24,88,2.5),(48,88,2.5),(72,88,2.5),(67,45,2)];patches=[cyl(x,z,r+.11,1,3) for x,z,r in aux];mask=patches[0]
    for patch in patches[1:]:mask=mask.fuse(patch)
    added=fascia.cut(oldfascia);rear=box((-1,4,-1),(100,20,160));ar=oldfascia.intersect(rear);br=fascia.intersect(rear)
    fascia_checks={'added_mm3':added.Volume(),'removed_mm3':oldfascia.cut(fascia).Volume(),'added_outside_four_plate_regions_mm3':added.cut(mask).Volume(),'rear_features_symmetric_difference_mm3':ar.cut(br).Volume()+br.cut(ar).Volume(),'closure_probe_missing_mm3':[cyl(x,z,r-.0001,1.0001,2.9998).cut(fascia).Volume() for x,z,r in aux]}
    assert fascia_checks['removed_mm3']<.001 and fascia_checks['added_outside_four_plate_regions_mm3']<.001 and fascia_checks['rear_features_symmetric_difference_mm3']<.001 and max(fascia_checks['closure_probe_missing_mm3'])<.001
    oldparts={'tower':oldtower,'fascia':oldfascia,'lid':lid,'planter':planter};parts={'tower':tower,'fascia':fascia,'lid':lid,'planter':planter};intersections={}
    for a,b in itertools.combinations(parts,2):
        before=oldparts[a].intersect(oldparts[b]).Volume();after=parts[a].intersect(parts[b]).Volume()
        intersections[a+'__'+b]={'baseline_mm3':before,'combined_R18_mm3':after,'change_mm3':after-before};assert after<=before+.001
    report['reopened_STEP_all_valid_single_solids']=True;report['retained_eight_board_pilots']=after_pilots;report['eight_board_pilots_identical_to_R17']=True;report['pump_route_checks']=route;report['fascia_checks']=fascia_checks;report['assembly_pair_intersections']=intersections
    report['limitations']=['Digital geometry assurance only; no new physical fit, leak, strength or electrical acceptance','Existing comparative slices retain documented errors and profile warnings; no new slicing performed','CAD process may exit1 after reports during known runtime shutdown anomaly; actual exit separately recorded']
    REPORT.write_text(json.dumps(report,indent=2)+'\n');print('PASS: eight retained board pilots, protected features and combined STEP assembly pairs',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mesh-only',action='store_true');main(p.parse_args().mesh_only)
