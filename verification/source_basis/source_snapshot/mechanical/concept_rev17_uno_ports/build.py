"""R17 left-wall ports, derived from the R16 relay body. Millimetres.

USB dimensions are explicitly authorised estimates. Print the wall coupon
before the full body. Earlier revisions and electronics are independent inputs.
"""

from pathlib import Path
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".tools" / "cad-runtime"))
import cadquery as cq
import trimesh

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "concept_rev16_uno_relay"
V = cq.Vector
WALL_MM = 6.0
COUPON_ORIGIN_YZ = (20.0, 96.5)
COUPON_SIZE_YZ = (60.0, 24.0)
# Includes the original opening and its 0.3 mm edge chamfers, with 1 mm overlap.
CLOSURE_YZ = (48.0, 97.5)
CLOSURE_SIZE_YZ = (30.0, 22.0)


def box(x: float, y: float, z: float, dx: float, dy: float, dz: float) -> cq.Solid:
    return cq.Solid.makeBox(dx, dy, dz, V(x, y, z))


def round_hole(y: float, z: float, diameter: float,
               x: float = -1.0, length: float = 8.0) -> cq.Solid:
    return cq.Solid.makeCylinder(diameter / 2, length, V(x, y, z), V(1, 0, 0))


def positive(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{name}: expected a number in millimetres")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name}: expected a finite positive dimension")
    return result


def load_parameters() -> dict:
    p = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    if p["units"] != "mm":
        raise ValueError("Only millimetre parameters are supported")
    for name in ("usb_centre_yz_mm", "usb_aperture_width_height_mm", "dc_centre_yz_mm"):
        values = p[name]
        if not isinstance(values, list) or len(values) != 2:
            raise ValueError(f"{name}: expected exactly two dimensions")
        p[name] = tuple(positive(v, name) for v in values)
    for name in ("usb_aperture_corner_radius_mm", "usb_fixing_pitch_mm",
                 "usb_fixing_pilot_diameter_mm", "dc_hole_diameter_mm"):
        p[name] = positive(p[name], name)
    w, h = p["usb_aperture_width_height_mm"]
    r = p["usb_aperture_corner_radius_mm"]
    if 2 * r >= min(w, h):
        raise ValueError("USB corner radius must be smaller than half either cut dimension")
    pitch = p["usb_fixing_pitch_mm"]
    pilot = p["usb_fixing_pilot_diameter_mm"]
    if (pitch - w - pilot) / 2 < 1.0:
        raise ValueError("USB aperture leaves less than 1 mm material to a fixing pilot")
    uy, uz = p["usb_centre_yz_mm"]
    dy, dz = p["dc_centre_yz_mm"]
    if abs(uz - dz) > 1e-6:
        raise ValueError("This panel layout requires both connector centres at the same height")
    flange = positive(p["reference_only"]["usb_flange_width_mm"], "USB flange width")
    if abs(uy - dy) - flange / 2 - p["dc_hole_diameter_mm"] / 2 < 4:
        raise ValueError("DC hole is too close to the USB flange reference envelope")
    # Both the full body and representative coupon use these same coordinates.
    cy, cz = COUPON_ORIGIN_YZ
    sy, sz = COUPON_SIZE_YZ
    for y, z, half_w, half_h in (
        (uy, uz, max(w / 2, pitch / 2 + pilot / 2), h / 2 + pilot / 2),
        (dy, dz, p["dc_hole_diameter_mm"] / 2, p["dc_hole_diameter_mm"] / 2),
    ):
        if min(y - half_w - cy, cy + sy - y - half_w,
               z - half_h - cz, cz + sz - z - half_h) < 2:
            raise ValueError("A port is too close to the coupon edge or outside its footprint")
    return p


def usb_cut(p: dict) -> cq.Solid:
    y, z = p["usb_centre_yz_mm"]
    w, h = p["usb_aperture_width_height_mm"]
    raw = box(-1, y - w / 2, z - h / 2, 8, w, h)
    return cq.Workplane("XY").newObject([raw]).edges("|X").fillet(
        p["usb_aperture_corner_radius_mm"]
    ).val()


def fixing_centres(p: dict) -> tuple[tuple[float, float], ...]:
    y, z = p["usb_centre_yz_mm"]
    return tuple((y + sign * p["usb_fixing_pitch_mm"] / 2, z) for sign in (-1, 1))


def cut_ports(solid: cq.Solid, p: dict) -> cq.Solid:
    solid = solid.cut(usb_cut(p)).clean()
    for y, z in fixing_centres(p):
        solid = solid.cut(round_hole(y, z, p["usb_fixing_pilot_diameter_mm"])).clean()
    y, z = p["dc_centre_yz_mm"]
    return solid.cut(round_hole(y, z, p["dc_hole_diameter_mm"])).clean()


def export(name: str, shape: cq.Solid) -> dict:
    if not shape.isValid() or len(shape.Solids()) != 1:
        raise ValueError(f"{name}: expected one valid solid")
    stl = HERE / "stl" / f"{name}.stl"
    step = HERE / "step" / f"{name}.step"
    cq.exporters.export(shape, str(stl), tolerance=0.025, angularTolerance=0.1)
    cq.exporters.export(shape, str(step))
    mesh = trimesh.load_mesh(stl)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"{name}: STL did not reopen as a mesh")
    if not (mesh.is_watertight and mesh.is_winding_consistent and
            mesh.volume > 0 and len(mesh.split()) == 1):
        raise ValueError(f"{name}: STL topology failed")
    reopened = cq.importers.importStep(str(step)).val()
    if not reopened.isValid() or len(reopened.Solids()) != 1:
        raise ValueError(f"{name}: STEP did not reopen as one valid solid")
    if abs(reopened.Volume() - shape.Volume()) > 0.02:
        raise ValueError(f"{name}: STEP volume changed")
    return {
        "stl_sha256": hashlib.sha256(stl.read_bytes()).hexdigest(),
        "step_sha256": hashlib.sha256(step.read_bytes()).hexdigest(),
        "bounds_mm": mesh.bounds.tolist(), "volume_mm3": float(mesh.volume),
        "watertight": bool(mesh.is_watertight),
        "winding_consistent": bool(mesh.is_winding_consistent),
        "mesh_components": len(mesh.split()), "step_one_valid_solid": True,
    }


def verify(base: cq.Solid, body: cq.Solid, p: dict) -> dict:
    mask = box(-0.01, 20, 96.5, 6.02, 60, 24)
    difference = {}
    for label, delta in (("added", body.cut(base)), ("removed", base.cut(body))):
        outside = delta.cut(mask).Volume() if delta.Volume() > 0.001 else 0.0
        if outside > 0.02:
            raise ValueError(f"{outside} mm3 {label} outside the named left-wall region")
        difference[label] = outside

    checks = {}
    for name, cutter in (("usb", usb_cut(p)),
                         ("dc", round_hole(*p["dc_centre_yz_mm"], p["dc_hole_diameter_mm"]))):
        overlap = body.intersect(cutter).Volume()
        if overlap > 0.01:
            raise ValueError(f"{name}: through-passage is blocked")
        checks[name + "_passage_obstruction_mm3"] = overlap
    for i, (y, z) in enumerate(fixing_centres(p)):
        obstruction = body.intersect(round_hole(y, z, p["usb_fixing_pilot_diameter_mm"])).Volume()
        if obstruction > 0.01:
            raise ValueError(f"USB fixing pilot {i}: blocked")
        checks[f"usb_fixing_{i}_obstruction_mm3"] = obstruction

    # Closure of the old window is checked away from the new USB and its pilots.
    restored_strip = box(0.1, 49.5, 99.0, 5.8, 27.0, 4.0)
    missing = restored_strip.cut(body).Volume()
    if missing > 0.01:
        raise ValueError("Old USB window has not been restored to a continuous wall")
    checks["old_window_restored_strip_missing_mm3"] = missing

    uy, uz = p["usb_centre_yz_mm"]
    dy, dz = p["dc_centre_yz_mm"]
    ref = p["reference_only"]
    # Proxies test only nominal clearance. They do not establish actual envelopes.
    proxies = {
        "usb_module_guess": box(0, uy - ref["usb_pcb_width_mm"] / 2,
                                 uz - 3.5, ref["usb_overall_depth_mm"],
                                 ref["usb_pcb_width_mm"], 7),
        "dc_internal_guess": round_hole(dy, dz, 10, 6, ref["dc_internal_body_length_mm_guess"]),
        "uno_pcb": box(13.71, 74.4, 72, 68.58, 1.6, 53.34),
        "relay_pcb": box(21, 74.4, 33, 50, 1.6, 26),
    }
    cavity = box(6.001, 8, 6, 83.99, 86, 152)
    for name, proxy in proxies.items():
        volume = body.intersect(proxy.intersect(cavity)).Volume()
        if volume > 0.01:
            raise ValueError(f"Nominal {name} clearance is obstructed")
        checks[name + "_internal_interference_mm3"] = volume
    for name in ("usb_module_guess", "dc_internal_guess"):
        for board in ("uno_pcb", "relay_pcb"):
            overlap = proxies[name].intersect(proxies[board]).Volume()
            if overlap > 0.01:
                raise ValueError(f"{name} intersects {board}")
            checks[f"{name}_to_{board}_interference_mm3"] = overlap
    return {"change_outside_left_wall_mm3": difference, **checks}


def main() -> None:
    p = load_parameters()
    for folder in ("stl", "step"):
        (HERE / folder).mkdir(exist_ok=True)
    baseline_path = BASE / "step" / "tower_sump_body_uno_relay_r16.step"
    base = cq.importers.importStep(str(baseline_path)).val()
    if not base.isValid() or len(base.Solids()) != 1:
        raise ValueError("Invalid R16 baseline")
    patch = box(0, *CLOSURE_YZ, WALL_MM, *CLOSURE_SIZE_YZ)
    body = cut_ports(base.fuse(patch).clean(), p)
    coupon = cut_ports(box(0, *COUPON_ORIGIN_YZ, WALL_MM, *COUPON_SIZE_YZ), p)
    interfaces = verify(base, body, p)
    report = {
        "revision": p["revision"], "status": "PROVISIONAL USB DIMENSIONS - FIT COUPON FIRST",
        "units": "mm", "cadquery": cq.__version__,
        "baseline_step": str(baseline_path.relative_to(ROOT)),
        "baseline_step_sha256": hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        "parameters_sha256": hashlib.sha256((HERE / "parameters.json").read_bytes()).hexdigest(),
        "parameters": p, "interfaces": interfaces,
        "exports": {
            "tower_sump_body_uno_ports_r17": export("tower_sump_body_uno_ports_r17", body),
            "power_ports_fit_coupon_r17": export("power_ports_fit_coupon_r17", coupon),
        },
        "physical_status": {
            "usb_shell_flange_holes_plug_screws_solder_access": "Not tested; estimates require coupon",
            "dc_thread_nut_panel_grip_depth_and_cable": "Not tested; 10 mm is only the requested cut diameter",
            "r15_r16_physical_gates": "Remain open; prior Uno, relay, lid and pump trials still required",
            "slicing_printing_strength_leaks": "Not performed",
            "full_mesh_self_intersection": "Not checked",
            "electrical_supply_wiring": "No change or electrical acceptance; six-pin USB/5 A image label is not a verified specification",
        },
    }
    (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PASS: R17 solid, STEP readback, STL topology and named left-wall checks", flush=True)


if __name__ == "__main__":
    main()
