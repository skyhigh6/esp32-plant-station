from pathlib import Path
import sys,json,zipfile,xml.etree.ElementTree as ET,subprocess,hashlib
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import trimesh,numpy as np
out=Path('.build/r18_source_audit'); f=Path('technical/cad/candidates/R18_open_pump_route/exports/tower_open_pump_route_r18_c01.stl');m=trimesh.load(f,force='mesh')
r={'candidate_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'watertight':bool(m.is_watertight),'winding_consistent':bool(m.is_winding_consistent),'connected_components':len(m.split(only_watertight=False)),'volume_mm3':float(m.volume),'bounds_mm':m.bounds.tolist(),'degenerate_faces':int((m.area_faces<1e-10).sum()),'faces':len(m.faces)}
(out/'candidate_mesh_checks.json').write_text(json.dumps(r,indent=2));print(r)
core='{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
ET.register_namespace('',core[1:-1])
ET.register_namespace('p','http://schemas.microsoft.com/3dmanufacturing/production/2015/06')
with zipfile.ZipFile('technical/print/main_parts/stl/all plates r17.3mf') as z:
 members={n:z.read(n) for n in z.namelist()}
# Baseline is a verbatim local copy. Candidate copy substitutes tower mesh only.
(out/'baseline_project.3mf').write_bytes(Path('technical/print/main_parts/stl/all plates r17.3mf').read_bytes())
t=ET.fromstring(members['3D/Objects/object_5.model']);mesh=t.find('.//'+core+'mesh');vs=mesh.find(core+'vertices');ts=mesh.find(core+'triangles');vs.clear();ts.clear()
for v in m.vertices-np.array([103.5,50,79]): ET.SubElement(vs,core+'vertex',dict(zip('xyz',[format(float(a),'.10g') for a in v])))
for face in m.faces:ET.SubElement(ts,core+'triangle',dict(zip(['v1','v2','v3'],[str(a) for a in face])))
members['3D/Objects/object_5.model']=ET.tostring(t,encoding='utf-8',xml_declaration=True)
ms=ET.fromstring(members['Metadata/model_settings.config'])
for ob in ms.findall('object'):
 if ob.attrib['id']=='2':
  for e in ob.iter():
   if 'face_count' in e.attrib:e.attrib['face_count']=str(len(m.faces))
members['Metadata/model_settings.config']=ET.tostring(ms,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(out/'candidate_project.3mf','w',compression=zipfile.ZIP_DEFLATED) as z:
 for n,b in members.items():z.writestr(n,b)
print('created local baseline/candidate slice inputs; original untouched')

