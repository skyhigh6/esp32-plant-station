from pathlib import Path
import sys,zipfile,re,math,json
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path('.build/r18_source_audit');targets=[84.7,87.7]
def parse(name):
 with zipfile.ZipFile(out/(name+'_sliced.3mf')) as z:lines=z.read('Metadata/plate_1.gcode').decode().splitlines()
 pos=np.zeros(3);feature='Unknown';relative=False;old_e=0;paths={z:[] for z in targets};counts={z:{} for z in targets};roi_support=0;z_support={}
 for line in lines:
  if line.startswith('; FEATURE: '):feature=line[11:].strip();continue
  code=line.split(';')[0].strip();tok=code.split()
  if not tok:continue
  cmd=tok[0];p={k:float(v) for k,v in re.findall(r'([XYZIJE])(-?(?:\d*\.\d+|\d+\.?\d*))',code)}
  if cmd=='M83':relative=True
  elif cmd=='M82':relative=False
  elif cmd=='G92' and 'E'in p:old_e=p['E']
  elif cmd in ['G0','G1','G2','G3']:
   new=pos.copy()
   for k,i in zip('XYZ',range(3)):
    if k in p:new[i]=p[k]
   ev=p.get('E');de=ev if relative else ev-old_e if ev is not None else 0
   if ev is not None:old_e=old_e+ev if relative else ev
   if de and de>0 and ('X'in p or 'Y'in p) and feature!='Custom':
    if cmd in ['G2','G3'] and 'I'in p and 'J'in p:
     centre=pos[:2]+[p['I'],p['J']];r=np.linalg.norm(pos[:2]-centre);start=math.atan2(pos[1]-centre[1],pos[0]-centre[0]);end=math.atan2(new[1]-centre[1],new[0]-centre[0]);d=(end-start)%(2*math.pi)
     if cmd=='G2':d=d-2*math.pi
     ang=np.linspace(start,start+d,10);xy=centre+np.column_stack((np.cos(ang),np.sin(ang)))*r
    else:xy=np.vstack((pos[:2],new[:2]))
    xy=xy-[24.49999,77.99999];mid=xy.mean(axis=0);zz=float(new[2])
    inside=(106.5<=mid[0]<=114 and 82<=mid[1]<=96 and 52<=zz<=129) or (89<=mid[0]<=114 and 88<=mid[1]<=96 and 77<=zz<=159)
    if feature.startswith('Support') and inside:roi_support+=de;z_support[round(zz,2)]=z_support.get(round(zz,2),0)+de
    for target in targets:
     if abs(zz-target)<.02 and (xy[:,0].min()<133 and xy[:,0].max()>86 and xy[:,1].min()<100 and xy[:,1].max()>78):
      paths[target].append((xy,feature));counts[target][feature]=counts[target].get(feature,0)+1
   pos=new
 return paths,counts,roi_support,z_support
names=['baseline','candidate'];records={};fig,axes=plt.subplots(2,2,figsize=(10,8),layout='constrained')
for j,name in enumerate(names):
 paths,counts,roi,zs=parse(name);records[name]={'layer_extrusion_move_counts':counts,'declared_region_support_filament_mm_midpoint_metric':roi,'declared_region_support_layers_mm':zs}
 for i,target in enumerate(targets):
  ax=axes[i,j]
  for xy,feature in paths[target]:
   colour='#f49a24' if feature=='Support' else '#d12727' if feature=='Support interface' else '#66717a'
   ax.plot(xy[:,0],xy[:,1],color=colour,lw=.7 if feature.startswith('Support') else .4,alpha=.8)
  ax.plot([89,114,114,89,89],[88,88,96,96,88],color='#2084b8',ls='--',lw=1.2)
  ax.set(xlim=(86,133),ylim=(78,100),aspect='equal',title=f'{name.title()} — z {target:.1f} mm',xlabel='Source x (mm)',ylabel='Source y (mm)');ax.grid(alpha=.15)
fig.suptitle('Upright slice comparison around pump-wire route\nGrey: part; orange: support; red: support interface; dashed: top-route cut boundary',fontsize=12)
fig.savefig(out/'route_layer_comparison.png',dpi=160)
(out/'route_layer_evidence.json').write_text(json.dumps(records,indent=2));print({k:{'region_support_filament_mm':v['declared_region_support_filament_mm_midpoint_metric'],'support_layer_count':len(v['declared_region_support_layers_mm']),'selected_layer_counts':v['layer_extrusion_move_counts']} for k,v in records.items()})
