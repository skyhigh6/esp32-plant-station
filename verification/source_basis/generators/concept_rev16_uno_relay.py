"""R16 Uno/relay prototype derived from the R15 STEP body. Units: mm.

The relay's nominal dimensions come from the supplied photographs and a seller
specification. Pilot size and real component/wire fit require a physical trial.
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
R15 = HERE.parent / "concept_rev15_uno"
STL = HERE / "stl"
STEP = HERE / "step"
STL.mkdir(exist_ok=True)
STEP.mkdir(exist_ok=True)
V = cq.Vector

# Viewed from the removable fascia: relay contact terminals on the right,
# DC+/DC-/IN1 terminals on the left. Board face and screwdriver access forward.
RELAY_BOARD_XZ_MIN = (21.0, 33.0)
RELAY_BOARD_XZ_SIZE = (50.0, 26.0)
RELAY_HOLE_PITCH_XZ = (44.5, 20.5)
RELAY_HOLE_DIAMETER_MM = 3.1
RELAY_CENTRES_XZ = tuple(
    (RELAY_BOARD_XZ_MIN[0] + RELAY_BOARD_XZ_SIZE[0] / 2 + sx * RELAY_HOLE_PITCH_XZ[0] / 2,
     RELAY_BOARD_XZ_MIN[1] + RELAY_BOARD_XZ_SIZE[1] / 2 + sz * RELAY_HOLE_PITCH_XZ[1] / 2)
    for sx in (-1, 1) for sz in (-1, 1)
)
RELAY_BOARD_FACE_Y = 74.4
RELAY_BOARD_SEAT_Y = 76.0
RELAY_COMPONENT_HEIGHT_MM = 18.5  # nominal seller envelope, including the PCB

# Same reinforced cone profile and same intended screw as the R15 Uno bosses.
# The 2.8 mm pilot is still a printing trial; thread and head fit are unverified.
RELAY_BOSS_LENGTH_MM = 19.0
RELAY_BOSS_TIP_OD_MM = 8.5
RELAY_BOSS_ROOT_OD_MM = 10.0
RELAY_PILOT_DIAMETER_MM = 2.8
RELAY_PILOT_DEPTH_MM = 11.0

assert RELAY_BOSS_TIP_OD_MM - RELAY_PILOT_DIAMETER_MM >= 5.0
assert RELAY_BOARD_XZ_MIN[1] - 21.0 >= 10.0  # battery saddle top
assert 72.0 - sum((RELAY_BOARD_XZ_MIN[1], RELAY_BOARD_XZ_SIZE[1])) >= 10.0  # Uno lower edge
assert RELAY_BOARD_XZ_MIN[0] >= 18.0
assert sum((RELAY_BOARD_XZ_MIN[0], RELAY_BOARD_XZ_SIZE[0])) <= 78.0


def box(x: float, y: float, z: float, dx: float, dy: float, dz: float) -> cq.Solid:
    return cq.Solid.makeBox(dx, dy, dz, V(x, y, z))


def cyl(x: float, y: float, z: float, diameter: float, length: float) -> cq.Solid:
    return cq.Solid.makeCylinder(diameter / 2, length, V(x, y, z), V(0, 1, 0))


def boss(x: float, z: float) -> cq.Solid:
    return cq.Solid.makeCone(
        RELAY_BOSS_TIP_OD_MM / 2,
        RELAY_BOSS_ROOT_OD_MM / 2,
        RELAY_BOSS_LENGTH_MM,
        V(x, RELAY_BOARD_SEAT_Y, z),
        V(0, 1, 0),
    )


def add_relay_mounts(base: cq.Solid) -> cq.Solid:
    mounted = base
    for x, z in RELAY_CENTRES_XZ:
        mounted = mounted.fuse(boss(x, z)).clean()
        mounted = mounted.cut(cyl(
            x, RELAY_BOARD_SEAT_Y - 1, z,
            RELAY_PILOT_DIAMETER_MM, RELAY_PILOT_DEPTH_MM + 1,
        )).clean()
    return mounted


def build_trial() -> cq.Solid:
    # Six-millimetre backing plate represents the rear wall. Four full-length
    # bosses test the real board pattern and screw insertion before a body print.
    return add_relay_mounts(box(16, 94, 28, 60, 6, 36))


def save_and_check(name: str, shape: cq.Solid) -> dict:
    if not shape.isValid() or len(shape.Solids()) != 1:
        raise ValueError(f"{name}: expected one valid CAD solid")
    stl_path = STL / f"{name}.stl"
    step_path = STEP / f"{name}.step"
    cq.exporters.export(shape, str(stl_path), tolerance=0.025, angularTolerance=0.1)
    cq.exporters.export(shape, str(step_path))
    mesh = trimesh.load_mesh(stl_path)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"{name}: STL did not reopen as one mesh")
    if not (mesh.is_watertight and mesh.is_winding_consistent and
            mesh.volume > 0 and len(mesh.split()) == 1):
        raise ValueError(f"{name}: STL topology failed")
    reopened = cq.importers.importStep(str(step_path)).val()
    if not reopened.isValid() or len(reopened.Solids()) != 1:
        raise ValueError(f"{name}: STEP reimport failed")
    if abs(reopened.Volume() - shape.Volume()) > 0.02:
        raise ValueError(f"{name}: STEP volume changed on reimport")
    return {
        "stl_sha256": hashlib.sha256(stl_path.read_bytes()).hexdigest(),
        "step_sha256": hashlib.sha256(step_path.read_bytes()).hexdigest(),
        "bounds_mm": mesh.bounds.tolist(),
        "volume_mm3": float(mesh.volume),
        "watertight": bool(mesh.is_watertight),
        "consistent_winding": bool(mesh.is_winding_consistent),
        "mesh_components": len(mesh.split()),
        "step_single_valid_solid": True,
    }


def verify_interfaces(old: cq.Solid, body: cq.Solid, lid: cq.Solid) -> dict:
    # Every body difference must lie in the dry-side relay mounting zone.
    mask = box(16, 74, 28, 60, 22, 36)
    added = body.cut(old)
    removed = old.cut(body)
    outside_added = added.cut(mask).Volume() if added.Volume() > 0.001 else 0.0
    outside_removed = removed.cut(mask).Volume() if removed.Volume() > 0.001 else 0.0
    if outside_added > 0.05 or outside_removed > 0.05:
        raise ValueError(f"Body changed outside relay zone: {outside_added}, {outside_removed}")

    x, z = RELAY_BOARD_XZ_MIN
    dx, dz = RELAY_BOARD_XZ_SIZE
    pcb = box(x, RELAY_BOARD_FACE_Y, z, dx, 1.6, dz)
    components = box(x, RELAY_BOARD_FACE_Y - RELAY_COMPONENT_HEIGHT_MM,
                     z, dx, RELAY_COMPONENT_HEIGHT_MM, dz)
    pcb_interference = body.intersect(pcb).Volume()
    component_interference = body.intersect(components).Volume()
    uno = box(13.71, 74.4, 72, 68.58, 1.6, 53.34)
    uno_interference = body.intersect(uno).Volume()
    lid_interference = body.intersect(lid).Volume()
    if max(pcb_interference, component_interference, uno_interference,
           lid_interference) > 0.01:
        raise ValueError("Nominal board/component/lid envelope intersects body")

    for px, pz in RELAY_CENTRES_XZ:
        open_pilot = body.intersect(cyl(px, 75.9, pz, RELAY_PILOT_DIAMETER_MM - 0.02, 11.05)).Volume()
        blind_end = body.intersect(cyl(px, 87.2, pz, 2.0, 1.0)).Volume()
        if open_pilot > 0.01 or blind_end < 3.0:
            raise ValueError(f"Relay pilot is blocked or not blind at {(px, pz)}")

    # A straight 6 mm driver envelope is clear through the front opening,
    # with the fascia removed. Actual screw-head and tool fit is a trial gate.
    driver_interferences = []
    for px, pz in RELAY_CENTRES_XZ:
        driver_interferences.append(body.intersect(cyl(px, 13, pz, 6, 62.9)).Volume())
    if max(driver_interferences) > 0.01:
        raise ValueError("Relay driver envelope blocked in front opening")

    return {
        "change_outside_relay_zone_mm3": {"added": outside_added, "removed": outside_removed},
        "nominal_relay_pcb_interference_mm3": pcb_interference,
        "nominal_relay_component_interference_mm3": component_interference,
        "nominal_uno_pcb_interference_mm3": uno_interference,
        "body_lid_interference_mm3": lid_interference,
        "relay_driver_interference_mm3": driver_interferences,
        "nominal_relay_to_uno_edge_z_clearance_mm": 72.0 - (z + dz),
        "nominal_relay_to_battery_saddle_z_clearance_mm": z - 21.0,
        "nominal_contact_terminal_to_right_inner_wall_x_clearance_mm": 90.0 - (x + dx),
        "nominal_logic_terminal_to_left_inner_wall_x_clearance_mm": x - 6.0,
    }


def main() -> None:
    old = cq.importers.importStep(str(R15 / "step" / "tower_sump_body_uno_r15.step")).val()
    lid = cq.importers.importStep(str(R15 / "step" / "top_cover_flush_r15.step")).val()
    if not old.isValid() or not lid.isValid():
        raise ValueError("Invalid R15 STEP source")
    body = add_relay_mounts(old)
    trial = build_trial()
    report = {
        "revision": "R16 Uno relay prototype",
        "units": "mm",
        "cadquery": cq.__version__,
        "parameters": {
            "relay_board_xz_min_mm": RELAY_BOARD_XZ_MIN,
            "relay_board_xz_size_mm": RELAY_BOARD_XZ_SIZE,
            "relay_hole_centres_xz_mm": RELAY_CENTRES_XZ,
            "relay_hole_pitch_xz_mm": RELAY_HOLE_PITCH_XZ,
            "relay_hole_diameter_mm_nominal": RELAY_HOLE_DIAMETER_MM,
            "relay_board_seat_y_mm": RELAY_BOARD_SEAT_Y,
            "relay_component_height_mm_nominal": RELAY_COMPONENT_HEIGHT_MM,
            "relay_boss_tip_root_od_mm": (RELAY_BOSS_TIP_OD_MM, RELAY_BOSS_ROOT_OD_MM),
            "relay_boss_length_mm": RELAY_BOSS_LENGTH_MM,
            "relay_pilot_diameter_mm_provisional": RELAY_PILOT_DIAMETER_MM,
            "relay_pilot_depth_mm": RELAY_PILOT_DEPTH_MM,
        },
        "exports": {},
    }
    for name, shape in (
        ("tower_sump_body_uno_relay_r16", body),
        ("top_cover_flush_r16", lid),
        ("relay_mount_trial_r16", trial),
    ):
        report["exports"][name] = save_and_check(name, shape)
    report["interfaces"] = verify_interfaces(old, body, lid)
    report["physical_status"] = {
        "relay_hole_pattern_and_underside": "pending four-hole and solder-clearance trial",
        "relay_screw": "pending fastener selection, head clearance and torque trial",
        "relay_terminals_and_wires": "pending fitted-module screwdriver and wire-bend trial",
        "r15_uno_lid_pump": "R15 physical acceptance remains open",
    }
    (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: R16 CAD, STL, STEP and nominal interface checks", flush=True)


if __name__ == "__main__":
    main()
