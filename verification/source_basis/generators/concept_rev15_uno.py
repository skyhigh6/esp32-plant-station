"""R15 Uno prototype revision from the R14 STEP body. Dimensions are millimetres.

R14 geometry is retained except for the four Uno bosses and the wet-side riser
relief. The lid replaces the retained R13 roof. Physical screw and pump fit
remain trial checks; see DESIGN_REVIEW.md.
"""

from pathlib import Path
import hashlib
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".tools" / "cad-runtime"))

import cadquery as cq
import trimesh


HERE = Path(__file__).resolve().parent
R14 = HERE.parent / "concept_rev14_uno"
R13 = HERE.parent / "concept_rev13"
STL = HERE / "stl"
STEP = HERE / "step"
STL.mkdir(exist_ok=True)
STEP.mkdir(exist_ok=True)
V = cq.Vector

# R14 mount centres, board seat and blind-pilot depth are retained.
UNO_HOLES_XZ = ((79.75, 107.56), (79.75, 79.62), (28.95, 122.80), (27.68, 74.54))
BOARD_SEAT_Y = 76.0
BOSS_LENGTH_MM = 19.0
BOSS_TIP_OD_MM = 8.5
BOSS_ROOT_OD_MM = 10.0
PILOT_DIAMETER_MM = 2.8  # provisional until the photographed screw is trialled
PILOT_DEPTH_MM = 11.0

# Remove the R14 ledge visible in Photo 4, stopping at the sump's 4 mm floor.
PUMP_RELIEF_X_MM = (106.5, 132.0)
PUMP_RELIEF_Y_MM = (83.0, 94.0)
PUMP_RELIEF_Z_MM = (4.0, 52.0)

# The pocket lowers the head bearing plane to R14's original z=161, preserving
# the effective screw stack despite the thicker roof.
LID_X_OVERHANG_MM = 1.5
LID_BASE_Z_MM = 158.0
LID_THICKNESS_MM = 5.5
LID_HEAD_POCKET_DIAMETER_MM = 6.6  # generous prototype allowance; measure actual heads
LID_HEAD_POCKET_DEPTH_MM = 2.5
LID_THROUGH_DIAMETER_MM = 3.4
LID_HOLES_XY = tuple((x, y) for x in (3.5, 92.5) for y in (15.0, 85.0))

assert (BOSS_TIP_OD_MM - PILOT_DIAMETER_MM) / 2 >= 2.5, "Boss tip wall is too thin"
assert LID_THICKNESS_MM - LID_HEAD_POCKET_DEPTH_MM >= 3.0, "Lid pocket floor is too thin"
assert LID_X_OVERHANG_MM + 3.5 - LID_HEAD_POCKET_DIAMETER_MM / 2 >= 1.5, "Lid pocket is too close to the side edge"
assert LID_BASE_Z_MM + LID_THICKNESS_MM - LID_HEAD_POCKET_DEPTH_MM == 161.0, "Lid screw bearing plane moved"
assert PUMP_RELIEF_Z_MM[0] == 4.0, "Pump relief must preserve the sump floor"
assert PUMP_RELIEF_Y_MM[1] <= 94.0, "Pump relief cuts into the rear-wall band"


def box(x: float, y: float, z: float, dx: float, dy: float, dz: float) -> cq.Solid:
    return cq.Solid.makeBox(dx, dy, dz, V(x, y, z))


def cyl(x: float, y: float, z: float, radius: float, length: float,
        axis: tuple[float, float, float] = (0, 0, 1)) -> cq.Solid:
    return cq.Solid.makeCylinder(radius, length, V(x, y, z), V(*axis))


def boss(x: float, y: float, z: float) -> cq.Solid:
    return cq.Solid.makeCone(
        BOSS_TIP_OD_MM / 2,
        BOSS_ROOT_OD_MM / 2,
        BOSS_LENGTH_MM,
        V(x, y, z),
        V(0, 1, 0),
    )


def build_body() -> cq.Solid:
    source = R14 / "step" / "tower_sump_body_uno.step"
    body = cq.importers.importStep(str(source)).val()
    if not body.isValid() or len(body.Solids()) != 1:
        raise ValueError(f"Invalid R14 source STEP: {source}")

    for x, z in UNO_HOLES_XZ:
        body = body.fuse(boss(x, BOARD_SEAT_Y, z)).clean()
        body = body.cut(cyl(
            x, BOARD_SEAT_Y - 1, z, PILOT_DIAMETER_MM / 2,
            PILOT_DEPTH_MM + 1, (0, 1, 0),
        )).clean()

    x0, x1 = PUMP_RELIEF_X_MM
    y0, y1 = PUMP_RELIEF_Y_MM
    z0, z1 = PUMP_RELIEF_Z_MM
    body = body.cut(box(x0, y0, z0, x1 - x0, y1 - y0, z1 - z0)).clean()
    return body


def build_lid() -> cq.Solid:
    lid = box(
        -LID_X_OVERHANG_MM, 0, LID_BASE_Z_MM,
        96 + 2 * LID_X_OVERHANG_MM, 100, LID_THICKNESS_MM,
    )
    lid = cq.Workplane("XY").newObject([lid]).edges("|Z").fillet(7).val()
    for x, y in LID_HOLES_XY:
        lid = lid.cut(cyl(
            x, y, LID_BASE_Z_MM - 1, LID_THROUGH_DIAMETER_MM / 2,
            LID_THICKNESS_MM + 2,
        )).clean()
        lid = lid.cut(cyl(
            x, y, LID_BASE_Z_MM + LID_THICKNESS_MM - LID_HEAD_POCKET_DEPTH_MM,
            LID_HEAD_POCKET_DIAMETER_MM / 2, LID_HEAD_POCKET_DEPTH_MM + 1,
        )).clean()
    return lid


def build_screw_trial(pilot_mm: float) -> cq.Solid:
    # The 19 mm projection and 6 mm backing wall reproduce the R15 boss length.
    coupon = box(0, 19, 0, 24, 6, 24)
    coupon = coupon.fuse(boss(12, 0, 12)).clean()
    coupon = coupon.cut(cyl(12, -1, 12, pilot_mm / 2, PILOT_DEPTH_MM + 1, (0, 1, 0))).clean()
    return coupon


def build_lid_trial() -> cq.Solid:
    coupon = box(0, 0, 0, 16, 16, LID_THICKNESS_MM)
    coupon = coupon.cut(cyl(8, 8, -1, LID_THROUGH_DIAMETER_MM / 2,
                            LID_THICKNESS_MM + 2)).clean()
    coupon = coupon.cut(cyl(8, 8, LID_THICKNESS_MM - LID_HEAD_POCKET_DEPTH_MM,
                            LID_HEAD_POCKET_DIAMETER_MM / 2,
                            LID_HEAD_POCKET_DEPTH_MM + 1)).clean()
    return coupon


def build_pump_route_trial(body: cq.Solid) -> cq.Solid:
    # Local corner of the actual R15 body. This checks the pump/tube envelope,
    # not full-body stiffness or water tightness.
    return body.intersect(box(100, 55, 0, 65, 45, 80)).clean()


def save_and_check(name: str, shape: cq.Solid) -> dict:
    if not shape.isValid() or len(shape.Solids()) != 1:
        raise ValueError(f"{name} is not one valid CAD solid")
    stl_path = STL / f"{name}.stl"
    step_path = STEP / f"{name}.step"
    cq.exporters.export(shape, str(stl_path), tolerance=0.025, angularTolerance=0.1)
    cq.exporters.export(shape, str(step_path))
    mesh = trimesh.load_mesh(stl_path)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"{name}: STL did not reopen as one mesh")
    components = mesh.split()
    if not (mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0 and len(components) == 1):
        raise ValueError(f"{name}: STL topology failed")
    reopened = cq.importers.importStep(str(step_path)).val()
    if not reopened.isValid() or len(reopened.Solids()) != 1 or abs(reopened.Volume() - shape.Volume()) > 0.02:
        raise ValueError(f"{name}: STEP reimport failed")
    return {
        "stl_sha256": hashlib.sha256(stl_path.read_bytes()).hexdigest(),
        "step_sha256": hashlib.sha256(step_path.read_bytes()).hexdigest(),
        "bounds_mm": mesh.bounds.tolist(),
        "volume_mm3": mesh.volume,
        "watertight": mesh.is_watertight,
        "consistent_winding": mesh.is_winding_consistent,
        "mesh_components": len(components),
        "step_single_valid_solid": True,
    }


def verify_interfaces(body: cq.Solid, lid: cq.Solid) -> dict:
    old = cq.importers.importStep(str(R14 / "step" / "tower_sump_body_uno.step")).val()
    regions = [cyl(x, 75, z, 5.6, 21, (0, 1, 0)) for x, z in UNO_HOLES_XZ]
    mask = regions[0]
    for region in regions[1:]:
        mask = mask.fuse(region).clean()
    x0, x1 = PUMP_RELIEF_X_MM
    y0, y1 = PUMP_RELIEF_Y_MM
    z0, z1 = PUMP_RELIEF_Z_MM
    mask = mask.fuse(box(x0 - 0.1, y0 - 0.1, z0 - 0.1,
                         x1 - x0 + 0.2, y1 - y0 + 0.2, z1 - z0 + 0.2)).clean()
    outside_added = body.cut(old).cut(mask).Volume()
    outside_removed = old.cut(body).cut(mask).Volume()
    if outside_added > 0.05 or outside_removed > 0.05:
        raise ValueError(f"Unexpected body change outside R15 regions: {outside_added}, {outside_removed}")

    board = box(13.71, 74.4, 72, 68.58, 1.6, 53.34)
    board_interference = body.intersect(board).Volume()
    if board_interference > 0.01:
        raise ValueError(f"Nominal Uno board intersects body: {board_interference}")

    # The recess is open to the 4 mm sump floor, with solid floor and dry-side web.
    recess_void = body.intersect(box(110, 84, 5, 15, 8, 12)).Volume()
    floor_material = body.intersect(box(110, 84, 0, 15, 8, 3.9)).Volume()
    dry_web_material = body.intersect(box(98, 84, 6, 6, 6, 40)).Volume()
    rear_wall_material = body.intersect(box(113, 96, 10, 4, 3, 40)).Volume()
    if recess_void > 0.01 or floor_material < 460 or dry_web_material < 1400 or rear_wall_material < 460:
        raise ValueError("Pump relief removed floor, rear wall or dry-side web")

    lid_overlap = body.intersect(lid).Volume()
    if lid_overlap > 0.01:
        raise ValueError(f"Lid intersects body: {lid_overlap}")

    # Check all blind holes still terminate within a boss.
    for x, z in UNO_HOLES_XZ:
        if body.intersect(cyl(x, 75.9, z, 1.39, 11.05, (0, 1, 0))).Volume() > 0.01:
            raise ValueError(f"Mount pilot obstructed at {(x, z)}")
        if body.intersect(cyl(x, 87.2, z, 1.0, 1.0, (0, 1, 0))).Volume() < 3.0:
            raise ValueError(f"Mount pilot is not blind at {(x, z)}")

    return {
        "change_outside_named_regions_mm3": {"added": outside_added, "removed": outside_removed},
        "nominal_uno_board_interference_mm3": board_interference,
        "riser_recess_void_mm3": recess_void,
        "sump_floor_probe_mm3": floor_material,
        "dry_web_probe_mm3": dry_web_material,
        "rear_wall_probe_mm3": rear_wall_material,
        "body_lid_interference_mm3": lid_overlap,
    }


def main() -> None:
    body = build_body()
    lid = build_lid()
    trial_28 = build_screw_trial(2.8)
    trial_30 = build_screw_trial(3.0)
    lid_trial = build_lid_trial()
    route_trial = build_pump_route_trial(body)
    report = {
        "revision": "R15 Uno prototype",
        "units": "mm",
        "cadquery": cq.__version__,
        "parameters": {
            "boss_tip_od_mm": BOSS_TIP_OD_MM,
            "boss_root_od_mm": BOSS_ROOT_OD_MM,
            "boss_length_mm": BOSS_LENGTH_MM,
            "body_pilot_diameter_mm": PILOT_DIAMETER_MM,
            "pilot_depth_mm": PILOT_DEPTH_MM,
            "pump_relief_xyz_mm": [PUMP_RELIEF_X_MM, PUMP_RELIEF_Y_MM, PUMP_RELIEF_Z_MM],
            "lid_thickness_mm": LID_THICKNESS_MM,
            "lid_pocket_diameter_mm": LID_HEAD_POCKET_DIAMETER_MM,
            "lid_pocket_depth_mm": LID_HEAD_POCKET_DEPTH_MM,
        },
        "exports": {},
    }
    for name, shape in (
        ("tower_sump_body_uno_r15", body),
        ("top_cover_flush_r15", lid),
        ("boss_trial_pilot_2p8", trial_28),
        ("boss_trial_pilot_3p0", trial_30),
        ("lid_head_trial_r15", lid_trial),
        ("pump_route_trial_r15", route_trial),
    ):
        report["exports"][name] = save_and_check(name, shape)
    report["interfaces"] = verify_interfaces(body, lid)
    report["physical_status"] = {
        "screw_fit": "pending coupon trial with actual screw and print process",
        "lid_head_fit": "pending head measurement and screw engagement trial",
        "pump_tube_fit": "pending fitted-pump and tube trial",
        "wet_dry_and_leak_test": "pending printed-body test",
    }
    (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: R15 CAD, STL, STEP and named interface checks", flush=True)


if __name__ == "__main__":
    main()
