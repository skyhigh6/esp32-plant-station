"""Read final R17 STLs independently: topology and through-wall port sections."""

from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / ".tools" / "cad-runtime"))
import numpy as np
import trimesh


def circle(loops: list, centre: tuple[float, float], target: float) -> float:
    matches = []
    for loop in loops:
        radii = np.linalg.norm(loop[:, (1, 2)] - np.array(centre), axis=1)
        if len(radii) >= 8 and np.max(np.abs(radii - target / 2)) < 0.035:
            matches.append(float(np.mean(radii)) * 2)
    if len(matches) != 1:
        raise AssertionError(f"Expected one diameter {target} at {centre}; found {matches}")
    return matches[0]


def usb_rectangle(loops: list, p: dict) -> dict:
    centre = np.array(p["usb_centre_yz_mm"])
    size = np.array(p["usb_aperture_width_height_mm"])
    radius = float(p["usb_aperture_corner_radius_mm"])
    minimum, maximum = centre - size / 2, centre + size / 2
    candidates = []
    for loop in loops:
        yz = loop[:, (1, 2)]
        if (np.allclose(yz.min(axis=0), minimum, atol=0.035) and
                np.allclose(yz.max(axis=0), maximum, atol=0.035)):
            # Signed-distance residual for a rounded rectangle verifies more
            # than the bounding box, including the specified corner radius.
            q = np.abs(yz - centre) - (size / 2 - radius)
            distance = np.linalg.norm(np.maximum(q, 0), axis=1) + np.minimum(
                np.maximum(q[:, 0], q[:, 1]), 0
            ) - radius
            residual = float(np.max(np.abs(distance)))
            if residual > 0.035:
                raise AssertionError(f"USB rounded profile error {residual} mm")
            candidates.append({"bounds_yz_mm": [yz.min(axis=0).tolist(), yz.max(axis=0).tolist()],
                               "size_mm": (yz.max(axis=0) - yz.min(axis=0)).tolist(),
                               "corner_profile_max_error_mm": residual})
    if len(candidates) != 1:
        raise AssertionError(f"Expected one USB profile, found {len(candidates)}")
    return candidates[0]


def main() -> None:
    p = json.loads((HERE / "parameters.json").read_text(encoding="utf-8"))
    report = {"revision": p["revision"], "units": "mm", "files": {}, "sections": {},
              "parameters_sha256": hashlib.sha256((HERE / "parameters.json").read_bytes()).hexdigest()}
    for name, expected_extents in (
        ("tower_sump_body_uno_ports_r17", (207, 100, 158)),
        ("power_ports_fit_coupon_r17", (6, 60, 24)),
    ):
        group = "main_parts" if name.startswith("tower_") else "fit_trials"
        path = PRINT_ROOT / group / "stl" / f"{name}.stl"
        mesh = trimesh.load_mesh(path, process=True)
        if not isinstance(mesh, trimesh.Trimesh):
            raise AssertionError(f"{name}: expected one STL mesh")
        incidence = np.bincount(mesh.edges_unique_inverse)
        record = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bounds_mm": mesh.bounds.tolist(), "volume_mm3": float(mesh.volume),
            "watertight": bool(mesh.is_watertight),
            "winding_consistent": bool(mesh.is_winding_consistent),
            "components": len(mesh.split()),
            "all_edges_two_faces": bool(np.all(incidence == 2)),
            "degenerate_faces": int(np.count_nonzero(mesh.area_faces < 1e-10)),
        }
        if not (record["watertight"] and record["winding_consistent"] and
                record["components"] == 1 and record["all_edges_two_faces"] and
                record["degenerate_faces"] == 0 and record["volume_mm3"] > 0):
            raise AssertionError(f"{name}: topology failure")
        if not np.allclose(mesh.extents, expected_extents, atol=0.03):
            raise AssertionError(f"{name}: wrong dimensions {mesh.extents}")
        report["files"][name] = record
        for x in (0.5, 3.0, 5.5):
            section = mesh.section(plane_origin=(x, 0, 0), plane_normal=(1, 0, 0))
            if section is None:
                raise AssertionError(f"{name}: missing section x={x}")
            loops = section.discrete
            uy, uz = p["usb_centre_yz_mm"]
            fixing = [(uy - p["usb_fixing_pitch_mm"] / 2, uz),
                      (uy + p["usb_fixing_pitch_mm"] / 2, uz)]
            report["sections"][f"{name}_x{x}"] = {
                "dc_diameter_mm": circle(loops, tuple(p["dc_centre_yz_mm"]), p["dc_hole_diameter_mm"]),
                "usb_fixing_diameters_mm": [circle(loops, c, p["usb_fixing_pilot_diameter_mm"]) for c in fixing],
                "usb_cut": usb_rectangle(loops, p),
            }
    report["unsupported"] = ["Full mesh self-intersection", "Slicer layers", "Physical fit and strength"]
    (REPORT_DIR / "independent_mesh_check.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PASS: 2 R17 meshes; six wall sections confirm USB profile, 2 fixing pilots and 10 mm bore")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-root", type=Path, default=ROOT / "technical/print")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "verification/cad")
    args = parser.parse_args()
    PRINT_ROOT = args.print_root.resolve()
    REPORT_DIR = args.report_dir.resolve()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    main()
