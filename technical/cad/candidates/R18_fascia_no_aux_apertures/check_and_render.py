"""Inspect the exported fascia mesh and actual plate sections, without CAD."""
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
from matplotlib.patches import Polygon
from matplotlib.path import Path as PlotPath

files={'R17 fascia':ROOT/'technical/print/main_parts/stl/fascia_charcoal.stl',
       'R18 C02 fascia':HERE/'exports/fascia_no_aux_apertures_r18_c02.stl'}
models={name:trimesh.load_mesh(p) for name,p in files.items()}
retained=[(x,72,12) for x in (24,48,72)]+[(32,48,7)]
retained += [(x,z,3.4) for x,z in [(9,10),(87,10),(9,148),(87,148)]]
retained += [(x,z,3) for x,z in [(10.5,97),(85.5,97),(10.5,128),(85.5,128)]]
obsolete=[(x,88,5) for x in (24,48,72)]+[(67,45,4)]
report={'units':'mm','sections_y_mm':2.5,'retained_circles':{},'obsolete_centres_solid':{},'meshes':{}}
sections={}
for name,m in models.items():
    incidence=np.bincount(m.edges_unique_inverse)
    assert m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1
    assert np.all(incidence==2) and not np.any(m.area_faces<1e-10)
    report['meshes'][name]={'sha256':hashlib.sha256(files[name].read_bytes()).hexdigest(),'closed':True,'winding':True,'components':1,'all_edges_two_faces':True,'degenerate_faces':0,'bounds_mm':m.bounds.tolist(),'volume_mm3':float(m.volume)}
    sec=m.section(plane_origin=[0,2.5,0],plane_normal=[0,1,0])
    loops=[a[:,[0,2]] for a in sec.discrete]
    sections[name]=loops
    circles=[]
    for x,z,d in retained:
        found=[]
        for loop in loops:
            r=np.linalg.norm(loop-[x,z],axis=1)
            if np.max(np.abs(r-d/2))<.025:found.append([float(r.min()),float(r.max())])
        assert len(found)==1,(name,x,z,d,found)
        circles.append({'centre_xz_mm':[x,z],'diameter_mm':d,'radius_range_mm':found[0]})
    report['retained_circles'][name]=circles
    solid=[]
    for x,z,d in obsolete:
        inside=sum(PlotPath(loop).contains_point((x,z)) for loop in loops)%2==1
        assert inside==(name=='R18 C02 fascia'),(name,x,z,inside)
        solid.append({'centre_xz_mm':[x,z],'solid_at_section':bool(inside)})
    report['obsolete_centres_solid'][name]=solid
    # Rectangular display aperture retains its measured mesh-section envelope.
    matches=[]
    for loop in loops:
        low=loop.min(axis=0); high=loop.max(axis=0)
        if np.allclose((low+high)/2,[48,112.5],atol=.01) and np.allclose(high-low,[71.4,24.6],atol=.01):matches.append((high-low).tolist())
    assert len(matches)==1
    report.setdefault('display_aperture_mm',{})[name]=matches[0]
assert np.allclose(models['R17 fascia'].bounds,models['R18 C02 fascia'].bounds,atol=.002)

fig,axs=plt.subplots(1,2,figsize=(9,9),sharex=True,sharey=True)
background='#f7f6f0'
for ax,(name,loops) in zip(axs,sections.items()):
    ax.set_facecolor(background)
    areas=[abs(np.dot(p[:-1,0],p[1:,1])-np.dot(p[1:,0],p[:-1,1]))/2 for p in loops]
    for i in np.argsort(areas)[::-1]:
        p=loops[i]
        other=sum(PlotPath(loop).contains_point(tuple(p[0])) for j,loop in enumerate(loops) if j!=i)
        colour='#444e50' if other%2==0 else background
        ax.add_patch(Polygon(p,facecolor=colour,edgecolor='#1f2526',linewidth=.65))
    for x in (24,48,72):ax.text(x,72,'Ø12',ha='center',va='center',fontsize=8)
    ax.text(48,112.5,'Display opening',ha='center',va='center',fontsize=9)
    if name=='R17 fascia':
        ax.annotate('Standalone LEDs',(48,88),xytext=(48,92),ha='center',color='#b64514',fontsize=9)
        ax.annotate('Speaker bore',(67,45),xytext=(53,30),color='#b64514',fontsize=9,arrowprops={'arrowstyle':'->','color':'#b64514'})
    else:
        ax.annotate('LED positions closed',(48,88),xytext=(48,92),ha='center',color='#efeee8',fontsize=9)
        ax.annotate('Speaker position closed',(67,45),xytext=(40,30),color='#efeee8',fontsize=9,arrowprops={'arrowstyle':'->','color':'#efeee8'})
    ax.set(xlim=(0,96),ylim=(0,158),title=name,xlabel='x / mm');ax.set_aspect('equal')
axs[0].set_ylabel('z / mm')
fig.suptitle('Fascia before / after — actual exported STL plate section at y2.5 mm\nThree button apertures, display, knob and fixing holes retained',fontsize=11)
fig.tight_layout();fig.savefig(HERE/'before_after_fascia.png',dpi=180);plt.close(fig)
(HERE/'independent_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: four plate closures, 12 retained circles, display and bounds; mesh topology and preview',flush=True)
