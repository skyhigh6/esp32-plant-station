from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('.tools/cad-runtime').resolve()))
import cadquery as cq
out=Path('.build/r18_source_audit');base=Path('technical/print/main_parts/step/tower_sump_body_uno_ports_r17.step');cand=Path('technical/cad/candidates/R18_open_pump_route/exports/tower_open_pump_route_r18_c01.step')
def box(lo,hi):return cq.Solid.makeBox(*[b-a for a,b in zip(lo,hi)],cq.Vector(*lo))
a=cq.importers.importStep(str(base)).val();b=cq.importers.importStep(str(cand)).val();removed=a.cut(b);added=b.cut(a)
mask=box((106.5,82,52),(114,96,129)).fuse(box((89,88,77),(114,96,159)))
report={'baseline_valid':a.isValid(),'candidate_valid':b.isValid(),'candidate_solid_count':len(b.Solids()),'removed_volume_mm3':removed.Volume(),'added_volume_mm3':added.Volume(),'removed_outside_declared_cutters_mm3':removed.cut(mask).Volume()}
regions={
'all_geometry_left_of_route':((-1,-1,-1),(89,101,159)),
'all_geometry_right_of_route':((114,-1,-1),(208,101,159)),
'rear_wall_band':((-1,96,-1),(208,101,159)),
'sump_floor_and_low_wall':((-1,-1,-1),(208,101,52)),
'below_rim_remaining_partition':((96,-1,4),(106.5,101,60)),
'left_usb_and_dc_ports':((-1,20,96),(7,80,120)),
'lid_fixing_rear_right':((89,81,151),(96,88,159))}
report['preserved_regions_removed_volume_mm3']={k:removed.intersect(box(*v)).Volume() for k,v in regions.items()}
free={
'lay_in_from_sump_side_lower':((108,90,53),(150,94,60)),
'lay_in_from_sump_side_upper':((108,90,61),(150,94,128)),
'vertical_route':((108,90,53),(113,94,128)),
'crossing_to_dry_tower':((90,90,78),(113,94,85)),
'crossing_top_access':((90,90,78),(113,94,159))}
report['free_corridor_solid_overlap_mm3']={k:b.intersect(box(*v)).Volume() for k,v in free.items()}
# Verify retained shelf and dry wall as actual material rather than just absence of a difference.
solid_probes={'crossing_floor':((96,89,76),(105,95,77)),'back_wall':((96,97,78),(113,99,150)),'below_rim_partition':((102,20,10),(105,80,59))}
report['retained_material_probe_missing_mm3']={k:box(*v).cut(b).Volume() for k,v in solid_probes.items()}
# Actual coupon is a rigid translation of the same cropped body, with no added material.
trial=cq.importers.importStep('technical/cad/candidates/R18_open_pump_route/exports/route_trial_r18_c01.step').val().translate((88,80,70));expected=b.intersect(box((88,80,70),(117,100,130)))
report['coupon_symmetric_difference_mm3']=trial.cut(expected).Volume()+expected.cut(trial).Volume()
(out/'candidate_step_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
