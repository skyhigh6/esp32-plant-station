"""Plant Station R10. Millimetres; x right, y rear, z up. Run with local cad-runtime."""
from pathlib import Path
import sys, json, itertools, hashlib
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.tools/cad-runtime'))
import cadquery as cq
import trimesh
import numpy as np
OUT = Path(__file__).parent
(OUT/'stl').mkdir(parents=True, exist_ok=True)
(OUT/'step').mkdir(exist_ok=True)
V=cq.Vector

# User-specified holes; other component envelopes remain provisional.
BUTTON_HOLE_MM = 12.0
BUTTON_HOLE_ALLOWANCE_MM = 0.0
BUTTON_NUT_OD_MM = 20.0
BUTTON_REAR_DEPTH_MM = 35.0
SUMP_HEIGHT_MM = 60.0
SUMP_FLOOR_MM = 4.0
PUMP_LWH_MM = (38.5, 25.5, 43.0)  # shortlisted COM3700, not measured hardware
PUMP_CLEARANCE_MM = 3.0
HOSE_OD_MM = 8.0
HOSE_DIAMETRAL_ALLOWANCE_MM = 0.4
PLANT_LIFT_MM = SUMP_HEIGHT_MM - 40.0
PCB_SIZE_MM = (67.0,64.0)  # SunFounder dimensioned carrier drawing
PCB_CENTRES_MM = (60.0,57.0)
LCD_SIZE_MM = (80.0,36.0)  # user's primary annotated LCD image
LCD_CENTRES_MM = (75.0,31.0)
LCD_BEZEL_MM = (71.0,24.2)
LCD_BEZEL_ALLOWANCE_MM = 0.4  # diametral, 0.2 each side
LCD_APERTURE_MM = tuple(d+LCD_BEZEL_ALLOWANCE_MM for d in LCD_BEZEL_MM)
LCD_APERTURE_XZ = (48-LCD_APERTURE_MM[0]/2,112.5-LCD_APERTURE_MM[1]/2)
# Compact provisional left port opening. Measure actual two plugs before tower print.
USB_YZ = (49.0, 98.5)
USB_WH = (28.0, 20.0)  # y width, z height; stacked carrier/module connectors
PIEZO_DIAMETER_MM = 10.0
PIEZO_SEAT_MM = 10.4
KNOB_BORES = [('round_5p0',5.0,None),('round_5p2',5.2,None),
              ('round_6p0',6.0,None),('round_6p2',6.2,None),
              ('round_6p35',6.35,None),('round_6p55',6.55,None),
              ('D_6p0',6.0,1.5),('D_6p2',6.2,1.6)]
assert SUMP_HEIGHT_MM - SUMP_FLOOR_MM - 3 > PUMP_LWH_MM[2] + PUMP_CLEARANCE_MM
assert BUTTON_NUT_OD_MM < 24.0, 'Button nuts exceed 24 mm centre spacing'
def box(x,y,z,dx,dy,dz): return cq.Solid.makeBox(dx,dy,dz,V(x,y,z))
def rounded(x,y,z,dx,dy,dz,r=5,axis='Z'):
    return cq.Workplane('XY').newObject([box(x,y,z,dx,dy,dz)]).edges('|'+axis).fillet(r).val()
def cyl(x,y,z,r,h,axis=(0,0,1)): return cq.Solid.makeCylinder(r,h,V(x,y,z),V(*axis))
def fuse(a,*bs):
    for b in bs: a=a.fuse(b)
    return a.clean()
def cut(a,*bs):
    for b in bs: a=a.cut(b)
    return a.clean()
def dovetail(y,z,h,clear=0):
    pts=[(95.5,y-3-clear),(96,y-3-clear),(100+clear,y-5-clear),(100+clear,y+5+clear),(96,y+3+clear),(95.5,y+3+clear)]
    return cq.Workplane('XY').polyline(pts).close().extrude(h).translate((0,0,z)).val()

# Measured interfaces; dimensions independent of the concept illustration.
# 90 degrees anticlockwise viewed from fascia: (x,z)->(48-(z-108.5),108.5+(x-48)).
PCB=[(19.5,78.5),(76.5,78.5),(19.5,138.5),(76.5,138.5)] # USB faces LEFT
LCD=[(10.5,97),(85.5,97),(10.5,128),(85.5,128)]
FAST=[(9,10),(87,10),(9,148),(87,148)]
cavity=rounded(6,8,6,84,86,153,2)
cavity=cq.Workplane('XY').newObject([cavity]).edges('<Z').fillet(1).val()
tower=cut(rounded(0,0,0,96,100,158,7),cavity,box(6,-1,6,84,12,148),rounded(3,-1,3,90,5,152,3,'Y'))
tower=cq.Workplane('XY').newObject([tower]).edges('>Z or <Z').fillet(0.5).val()
tower=cq.Workplane('XY').newObject([tower]).edges('<Y').fillet(0.3).val()
# Fill the relieved edge behind each boss. Upper webs have a 45-degree lower edge
# and overlap the side wall by 2 mm; no near-tangent attachment remains.
for side in ('left','right'):
    pts=[(4,133),(14,143),(14,158),(4,158)]
    if side=='right': pts=[(96-x,z) for x,z in pts]
    web=cq.Workplane('XZ',origin=(0,13,0)).polyline(pts).close().extrude(9).val()
    web=cq.Workplane('XY').newObject([web]).edges('|Y').fillet(0.6).val()
    lower=rounded(4 if side=='left' else 82,4,6,10,9,9,0.6,'Y')
    tower=fuse(tower,web,lower)
for x,z in FAST:
    tower=fuse(tower,cyl(x,4,z,5,9,(0,1,0)))
    tower=cut(tower,cyl(x,3,z,1.4,11,(0,1,0)))
# Rear-integrated board standoffs, inserted via full front opening.
for x,z in PCB:
    boss=cq.Workplane('XY').newObject([cyl(x,76,z,4,19,(0,1,0))]).edges('<Y').chamfer(0.3).val()
    tower=fuse(tower,boss)
    roots=[e for e in tower.Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y-94)<1e-5 and abs(e.Center().x-x)<1e-5 and abs(e.Center().z-z)<1e-5 and abs(e.radius()-4)<1e-5]
    assert len(roots)==1, 'Missing board boss root'
    tower=tower.fillet(0.6,roots)
    tower=cut(tower,cyl(x,75,z,1.4,12,(0,1,0)))
# Small side aperture, through the left wall only. No top service opening.
tower=cut(tower,box(-1,USB_YZ[0],USB_YZ[1],8,*USB_WH))
usb_edges=[e for e in tower.Edges() if e.geomType()=='LINE' and (abs(e.Center().x)<1e-5 or abs(e.Center().x-6)<1e-5) and 48.9<=e.Center().y<=77.1 and 98.4<=e.Center().z<=118.6]
assert len(usb_edges)==8, 'USB edge selection changed'
tower=tower.chamfer(0.3,None,usb_edges)
for y in (25,75):
    tower=fuse(tower,dovetail(y,6,29),box(95,17 if y==25 else 67,0,5.8,16,3))
# Battery tray locating/fixing pads on dry floor, blind pilots.
for x in (18,78):
    pad=cq.Workplane('XY').newObject([cyl(x,45,5,4,4)]).edges('>Z').chamfer(0.3).val()
    tower=fuse(tower,pad)
    roots=[e for e in tower.Edges() if e.geomType()=='CIRCLE' and abs(e.Center().z-6)<1e-5 and abs(e.Center().x-x)<1e-5 and abs(e.Center().y-45)<1e-5 and abs(e.radius()-4)<1e-5]
    assert len(roots)==1, 'Missing floor pad root'
    tower=tower.fillet(0.6,roots)
    tower=cut(tower,cyl(x,45,4,1.4,6))
parts={'tower_sage':tower}
panel=rounded(3.4,1,3.4,89.2,3,151.2,3,'Y')
panel=cut(panel,box(LCD_APERTURE_XZ[0],0,LCD_APERTURE_XZ[1],LCD_APERTURE_MM[0],6,LCD_APERTURE_MM[1]))
for x,z in FAST: panel=cut(panel,cyl(x,0,z,1.7,6,(0,1,0)))
for x in (24,48,72):
    panel=cut(panel,cyl(x,0,72,(BUTTON_HOLE_MM+BUTTON_HOLE_ALLOWANCE_MM)/2,6,(0,1,0)),cyl(x,0,88,2.5,6,(0,1,0)))
panel=cut(panel,cyl(32,0,48,3.5,6,(0,1,0)))
# 10 mm piezo glued around its perimeter, sound face against the fascia.
panel=cut(panel,cyl(67,0,45,2.0,6,(0,1,0)))
panel=fuse(panel,cut(cyl(67,3.8,45,7.2,3.2,(0,1,0)),
                    cyl(67,3.7,45,PIEZO_SEAT_MM/2,3.5,(0,1,0))))
# LED collars support a glue fillet; the front bores remain nominal 5 mm.
for x in (24,48,72):
    panel=fuse(panel,cut(cyl(x,3.8,88,4,2.2,(0,1,0)),cyl(x,3.7,88,2.7,2.5,(0,1,0))))
# 8 mm PCB stand-off is an unmeasured depth allowance; 6 OD / 3 bore pads.
for x,z in LCD:
    panel=fuse(panel,cyl(x,3.5,z,3,8.5,(0,1,0)))
    panel=cut(panel,cyl(x,0,z,1.5,13,(0,1,0)))
parts['fascia_charcoal']=panel
lid=rounded(0,0,158,96,100,3,7)

# Screw-down top cover with blind shell pilots; corner walls retained.
for x in (3.5,92.5):
    for y in (15,85):
        lid=cut(lid,cyl(x,y,157,1.7,5))
        tower=cut(tower,cyl(x,y,151,1.4,8))
parts['tower_sage']=tower
parts['top_cover_sage']=lid
sump=cut(rounded(101,0,0,106,100,SUMP_HEIGHT_MM,7),rounded(107,6,SUMP_FLOOR_MM,94,88,SUMP_HEIGHT_MM,3))
for y in (25,75):
    collar=box(96, y-9,3,10,18,35)
    collar=cut(collar,dovetail(y,2.9,36,0.4))
    sump=fuse(sump,collar)
parts['sump_charcoal']=sump
# Removable planting insert seats directly on sump rim, no concealed deck.
plant=fuse(rounded(102,1,40,104,98,4,6),rounded(106,15,43,96,70,51,5))
# Full-height outer skirt follows the concept silhouette without solid thick walls.
skirt=cut(rounded(102,1,43,104,98,51,6),rounded(105,4,42,98,92,50,3))
plant=fuse(plant,skirt)
plant=cut(plant,rounded(109,20,44,90,60,52,3))
# Locating lip enters sump with 0.4 mm nominal clearance on every side.
lip=cut(rounded(107.4,6.4,37,93.2,87.2,4,3.4),rounded(110.4,9.4,36,87.2,81.2,6,3))
plant=fuse(plant,lip)
# Rear service notch for provisional tube and pump cable; outside soil cavity.
plant=cut(plant,box(178,84,36,18,18,80))
for x in (129,175):plant=cut(plant,cyl(x,50,39,3,7))
plant=plant.translate((0,0,PLANT_LIFT_MM))
parts['planter_sage']=plant
# Open-ended holder tray: 72mm usable length, 22mm between side rails.
battery=box(12,30,9,72,30,3)
battery=fuse(battery,box(12,30,12,72,4,9),box(12,56,12,72,4,9))
for x in (18,78):battery=cut(battery,cyl(x,45,8,1.7,5))
parts['battery_tray']=battery
# Exterior hose clips keep the water line out of the dry enclosure.
clip=box(96,84,136,8,14,4)
clip=fuse(clip,cyl(108,91,136,6,4))
clip=cut(clip,cyl(108,91,135,(HOSE_OD_MM+HOSE_DIAMETRAL_ALLOWANCE_MM)/2,6),box(111,89,135,5,4,6),cyl(100,91,135,1.7,6))
# Mount on tower right upper wall using blind vertical pilot in shell rim/arm.
# Separate clamp screws into a solid external shelf, no water passage.
shelf=cq.Workplane('XY').newObject([box(95,84,132,9,14,4)]).edges().chamfer(0.3).val()
tower=fuse(parts['tower_sage'],shelf)
tower=cut(tower,cyl(100,91,133,1.4,4))
parts['tower_sage']=tower
parts['hose_clip']=clip


# R10: one structural base; retain both water-containing walls below the rim.
# Provisional 4 mm cable, laid into an open internal trough before planter fit.
CABLE_OD_MM=4.0
CABLE_ROUTE_CENTRE_YZ=(90.5,81.0)
bridge=box(94,8,0,13,84,56)
trough=cut(box(94,85.5,74,98,10,12),box(93,87.5,77,100,6,10))
# Sump-side rise opening is above the rim; it never pierces the wet/dry wall.
trough=cut(trough,cyl(184,90.5,73,4,15))
combined=fuse(tower,sump,bridge,trough)
combined=cut(combined,cyl(89,90.5,81,4,13,(1,0,0)))
# Open-topped relief lets the planter lift vertically off the fixed trough.
plant=cut(plant,box(101,85,56,92,11,70))
plant=cut(plant,box(101,84,56,4,17,70))
# Retain the rear skirt as one solid via bridges above the fixed trough.
for x in (120,160):
    plant=fuse(plant,box(x,82,110,6,16,4))
parts.pop('tower_sage');parts.pop('sump_charcoal')
parts['tower_sump_body']=combined
parts['planter_sage']=plant
# Keep existing tower-specific probes pointed at the revised full body.
tower=combined


def verify():
    report={'revision':'R10','units':'mm','cadquery':cq.__version__,'parts':{},'pairwise':[],'critical':{}}
    for name,sh in parts.items():
        assert sh.isValid(),name+' invalid CAD'
        assert len(sh.Solids())==1,(name,'solid count',len(sh.Solids()))
        p=OUT/'stl'/f'{name}.stl'
        cq.exporters.export(sh,str(p),tolerance=.025,angularTolerance=.1)
        cq.exporters.export(sh,str(OUT/'step'/f'{name}.step'))
        m=trimesh.load_mesh(p,process=True)
        rec={'bounds_mm':m.extents.tolist(),'closed':bool(m.is_watertight),'winding':bool(m.is_winding_consistent),'components':len(m.split()),'volume_mm3':float(m.volume),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        report['parts'][name]=rec
        assert rec['closed'] and rec['winding'] and rec['components']==1 and rec['volume_mm3']>0,(name,rec)
        print('EXPORTED',name,flush=True)
    # Real BRep intersections; failures raise, never silently count as zero.
    assert abs(box(0,0,0,10,10,10).intersect(box(5,0,0,10,10,10)).Volume()-500)<1e-6
    for (a,sa),(b,sb) in itertools.combinations(parts.items(),2):
        vol=sa.intersect(sb).Volume()
        report['pairwise'].append({'a':a,'b':b,'intersection_mm3':vol})
        print('PAIR',a,b,vol,flush=True)
        if vol>1e-5:
            (OUT/'verification.json').write_text(json.dumps(report,indent=2))
            raise ValueError(f'Interference {a}/{b}: {vol}')
    # Probe each required through-hole directly on solid; positive probe controls.
    for x,z in LCD+FAST:
        assert panel.intersect(cyl(x,0,z,1.0,6,(0,1,0))).Volume()<1e-7
    assert panel.intersect(box(LCD_APERTURE_XZ[0]+.01,0,LCD_APERTURE_XZ[1]+.01,LCD_APERTURE_MM[0]-.02,6,LCD_APERTURE_MM[1]-.02)).Volume()<1e-7
    for x in (129,175): assert plant.intersect(cyl(x,50,39+PLANT_LIFT_MM,2.5,7)).Volume()<1e-7
    assert sump.intersect(box(110,10,0,80,80,3)).Volume()>19000
    report['critical']={'integrated_body':True,'cable_route':{'provisional_cable_OD_mm':4,'trough_clear_width_mm':6,'trough_floor_z_mm':77,'sump_rim_z_mm':60,'crossing_min_z_mm':77,'water_level':'UNKNOWN - no approved maximum fill','connector_and_bend_radius':'UNKNOWN - route unterminated cable before planter installation'},'edge_treatment_mm':{'cavity_vertical':2,'cavity_floor':1,'rim_base':0.5,'front_edge':0.3,'support_profile':0.6,'standoff_root':0.6,'standoff_tip_chamfer':0.3},'upper_support_top_z_mm':158,'LCD_aperture_mm':LCD_APERTURE_MM,'LCD_centres_mm':LCD_CENTRES_MM,'PCB_reference_centres_mm':PCB_CENTRES_MM,'PCB_installed_centres_xz_mm':[57,60],'plant_cavity_mm':[90,60,50],'drains':2,'drain_diameter_mm':6,'floor_mm':4,'dovetail_clearance_mm':0.4,'through_probes':'PASS','floor_probe':'PASS','overlap_control_mm3':500}
    # Verify button bores plus retained wall immediately outside each bore.
    for x in (24,48,72):
        assert panel.intersect(cyl(x,0,72,5.99,6,(0,1,0))).Volume()<1e-7
        assert panel.intersect(cyl(x,1,72,6.2,3,(0,1,0))).Volume()>15
        nut=cyl(x,4.01,72,BUTTON_NUT_OD_MM/2,5,(0,1,0))
        rear=cyl(x,9.01,72,8,BUTTON_REAR_DEPTH_MM-5,(0,1,0))
        for name,sh in parts.items():
            assert nut.intersect(sh).Volume()<1e-6,('button nut clash',name)
            assert rear.intersect(sh).Volume()<1e-6,('button rear clash',name)
    # Pump body including 3 mm lateral/top allowance; floor remains the support datum.
    pump=box(143,27,SUMP_FLOOR_MM,*PUMP_LWH_MM)
    pump_clear=box(143-PUMP_CLEARANCE_MM,27-PUMP_CLEARANCE_MM,SUMP_FLOOR_MM+.01,
                   PUMP_LWH_MM[0]+2*PUMP_CLEARANCE_MM,PUMP_LWH_MM[1]+2*PUMP_CLEARANCE_MM,
                   PUMP_LWH_MM[2]+PUMP_CLEARANCE_MM-.01)
    for name,sh in parts.items():
        assert pump_clear.intersect(sh).Volume()<1e-6,('pump envelope clash',name)
    # Vertical hose/cable passage through the rear notch, away from the soil cavity.
    for probe in (cyl(184,90,54,4.2,65),cyl(192,90,54,2,65)):
        assert plant.intersect(probe).Volume()<1e-6,'rear service passage blocked'
    assert parts['hose_clip'].intersect(cyl(108,91,135,4.19,6)).Volume()<1e-6
    report['critical'].update({'button_holes_mm':[12,12,12],'button_centres_x_mm':[24,48,72],
        'button_centre_z_mm':72,'button_panel_thickness_mm':3,'sump_external_height_mm':SUMP_HEIGHT_MM,
        'sump_internal_depth_mm':SUMP_HEIGHT_MM-SUMP_FLOOR_MM,'pump_LWH_mm':list(PUMP_LWH_MM),
        'pump_allowance_mm':PUMP_CLEARANCE_MM,'pump_body_to_planter_underside_mm':13,
        'pump_body_to_lip_bottom_mm':10,'hose_clip_bore_mm':HOSE_OD_MM+HOSE_DIAMETRAL_ALLOWANCE_MM,
        'button_nut_envelope_OD_mm':BUTTON_NUT_OD_MM,'button_rear_envelope_depth_mm':BUTTON_REAR_DEPTH_MM,
        'new_envelope_checks':'PASS'})
    # Component envelopes are assumptions; hole centres remain measured inputs.
    pcb_envelope=box(16,44.4,75,64,31.6,67)
    lcd_envelope=box(8,12,94.5,80,21.6,36)
    for label,env in [('PCB',pcb_envelope),('LCD',lcd_envelope)]:
        for name,sh in parts.items():
            assert env.intersect(sh).Volume()<1e-6,(label,'envelope clash',name)
    usb_access=box(-10,USB_YZ[0]+.01,USB_YZ[1]+.01,26,USB_WH[0]-.02,USB_WH[1]-.02)
    for name,sh in parts.items():
        assert usb_access.intersect(sh).Volume()<1e-6,('USB lateral passage',name)
    assert lid.intersect(box(12,40,158.01,72,46,2.98)).Volume()>9800,'top opening not closed'
    for x in (7,84):
        assert tower.intersect(box(x,6,154,5,5,3)).Volume()>74.9, 'Upper gap not filled'
    for x in (5,83):
        assert tower.intersect(box(x,8,144,8,4,8)).Volume()>200,'boss web missing'
    assert panel.intersect(cyl(67,4.01,45,5.19,2.98,(0,1,0))).Volume()<1e-6
    assert panel.intersect(cyl(67,1,45,4.8,2,(0,1,0))).Volume()>110,'piezo seating floor missing'
    report['critical'].update({'PCB_outline_reference_mm':PCB_SIZE_MM,'PCB_installed_outline_xz_mm':[64,67],
        'LCD_outline_mm':LCD_SIZE_MM,'PCB_mount_coordinates_xz_mm':PCB,'LCD_mount_coordinates_xz_mm':LCD,
        'USB_orientation':'90 degrees anticlockwise from R7 viewed from fascia; both ports face left',
        'USB_left_opening_yz_mm':USB_YZ,'USB_left_opening_wh_mm':USB_WH,
        'USB_fit_status':'PROVISIONAL: connector offsets and plugs not measured',
        'top_cover':'solid 3 mm roof except four fixing holes',
        'upper_boss_webs':'9 mm deep, 10 mm wide, 45 degree lower edge; positive volume probes passed',
        'piezo_seat_ID_depth_mm':[10.4,3],'piezo_body_OD_user_mm':10,'piezo_sound_hole_mm':4,
        'LED_bores_mm':5,'LED_glue_collar_ID_mm':5.4})
    accesses=[]
    for x,z in PCB:
        # Front cover removed: driver access to the PCB fastener head.
        assert tower.intersect(cyl(x,13,z,3.5,62.9,(0,1,0))).Volume()<1e-6
        # Blind pilot remains open at the board seating face.
        assert tower.intersect(cyl(x,75.9,z,1.3,10,(0,1,0))).Volume()<1e-6
        accesses.append({'group':'PCB','x_mm':x,'z_mm':z,'driver_diameter_mm':7,'blind_pilot_depth_mm':11})
    aperture=box(LCD_APERTURE_XZ[0],-5,LCD_APERTURE_XZ[1],LCD_APERTURE_MM[0],24,LCD_APERTURE_MM[1])
    for x,z in LCD:
        assert panel.intersect(cyl(x,0,z,1.49,13,(0,1,0))).Volume()<1e-6
        assert aperture.intersect(cyl(x,-2,z,2.75,4,(0,1,0))).Volume()<1e-6
        accesses.append({'group':'LCD','x_mm':x,'z_mm':z,'stand_off_mm':8,'OD_mm':6,'through_hole_mm':3,'max_head_diameter_mm':5.5})
    for x,z in FAST:
        assert tower.intersect(cyl(x,-8,z,3,11.9,(0,1,0))).Volume()<1e-6
        accesses.append({'group':'fascia','x_mm':x,'z_mm':z,'front_driver_diameter_mm':6})
    for x in (18,78):
        probe=cyl(x,45,12.01,3.5,28)
        assert sum(sh.intersect(probe).Volume() for sh in parts.values())<1e-6
        accesses.append({'group':'battery','x_mm':x,'y_mm':45,'driver_diameter_mm':7})
    for x in (3.5,92.5):
        for y in (15,85):
            probe=cyl(x,y,161.01,3,20)
            assert sum(sh.intersect(probe).Volume() for sh in parts.values())<1e-6
            accesses.append({'group':'top_cover','x_mm':x,'y_mm':y,'driver_diameter_mm':6,'min_pilot_wall_mm':1.1})
    probe=cyl(100,91,140.01,3,20)
    assert sum(sh.intersect(probe).Volume() for sh in parts.values())<1e-6
    accesses.append({'group':'hose_clip','driver_diameter_mm':6,'blind_pilot_depth_mm':3})
    assert PCB[1][0]-PCB[0][0]==57 and PCB[2][1]-PCB[0][1]==60
    assert LCD[1][0]-LCD[0][0]==75 and LCD[2][1]-LCD[0][1]==31
    # Positive continuity probe in the former tower/sump gap.
    seam=box(96.1,10,1,4.8,80,54)
    assert abs(combined.intersect(seam).Volume()-seam.Volume())<1e-5
    # Connected cable test envelope: vertical rise, curved corner allowance,
    # horizontal crossing, then discharge inside tower. 4 mm cable provisional.
    route_probes=[cyl(184,90.5,45,2,36),cq.Solid.makeSphere(2,V(184,90.5,81)),cyl(85,90.5,81,2,99,(1,0,0))]
    for probe in route_probes:
        for name,sh in parts.items():
            assert sh.intersect(probe).Volume()<1e-5,('cable route blocked',name)
    # Wall strip stays solid from floor to full rim: no submerged wet/dry hole.
    barrier=box(102,10,4,4,80,56)
    assert abs(combined.intersect(barrier).Volume()-barrier.Volume())<1e-5
    lift_checks=[]
    for lift in range(0,121,2):
        overlap=plant.translate((0,0,lift)).intersect(combined).Volume()
        assert overlap<1e-5, ('planter lift clash',lift,overlap)
        lift_checks.append({'lift_mm':lift,'overlap_mm3':overlap})
    report['planter_lift_checks_2mm_steps']=lift_checks
    report['cable_checks']={'bridge_continuity_probe':'PASS','connected_4mm_route_probes':'PASS','full_height_sump_wall_probe':'PASS','rim_to_trough_floor_mm':17}
    report['standoffs']=accesses
    report['clearances_mm']={'PCB_edge_to_sidewall':10,'PCB_standoff_to_sidewall':9.5,'PCB_seating_face_to_rear_wall':18,'LCD_edge_to_sidewall':2,'LCD_to_PCB_assumed_component_envelopes':10.8,'LCD_boss_to_aperture_min':(1.8**2+3.2**2)**.5-3,'LCD_5p5mm_screw_head_to_aperture_min':(1.8**2+3.2**2)**.5-2.75,'LCD_boss_radial_wall':1.5,'fascia_edge_gap':.4,'sump_lip_side_gap':.4}
    report['assumed_envelopes']={'PCB':'Source 67 x 64 rotated to 64 x 67 installed; assumed 31.6 stack towards fascia','LCD':'Image 80 x 36 PCB; assumed 1.6 thickness and 20 rear projection; assumed 8 mm spacing behind fascia'}
    report['not_verified']=['Actual component fit and undersides','Fastener selection and print tolerances','Slicing and load strength','Leak test','Full mesh self-intersection test']
    (OUT/'verification.json').write_text(json.dumps(report,indent=2))
    cq.exporters.export(cq.Compound.makeCompound(list(parts.values())),str(OUT/'assembly.step'))
    cq.exporters.export(pump,str(OUT/'pump_envelope_reference.step'))
    # Separate coupon, not an assembly component. Left-to-right 12.0/12.2/12.4 mm holes.
    coupon=cut(box(0,0,0,76,28,3),box(-1,-1,-1,4,4,5))
    for x,d in ((14,12.0),(38,12.2),(62,12.4)):coupon=cut(coupon,cyl(x,14,-1,d/2,5))
    cq.exporters.export(coupon,str(OUT/'stl'/'button_fit_coupon.stl'),tolerance=.025,angularTolerance=.1)
    cq.exporters.export(coupon,str(OUT/'step'/'button_fit_coupon.step'))
    lcd_coupon=cut(box(0,0,0,84,40,3),box(6.3,7.7,-1,71.4,24.6,5))
    for x in (4.5,79.5):
        for y in (4.5,35.5):lcd_coupon=cut(lcd_coupon,cyl(x,y,-1,1.5,5))
    pcb_coupon=cut(box(0,0,0,73,70,2),box(11,11,-1,51,48,4))
    for x in (6.5,66.5):
        for y in (6.5,63.5):pcb_coupon=cut(pcb_coupon,cyl(x,y,-1,1.4,4))
    for name,shape in [('lcd_fit_coupon',lcd_coupon),('carrier_fit_coupon',pcb_coupon)]:
        assert shape.isValid() and len(shape.Solids())==1
        cq.exporters.export(shape,str(OUT/'stl'/f'{name}.stl'),tolerance=.025,angularTolerance=.1)
        cq.exporters.export(shape,str(OUT/'step'/f'{name}.step'))
    export_extras()
    # OpenCascade writes trailing spaces; normalise serialization only, not geometry.
    for path in OUT.rglob('*.step'):
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n',newline='\n')
    return report

def shaft_tool(d,flat,z=-1,h=12):
    sh=cyl(0,0,z,d/2,h)
    if flat is not None: sh=sh.intersect(box(-d,-d,z,2*d,d+flat,h))
    return sh

def export_extras():
    import math
    extras={}
    # Print closed top on bed, bore upwards: no trapped bore supports.
    for name,d,flat in KNOB_BORES:
        sh=cyl(0,0,0,10,14)
        for i in range(24):
            a=i*math.tau/24
            sh=cut(sh,cyl(10*math.cos(a),10*math.sin(a),-1,.65,16))
        sh=cut(sh,shaft_tool(d,flat,z=3,h=12),box(-.55,5,-.1,1.1,4,0.8))
        extras['knob_'+name]=sh
    coupon=box(0,0,0,100,32,3)
    for i,(name,d,flat) in enumerate(KNOB_BORES):
        x=12+25*(i%4);y=9+14*(i//4)
        coupon=cut(coupon,shaft_tool(d,flat,z=-1,h=5).translate((x,y,0)))
    # One clipped corner defines the origin; map printed in the guide.
    coupon=cut(coupon,box(-1,-1,-1,5,5,5))
    extras['knob_fit_coupon']=coupon
    # Optional external blank: tape temporarily for marking measured socket positions.
    # Sits OUTSIDE left wall. Customise its window after actual cable measurements.
    extras['usb_marking_blank']=box(0,0,0,34,26,1.2)
    extras['piezo_led_fit_coupon']=cut(box(0,0,0,40,22,3),cyl(10,11,-1,5.2,5),cyl(28,11,-1,2.5,5))
    # Isolated copies of real upper boss regions for slicing/fastener fit trials.
    extras['upper_boss_print_coupon']=tower.intersect(box(0,0,132,17,18,26)).translate((0,0,-132))
    for name,sh in extras.items():
        assert sh.isValid() and len(sh.Solids())==1,name
        cq.exporters.export(sh,str(OUT/'stl'/f'{name}.stl'),tolerance=.025,angularTolerance=.1)
        cq.exporters.export(sh,str(OUT/'step'/f'{name}.step'))
    (OUT/'knob_options.json').write_text(json.dumps({'units':'mm','outside_diameter':20,'height':14,
        'blind_bore_depth':11,'print':'closed top at z=0 on bed, bore upwards',
        'options':[{'file':'knob_'+n+'.stl','diameter':d,'flat_offset_from_axis':f} for n,d,f in KNOB_BORES]},indent=2))

def render():
    import vtk
    for mode in ('assembly','exploded','internal','fascia_rear','knobs'):
        renderer=vtk.vtkRenderer();renderer.SetBackground(.957,.949,.922)
        shapes=dict(parts)
        if mode=='assembly':
            knob=cq.importers.importStep(str(OUT/'step'/'knob_round_6p2.step')).val()
            shapes['knob_reference']=knob.rotate((0,0,0),(1,0,0),-90).translate((32,-14.5,48))
        if mode=='internal':
            shapes.pop('fascia_charcoal');shapes.pop('top_cover_sage')
            shapes['PCB_reference']=box(16,74.4,75,64,1.6,67)
            for x,z in PCB:
                shapes['PCB_reference']=cut(shapes['PCB_reference'],cyl(x,74,z,1.6,3,(0,1,0)))
        if mode=='fascia_rear': shapes={'fascia_charcoal':panel}
        if mode=='knobs':
            shapes={}
            for i,(name,d,flat) in enumerate(KNOB_BORES):
                sh=cq.importers.importStep(str(OUT/'step'/('knob_'+name+'.step'))).val()
                shapes[name]=sh.translate(((i%4)*26,(i//4)*28,0))
        for name,sh in shapes.items():
            if mode=='exploded':
                delta={'fascia_charcoal':(0,-38,0),'top_cover_sage':(0,0,40),'planter_sage':(25,0,55),
                       'tower_sump_body':(0,0,0),'battery_tray':(0,-25,20),'hose_clip':(0,0,15)}.get(name,(0,0,0))
                sh=sh.translate(delta)
            temp=OUT/f'_render_{name}.stl'
            cq.exporters.export(sh,str(temp),tolerance=.05,angularTolerance=.1)
            reader=vtk.vtkSTLReader();reader.SetFileName(str(temp));reader.Update()
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(reader.GetOutput())
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            colour=(.2,.23,.24) if 'charcoal' in name else (.54,.60,.50)
            if name=='PCB_reference': colour=(.15,.4,.24)
            actor.GetProperty().SetColor(*colour);actor.GetProperty().SetInterpolationToPhong()
            renderer.AddActor(actor);temp.unlink()
        camera=renderer.GetActiveCamera()
        camera.SetPosition(*((160,430,220) if mode=='fascia_rear' else (-320,-500,300)))
        if mode=='knobs': camera.SetPosition(130,-180,240)
        camera.SetFocalPoint(*((48,4,79) if mode=='fascia_rear' else (100,40,85)))
        if mode=='knobs': camera.SetFocalPoint(39,14,7)
        camera.SetViewUp(0,0,1);camera.ParallelProjectionOn()
        renderer.ResetCamera();camera.Zoom(1.10)
        window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(1400,1200)
        window.AddRenderer(renderer);window.Render()
        grab=vtk.vtkWindowToImageFilter();grab.SetInput(window);grab.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/f'{mode}.png'))
        writer.SetInputConnection(grab.GetOutputPort());writer.Write();window.Finalize()

if __name__=='__main__':
    verify()
    if '--no-render' not in sys.argv: render()
    print('PASS',flush=True)
