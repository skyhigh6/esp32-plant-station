from pathlib import Path
import sys,json,hashlib,zipfile,xml.etree.ElementTree as ET
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import numpy as np
import trimesh
from scipy.spatial import cKDTree
ROOT=Path.cwd(); OUT=ROOT/'.build/r18_source_audit'
CORE='{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
PROD='{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}'
FILES=['technical/print/main_parts/stl/all plates r17.3mf','technical/print/main_parts/stl/fascia_charcoal.3mf','technical/print/plate_layout/r17_plate_layout.3mf','technical/print/slicer_exports/tower_r17.gcode.3mf']
KEYS=['printer_model','nozzle_diameter','print_settings_id','layer_height','wall_loops','filament_type','enable_support','support_type','support_on_build_plate_only','support_threshold_angle','support_top_z_distance','support_bottom_z_distance','support_object_xy_distance','support_interface_top_layers','support_interface_bottom_layers','brim_type','brim_width']
def sha(b):return hashlib.sha256(b).hexdigest()
def meta(e):return {k.attrib['key']:k.attrib.get('value') for k in e.findall('metadata') if 'key' in k.attrib}
def tmat(s):
 a=np.array([float(x) for x in s.split()]).reshape(4,3); return a[:3],a[3]
def inspect(fn):
 f=ROOT/fn
 result={'file':fn,'sha256':sha(f.read_bytes())}
 with zipfile.ZipFile(f) as z:
  result['archive_crc_error']=z.testzip(); result['member_count']=len(z.namelist());result['gcode_members']=[n for n in z.namelist() if n.endswith('.gcode')]
  result['mesh_member_sha256']={n:sha(z.read(n)) for n in z.namelist() if n.endswith('.model') and n!='3D/3dmodel.model'}
  model=ET.fromstring(z.read('3D/3dmodel.model'));result['unit']=model.attrib.get('unit')
  metadata={e.attrib['name']:e.text for e in model.findall(CORE+'metadata')}
  result['application']=metadata.get('Application');result['creation_date']=metadata.get('CreationDate');result['modification_date']=metadata.get('ModificationDate')
  settings=json.loads(z.read('Metadata/project_settings.config'));result['settings']={k:settings.get(k) for k in KEYS}
  ms=ET.fromstring(z.read('Metadata/model_settings.config')); resources=model.find(CORE+'resources');objs={o.attrib['id']:o for o in resources.findall(CORE+'object')} if resources is not None else {}
  build=model.find(CORE+'build');items={i.attrib['objectid']:i.attrib for i in build.findall(CORE+'item')} if build is not None else {}
  result['parts']=[]
  for o in ms.findall('object'):
   om=meta(o); oid=o.attrib['id']; mo=objs.get(oid);components=[]
   if mo is not None:
    comps=mo.find(CORE+'components');components=comps.findall(CORE+'component') if comps is not None else []
   for part in o.findall('part'):
    pm=meta(part); pid=part.attrib['id'];comp=next((c for c in components if c.attrib.get('objectid')==pid),None)
    rec={'object_id':oid,'part_id':pid,'name':pm.get('name'),'source_file':pm.get('source_file'),'object_overrides':{k:v for k,v in om.items() if k not in ['name','extruder']},'source_offset_mm':[float(pm.get('source_offset_'+k,0)) for k in 'xyz'],'source_matrix':pm.get('matrix'),'build_transform':items.get(oid,{}).get('transform')}
    if comp is None: result['parts'].append(rec);continue
    path=comp.attrib.get(PROD+'path','3D/3dmodel.model').lstrip('/');rec['mesh_member']=path;rec['component_transform']=comp.attrib.get('transform')
    mesh_model=ET.fromstring(z.read(path));source_obj=next(obj for obj in mesh_model.findall('.//'+CORE+'object') if obj.attrib['id']==pid)
    vs=source_obj.find('.//'+CORE+'vertices');ts=source_obj.find('.//'+CORE+'triangles');v=np.array([[float(e.attrib[k]) for k in 'xyz'] for e in vs]);t=np.array([[int(e.attrib[k]) for k in ['v1','v2','v3']] for e in ts])
    sourcev=v+np.array(rec['source_offset_mm']);rec['vertex_count']=len(v);rec['face_count']=len(t);rec['source_bounds_mm']=[sourcev.min(axis=0).tolist(),sourcev.max(axis=0).tolist()]
    if rec['build_transform']:
     cr,ct=tmat(rec['component_transform']);br,bt=tmat(rec['build_transform']);bv=(v@cr+ct)@br+bt;rec['build_bounds_mm']=[bv.min(axis=0).tolist(),bv.max(axis=0).tolist()];rec['build_height_mm']=float(np.ptp(bv[:,2]))
    canonical=ROOT/'technical/print/main_parts/stl'/pm.get('source_file','');
    if pm.get('source_file')=='top_cover_flush_r15.stl':canonical=ROOT/'technical/print/main_parts/stl/top_cover_flush_r16.stl'
    if canonical.exists():
     cm=trimesh.load(canonical,force='mesh');tree=cKDTree(cm.vertices);d,ix=tree.query(sourcev);rev=cKDTree(sourcev).query(cm.vertices)[0]
     # triangle connectivity compared using canonical vertex ids after nearest-point mapping
     mapped=np.sort(ix[t],axis=1);actual=np.sort(cm.faces,axis=1);tri_match=len(mapped)==len(actual) and set(map(tuple,mapped))==set(map(tuple,actual))
     rec['canonical_comparison']={'file':str(canonical.relative_to(ROOT)).replace('\\','/'),'sha256':sha(canonical.read_bytes()),'max_bidirectional_vertex_error_mm':float(max(d.max(),rev.max())),'vertex_match_0p0002mm':bool(max(d.max(),rev.max())<0.0002),'same_triangle_connectivity':bool(tri_match),'canonical_faces':len(cm.faces),'canonical_bounds_mm':cm.bounds.tolist()}
    result['parts'].append(rec)
  result['plates']=[{'metadata':meta(p),'instances':[meta(x) for x in p.findall('model_instance')]} for p in ms.findall('plate')]
 return result,settings
results=[];settings=[]
for f in FILES:
 r,s=inspect(f);results.append(r);settings.append(s)
# Keep keys and non-sensitive relevant print settings only. Never retain account or price fields.
changes={k:{'published':settings[2].get(k),'newer_user_project':settings[0].get(k)} for k in settings[0] if settings[0].get(k)!=settings[2].get(k) and not any(x in k.lower() for x in ['cost','price','userid','user_id','account','profile_id'])}
report={'audit_date':'2026-10-11','runtime':sys.version,'trimesh_version':trimesh.__version__,'units':'mm','files':results,'newer_user_project_setting_changes':changes,'limitations':['No slicer rerun or layer review performed','No source relationship to physical printed part independently established','No physical fit or leak acceptance inferred from digital matches']}
(OUT/'source_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8')
for r in results:
 print(r['file'],r['sha256'],r['creation_date'],'parts',len(r['parts']),'gcode',len(r['gcode_members']))
 for p in r['parts']:
  if 'canonical_comparison'in p:print(p['name'],p['face_count'],p['canonical_comparison']['max_bidirectional_vertex_error_mm'],p['canonical_comparison']['same_triangle_connectivity'],p.get('build_height_mm'))
print('changed settings keys',list(changes))
