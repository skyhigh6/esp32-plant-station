from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import cadquery as cq
b=cq.importers.importStep('technical/cad/candidates/R18_open_pump_route/exports/tower_open_pump_route_r18_c01.step').val()
def bx(lo,hi):return cq.Solid.makeBox(*[y-x for x,y in zip(lo,hi)],cq.Vector(*lo))
checks={
'front_approach_above_rim':((108,70,61),(113,94,128)),
'short_sump_side_above_rim':((108,90,61),(114.1,94,128)),
'short_sump_side_below_rim':((108,90,53),(114.1,94,60)),
'bottom_sump_access_near_front':((108,82,53),(150,86,60)),
'front_approach_low':((108,70,53),(113,94,60)),
'below_rim_connection_forward_of_tube':((110,82,53),(130,86,60))}
r={k:b.intersect(bx(*v)).Volume() for k,v in checks.items()};print(json.dumps(r,indent=2),flush=True);Path('.build/r18_source_audit/candidate_access_checks.json').write_text(json.dumps(r,indent=2))
