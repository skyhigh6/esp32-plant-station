from pathlib import Path
import zipfile,re,json,math,xml.etree.ElementTree as ET
out=Path('.build/r18_source_audit')
def scan(name):
 with zipfile.ZipFile(out/(name+'_sliced.3mf')) as z:
  gc=z.read('Metadata/plate_1.gcode').decode();info=ET.fromstring(z.read('Metadata/slice_info.config'))
  plate=info.find('plate');met={e.attrib.get('key'):e.attrib.get('value') for e in plate.findall('metadata')};warnings=[e.attrib for e in plate.findall('warning')]
  settings=json.loads(z.read('Metadata/project_settings.config'))
 lines=gc.splitlines();feature='Unknown';relative=False;old_e=0;stats={};pos={'X':0.,'Y':0.,'Z':0.};arc_support=0
 for line in lines:
  if line.startswith('; FEATURE: '):feature=line[11:].strip();continue
  code=line.split(';')[0].strip(); toks=code.split()
  if not toks:continue
  cmd=toks[0];pars={k:float(v) for k,v in re.findall(r'([XYZE])(-?(?:\d*\.\d+|\d+\.?\d*))',code)}
  if cmd=='M83':relative=True
  elif cmd=='M82':relative=False
  elif cmd=='G92' and 'E'in pars:old_e=pars['E']
  elif cmd in ['G0','G1','G2','G3']:
   ev=pars.get('E');de=ev if relative else ev-old_e if ev is not None else 0
   if ev is not None:old_e=old_e+ev if relative else ev
   if de is not None and de>0 and ('X'in pars or 'Y'in pars):
    v=stats.setdefault(feature,{'deposited_filament_length_mm':0.,'extruding_moves':0,'min_z':9999.,'max_z':-9999.})
    v['deposited_filament_length_mm']+=de;v['extruding_moves']+=1;v['min_z']=min(v['min_z'],pos['Z']);v['max_z']=max(v['max_z'],pos['Z'])
    if feature.startswith('Support') and cmd in ['G2','G3']:arc_support+=1
   for k in pos:
    if k in pars:pos[k]=pars[k]
 diameter=float(settings['filament_diameter'][0]);density=float(settings['filament_density'][0]);area=math.pi*(diameter/2)**2
 for v in stats.values():v['deposited_volume_mm3']=v['deposited_filament_length_mm']*area;v['estimated_mass_g']=v['deposited_volume_mm3']/1000*density
 support={k:v for k,v in stats.items() if k.startswith('Support')};se=sum(v['deposited_filament_length_mm'] for v in support.values())
 log=(out/(name+'_slice.log')).read_text();errs=[l for l in log.splitlines() if '[error]' in l];warns=[l for l in log.splitlines() if '[warning]' in l]
 return {'name':name,'metadata':met,'warnings':warnings,'stored_filament_diameter_mm':diameter,'stored_filament_density_g_cm3':density,'support_features':support,'support_filament_length_mm':se,'support_volume_mm3':se*area,'support_estimated_mass_g':se*area/1000*density,'support_arc_moves':arc_support,'slicer_log_error_count':len(errs),'slicer_log_error_examples':sorted(set(re.sub(r'^.*\[error\]\s*','',e) for e in errs))[:6],'slicer_log_warning_examples':sorted(set(re.sub(r'^.*\[warning\]\s*','',e) for e in warns))[:6]}
a=scan('baseline');b=scan('candidate')
r={'baseline':a,'candidate':b,'support_reduction_percent':100*(1-b['support_volume_mm3']/a['support_volume_mm3']),'support_reduction_mm3':a['support_volume_mm3']-b['support_volume_mm3'],'support_reduction_estimated_mass_g':a['support_estimated_mass_g']-b['support_estimated_mass_g'],'method':'Parse feature-tagged G0/G1/G2/G3 XY motion with positive commanded E extrusion, respecting M82/M83/G92. Support + Support interface. Excludes retractions and E-only primes; material volume uses stored filament diameter and density. Comparative commanded deposition, not observed consumption.','limitations':['No physical print performed','Stored user profile produces bed_temperature_too_high_than_filament warning in both slices; profile is not accepted for printing','Slicer logs emit ZFiller errors in both despite exit 0; comparative result needs layer review before manufacture']}
(out/'slice_comparison.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
