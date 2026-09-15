"""Plant Station R14 Uno mounts, derived from R13. Millimetres; x right, y rear, z up. Run with local cad-runtime."""
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
PCB_SIZE_MM = (68.58,53.34)  # Official UNO-TH_Rev3e.brd outline
UNO_ORIGIN_XZ = (13.71,72.0)
UNO_HOLES = [(66.04,35.56),(66.04,7.62),(15.24,50.8),(13.97,2.54)]
STANDOFF_OD_MM = 6.0
PILOT_DIAMETER_MM = 2.8
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
PCB=[(UNO_ORIGIN_XZ[0]+x,UNO_ORIGIN_XZ[1]+z) for x,z in UNO_HOLES] # Components face front, USB left
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
    lower=box(4 if side=='left' else 82,4,6,10,9,9)
    # Add a concave R2 root without removing supporting material.
    root=cut(box(14,4,6,2,9,2),cyl(16,3,8,2,11,(0,1,0)))
    if side=='right': root=root.mirror('YZ',(48,0,0))
    lower=fuse(lower,root)
    tower=fuse(tower,web,lower)
for x,z in FAST:
    tower=fuse(tower,cyl(x,4,z,5,9,(0,1,0)))
    tower=cut(tower,cyl(x,3,z,1.4,11,(0,1,0)))
# Rear-integrated board standoffs, inserted via full front opening.
for x,z in PCB:
    boss=cq.Workplane('XY').newObject([cyl(x,76,z,STANDOFF_OD_MM/2,19,(0,1,0))]).edges('<Y').chamfer(0.3).val()
    tower=fuse(tower,boss)
    roots=[e for e in tower.Edges() if e.geomType()=='CIRCLE' and abs(e.Center().y-94)<1e-5 and abs(e.Center().x-x)<1e-5 and abs(e.Center().z-z)<1e-5 and abs(e.radius()-STANDOFF_OD_MM/2)<1e-5]
    assert len(roots)==1, 'Missing board boss root'
    tower=tower.fillet(0.6,roots)
    tower=cut(tower,cyl(x,75,z,PILOT_DIAMETER_MM/2,12,(0,1,0)))
# Small side aperture, through the left wall only. No top service opening.
tower=cut(tower,box(-1,USB_YZ[0],USB_YZ[1],8,*USB_WH))
usb_edges=[e for e in tower.Edges() if e.geomType()=='LINE' and (abs(e.Center().x)<1e-5 or abs(e.Center().x-6)<1e-5) and 48.9<=e.Center().y<=77.1 and 98.4<=e.Center().z<=118.6]
assert len(usb_edges)==8, 'USB edge selection changed'
tower=tower.chamfer(0.3,None,usb_edges)
for y in (25,75):
    tower=fuse(tower,dovetail(y,6,29),box(95,17 if y==25 else 67,0,5.8,16,3))
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

parts['battery_tray']=battery
# R13: one structural base; retain both water-containing walls below the rim.
# Compact cable riser integrated with divider, rear wall and sump floor.
# Cable enters from the wet side, rises, and crosses only above the rim.
CABLE_OD_MM=4.0
CABLE_ROUTE_CENTRE_YZ=(90.5,81.0)
bridge=box(94,8,0,13,84,56)
# Supported common service area, separate tube and electrical passages.
# Tube remains entirely on the wet side; only wires cross into the tower.
TUBE_OD_MM=8.0
PUMP_WIRE_OD_MM=2.5  # each of two insulated wires, provisional
riser=rounded(94,84,4,38,16,124,7)
riser=cq.Workplane('XY').newObject([riser]).edges('>Z').fillet(3).val()
combined=fuse(tower,sump,bridge,riser)
combined=cut(combined,cyl(123,92,18,5,112),cyl(110,92,18,4,70),
             box(106.5,83,18,23.5,11,34),
             cyl(89,92,81,4,21,(1,0,0)))
# Independent sensor entry starts at the sump rim, separate from wet tube path.
combined=cut(combined,cyl(89,65,64,4,9,(1,0,0)))
# Local service relief allows vertical removal; original soil cavity retained.
plant=cut(plant,box(101,83.5,56,32,17.5,76))
# Local sensor lead clearance through the planter skirt, outside the soil cavity.
plant=cut(plant,rounded(101,60,56,7,10,14,2,'X'))
# Integrated battery saddle with an under-floor tie tunnel.
# Original 72 x 22 mm clear holder space retained; tie size provisional.
combined=fuse(combined,battery,box(12,30,3.5,72,30,8.5))
combined=cut(combined,box(45,29,7,6,32,2.5))
parts.pop('battery_tray')
parts.pop('tower_sage');parts.pop('sump_charcoal')
parts['tower_sump_body']=combined
parts['planter_sage']=plant
# Keep existing tower-specific probes pointed at the revised full body.
tower=combined

# Export only the changed body and a board-size mounting coupon.
if __name__ == '__main__':
    import xml.etree.ElementTree as ET
    official=ET.parse(OUT/'references/UNO-TH_Rev3e.brd')
    holes=[(float(h.attrib['x']),float(h.attrib['y'])) for h in official.findall('.//board/plain/hole')]
    assert sorted(holes)==sorted(UNO_HOLES)
    coupon=box(0,0,0,*PCB_SIZE_MM,2)
    for x,z in UNO_HOLES:
        coupon=cut(coupon,cyl(x,z,-1,1.6,4))
    # A matching boss on the coupon tests the retained pilot and seating face.
    coupon=fuse(coupon,cyl(40,25,2,3,8))
    coupon=cut(coupon,cyl(40,25,1,1.4,10))
    report={'revision':'R14 Uno','units':'mm','cadquery':cq.__version__,'hole_centres_xz_mm':PCB,'standoff_OD_mm':6,'pilot_diameter_mm':2.8,'pilot_depth_from_seat_mm':11,'rear_clearance_mm':18,'checks':{}}
    for name,shape in [('tower_sump_body_uno',combined),('uno_mount_fit_coupon',coupon)]:
        assert shape.isValid() and len(shape.Solids())==1
        cq.exporters.export(shape,str(OUT/'stl'/f'{name}.stl'),tolerance=.025,angularTolerance=.1)
        cq.exporters.export(shape,str(OUT/'step'/f'{name}.step'))
        mesh=trimesh.load_mesh(OUT/'stl'/f'{name}.stl')
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
        assert len(mesh.split())==1
        reopened=cq.importers.importStep(str(OUT/'step'/f'{name}.step')).val()
        assert reopened.isValid() and len(reopened.Solids())==1
        assert abs(reopened.Volume()-shape.Volume())<.01
        report['checks'][name]={'valid_single_solid':True,'watertight':True,'consistent_winding':True,'mesh_components':1,'bounds_mm':mesh.bounds.tolist(),'STEP_reimport':'PASS'}
    for x,z in PCB:
        assert combined.intersect(cyl(x,75.9,z,1.39,11.05,(0,1,0))).Volume()<1e-6
        assert combined.intersect(cyl(x,87.2,z,1,1,(0,1,0))).Volume()>3
        assert combined.intersect(box(x+1.8,76.4,z-.2,.4,17,.4)).Volume()>2.6
    # Preserve every R13 feature outside small cylinders enclosing old/new mounts.
    old=cq.importers.importStep(str(OUT.parent/'concept_rev13/step/tower_sump_body.step')).val()
    regions=[cyl(x,75,z,5,20,(0,1,0)) for x,z in PCB+[(19.5,78.5),(76.5,78.5),(19.5,138.5),(76.5,138.5)]]
    mask=fuse(regions[0],*regions[1:])
    added=combined.cut(old).cut(mask).Volume()
    removed=old.cut(combined).cut(mask).Volume()
    assert added<.01 and removed<.01,(added,removed)
    report['outside_mount_change_mm3']={'added':added,'removed':removed}
    board=box(13.71,74.4,72,68.58,1.6,53.34)
    assert combined.intersect(board).Volume()<1e-6
    report['board_envelope_interference_mm3']=combined.intersect(board).Volume()
    report['limitations']=['Actual Uno variant and screw fit unmeasured; print coupon first','Existing USB aperture retained; plug access and component/header clearances require physical trial','Not sliced, printed or physically fit-tested; full mesh self-intersection not checked']
    (OUT/'verification.json').write_text(json.dumps(report,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    mesh=trimesh.load_mesh(OUT/'stl/tower_sump_body_uno.stl')
    fig,ax=plt.subplots(figsize=(10,8))
    for y,col in [(90,'#264c3f'),(76.5,'#c26a20')]:
        section=mesh.section(plane_origin=[0,y,0],plane_normal=[0,1,0])
        for loop in section.discrete: ax.plot(loop[:,0],loop[:,2],color=col,lw=1)
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((13.71,72),68.58,53.34,fill=False,ls='--',color='royalblue'))
    for i,(x,z) in enumerate(PCB): ax.annotate(f'{i+1}: {x:.2f}, {z:.2f}',(x,z),xytext=(5,7),textcoords='offset points',fontsize=8)
    ax.set(xlim=(-4,211),ylim=(-4,162),xlabel='x / mm',ylabel='z / mm',title='R14 Uno mounts - exported STL sections\nDashed: board envelope; labels: mounting centres x, z / mm')
    ax.set_aspect('equal');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'mount_section.png',dpi=160);plt.close(fig)
    import vtk
    ren=vtk.vtkRenderer();ren.SetBackground(.95,.95,.92)
    reader=vtk.vtkSTLReader();reader.SetFileName(str(OUT/'stl/tower_sump_body_uno.stl'));reader.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(reader.GetOutput())
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(.45,.58,.48);ren.AddActor(actor)
    cam=ren.GetActiveCamera();cam.SetPosition(260,-500,310);cam.SetFocalPoint(100,45,80);cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();ren.ResetCamera()
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1100,1000);win.AddRenderer(ren);win.Render()
    grab=vtk.vtkWindowToImageFilter();grab.SetInput(win);grab.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/'preview.png'));writer.SetInputConnection(grab.GetOutputPort());writer.Write();win.Finalize()
    print('PASS: exports, mounts, unchanged exterior, STEP and mesh verification',flush=True)
