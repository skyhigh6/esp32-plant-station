"""Independent exported-mesh checks and before/after visual review, no CAD import."""
from pathlib import Path
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'.tools/cad-runtime'))
import trimesh
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=ROOT/'technical/print/main_parts/stl/tower_sump_body_uno_ports_r17.stl'
NEW=HERE/'exports/tower_open_pump_route_r18_c01.stl'
meshes={'R17':trimesh.load_mesh(BASE),'R18 C01':trimesh.load_mesh(NEW)}
report={'units':'mm','files':{},'support_proxy':{},'limitations':['Downward face area is geometry evidence, not slicer support consumption','No full self-intersection test or physical acceptance']}
for p in sorted((HERE/'exports').glob('*.stl')):
    m=trimesh.load_mesh(p)
    incidence=np.bincount(m.edges_unique_inverse)
    assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1
    assert np.all(incidence==2) and not np.any(m.area_faces<1e-10)
    report['files'][p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'closed':True,'consistent_winding':True,'components':1,'all_edges_two_faces':True,'degenerate_faces':0,'volume_mm3':float(m.volume),'bounds_mm':m.bounds.tolist()}
for name,m in meshes.items():
    c=m.triangles_center
    local=np.all((c>=[89,82,52]) & (c<=[114,96,159]),axis=1)
    down=m.face_normals[:,2]<-.5
    report['support_proxy'][name]={'route_faces_downward_more_than_30deg_from_vertical_area_mm2':float(m.area_faces[local&down].sum())}
old_area=report['support_proxy']['R17']['route_faces_downward_more_than_30deg_from_vertical_area_mm2']
new_area=report['support_proxy']['R18 C01']['route_faces_downward_more_than_30deg_from_vertical_area_mm2']
report['support_proxy']['reduction_percent']=100*(old_area-new_area)/old_area
assert new_area<old_area
# Compare all board mounting sections as circles in the actual mesh exports.
centres=[(79.75,107.56),(79.75,79.62),(28.95,122.8),(27.68,74.54),(23.75,35.75),(23.75,56.25),(68.25,35.75),(68.25,56.25)]
report['board_pilot_sections']={}
for name,m in meshes.items():
    sec=m.section(plane_origin=[0,80,0],plane_normal=[0,1,0])
    values=[]
    for x,z in centres:
        match=[]
        for loop in sec.discrete:
            r=np.linalg.norm(loop[:,[0,2]]-[x,z],axis=1)
            if np.max(np.abs(r-1.4))<.025:match.append([float(r.min()),float(r.max())])
        assert len(match)==1,(name,x,z,match)
        values.append({'centre_xz_mm':[x,z],'radius_min_max_mm':match[0]})
    report['board_pilot_sections'][name]=values
assert np.allclose(meshes['R18 C01'].extents,[207,100,158],atol=.02)
fig,axs=plt.subplots(1,2,figsize=(12,7),sharex=True,sharey=True)
for ax,(name,m) in zip(axs,meshes.items()):
    sec=m.section(plane_origin=[0,92,0],plane_normal=[0,1,0])
    for loop in sec.discrete:ax.plot(loop[:,0],loop[:,2],color='#365846',lw=1.4)
    ax.axhline(60,ls='--',color='royalblue');ax.axhline(77,ls=':',color='darkorange')
    ax.set(xlim=(84,134),ylim=(40,162),title=name,xlabel='x / mm');ax.set_aspect('equal');ax.grid(alpha=.2)
axs[0].set_ylabel('z / mm')
axs[0].annotate('Enclosed wire bore\nand crossover roof',(108,82),xytext=(87,135),arrowprops={'arrowstyle':'->'},fontsize=9)
axs[1].annotate('Open upwards:\nlay lead in from top',(100,105),xytext=(87,140),arrowprops={'arrowstyle':'->'},fontsize=9)
axs[1].annotate('Tube retained',(123,105),xytext=(117,65),arrowprops={'arrowstyle':'->'},fontsize=9)
fig.suptitle('Pump-wire route: actual STL section at y92 mm\nBlue: sump rim z60; orange: crossover floor z77',fontsize=12)
fig.tight_layout();fig.savefig(HERE/'before_after_section.png',dpi=160);plt.close(fig)

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(14,8))
for i,(name,m) in enumerate(meshes.items()):
    ax=fig.add_subplot(1,2,i+1,projection='3d')
    clipped=[]
    for triangle in m.triangles:
        polygon=list(triangle)
        for axis,minimum in [(0,86),(1,78),(2,40)]:
            result=[]
            for j,current in enumerate(polygon):
                previous=polygon[j-1]
                a=previous[axis]>=minimum; b=current[axis]>=minimum
                if a!=b:
                    fraction=(minimum-previous[axis])/(current[axis]-previous[axis])
                    result.append(previous+fraction*(current-previous))
                if b: result.append(current)
            polygon=result
            if not polygon: break
        for j in range(1,len(polygon)-1): clipped.append([polygon[0],polygon[j],polygon[j+1]])
    triangles=np.asarray(clipped)
    normals=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0])
    lengths=np.linalg.norm(normals,axis=1)
    normals=normals/np.maximum(lengths[:,None],1e-12)
    brightness=.45+.55*np.clip(normals @ np.array([.3,-.7,.6]),0,1)
    colours=np.column_stack([.43*brightness,.65*brightness,.48*brightness,np.ones(len(brightness))])
    coll=Poly3DCollection(triangles,facecolors=colours,edgecolor='none')
    ax.add_collection3d(coll)
    ax.set(xlim=(86,138),ylim=(78,103),zlim=(35,163),title=name+' - cropped actual STL',xlabel='x / mm',ylabel='y / mm',zlabel='z / mm')
    ax.set_box_aspect((52,25,128));ax.view_init(elev=24,azim=-62)
fig.tight_layout();fig.savefig(HERE/'before_after_route.png',dpi=150);plt.close(fig)
(HERE/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: independent STL topology, eight unchanged pilot sections, route support-area reduction and visuals',flush=True)
