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
    section=mesh.section(plane_origin=[0,92,0],plane_normal=[0,1,0])
    assert section is not None
    for i,loop in enumerate(section.discrete):
        ax.plot(loop[:,0],loop[:,2],color=colour,lw=1.5,label=name.replace('_',' ') if i==0 else None)
ax.plot([110,110,85],[30,81,81],color='#c56b13',lw=3,label='Pump wires (schematic centreline)')
ax.plot([123,123],[30,146],color='#24628b',lw=4,label='Water tube (schematic centreline)')
ax.annotate('',xy=(85,81),xytext=(110,81),arrowprops=dict(arrowstyle='->',color='#c56b13',lw=3))
ax.plot([110,200],[60,60],'--',color='#24628b',lw=1,label='Sump rim z = 60 mm')
ax.annotate('Crossover bottom z = 77 mm\n17 mm above sump rim',xy=(103,77),xytext=(122,127),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.annotate('Shared sump-side intake\nSeparate tube and wire passages',xy=(123,35),xytext=(135,40),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.annotate('Wet/dry wall retained\nNo hole below rim',xy=(104,34),xytext=(20,35),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.text(6,168,'R12 · Cable route section at y = 92 mm',fontsize=16,weight='bold')
ax.text(6,158,'Actual STL outlines · orange cable path is illustrative, not a bend-radius proof',fontsize=10)
ax.set(xlim=(-3,213),ylim=(-4,176),xlabel='x / mm',ylabel='z / mm')
ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(loc='lower center',bbox_to_anchor=(.5,-.22),ncol=2)
fig.text(.12,.015,'Maximum fill level, cable jacket, connector size and minimum bend radius: UNKNOWN. No water-level approval.',fontsize=10)
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(OUT/'cable_section.png',dpi=170);plt.close(fig)
print('PASS: cable section drawn from final exported STL outlines')

# Cross-section through the transverse battery tie slot.
mesh=trimesh.load_mesh(OUT/'stl/tower_sump_body.stl')
section=mesh.section(plane_origin=[48,0,0],plane_normal=[1,0,0])
assert section is not None
fig,ax=plt.subplots(figsize=(10,5))
for loop in section.discrete:
    ax.plot(loop[:,1],loop[:,2],color='#304d42',lw=2)
ax.plot([28,62],[8.25,8.25],color='#c56b13',lw=2)
ax.annotate('Tie tunnel: 6 wide x 2.5 high',xy=(45,8.25),xytext=(32,2),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.annotate('Holder seats at z12',xy=(45,12),xytext=(34,26),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.set(xlim=(22,68),ylim=(0,30),xlabel='y / mm',ylabel='z / mm',title='R12 battery saddle: actual STL section at x48 mm')
ax.set_aspect('equal');ax.grid(alpha=.15);fig.tight_layout();fig.savefig(OUT/'battery_tie_section.png',dpi=170);plt.close(fig)
print('PASS: battery tie slot section drawn from final STL')

# Sensor entry plane, separate from the tube riser section.
mesh=trimesh.load_mesh(OUT/'stl/tower_sump_body.stl')
section=mesh.section(plane_origin=[93,0,0],plane_normal=[1,0,0])
fig,ax=plt.subplots(figsize=(8,8))
for loop in section.discrete:
    ax.plot(loop[:,1],loop[:,2],color='#304d42',lw=1.5)
ax.axhline(116,color='#8d9860',ls='--',label='Planter top z116 (reference)')
ax.annotate('8 mm sensor entry\ncentre y65 / z128\nLowest edge 8 mm above planter',xy=(65,128),xytext=(10,175),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.set(xlim=(-5,105),ylim=(90,190),xlabel='y / mm',ylabel='z / mm',title='R12 moisture sensor entry: actual STL section at x93')
ax.set_aspect('equal');ax.legend(loc='lower left');ax.grid(alpha=.15);fig.tight_layout();fig.savefig(OUT/'sensor_entry_section.png',dpi=170);plt.close(fig)
print('PASS: sensor entry section drawn from final STL')
