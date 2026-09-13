"""Actual exported STL section with a schematic cable centreline; millimetres."""
from pathlib import Path
import sys
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[1]/'.tools/cad-runtime'))
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig,ax=plt.subplots(figsize=(12,8))
for name,colour in [('tower_sump_body','#304d42'),('planter_sage','#8d9860')]:
    mesh=trimesh.load_mesh(OUT/'stl'/(name+'.stl'))
    section=mesh.section(plane_origin=[0,90.5,0],plane_normal=[0,1,0])
    assert section is not None
    for i,loop in enumerate(section.discrete):
        ax.plot(loop[:,0],loop[:,2],color=colour,lw=1.5,label=name.replace('_',' ') if i==0 else None)
ax.plot([184,184,85],[20,81,81],color='#c56b13',lw=3,label='Cable route (schematic centreline)')
ax.annotate('',xy=(85,81),xytext=(135,81),arrowprops=dict(arrowstyle='->',color='#c56b13',lw=3))
ax.plot([110,200],[60,60],'--',color='#24628b',lw=1,label='Sump rim z = 60 mm')
ax.annotate('Open trough floor z = 77 mm\n17 mm above sump rim',xy=(145,77),xytext=(120,127),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.annotate('Cable rises on sump side\nbefore crossing wall',xy=(184,68),xytext=(136,35),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.annotate('Wet/dry wall retained\nNo hole below rim',xy=(104,34),xytext=(20,35),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.text(6,168,'R10 · Cable route section at y = 90.5 mm',fontsize=16,weight='bold')
ax.text(6,158,'Actual STL outlines · orange cable path is illustrative, not a bend-radius proof',fontsize=10)
ax.set(xlim=(-3,213),ylim=(-4,176),xlabel='x / mm',ylabel='z / mm')
ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(loc='lower center',bbox_to_anchor=(.5,-.22),ncol=2)
fig.text(.12,.015,'Maximum fill level, cable jacket, connector size and minimum bend radius: UNKNOWN. No water-level approval.',fontsize=10)
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(OUT/'cable_section.png',dpi=170);plt.close(fig)
print('PASS: cable section drawn from final exported STL outlines')
