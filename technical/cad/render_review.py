"""R17 previews from final STL files. No fitted component proxy is displayed."""

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / ".tools" / "cad-runtime"))
import vtk

PRINT = ROOT / "technical/print/main_parts"
PREVIEWS = ROOT / "verification/cad"


def actor(path: Path, colour: tuple[float, float, float],
          left_wall_only: bool = False) -> vtk.vtkActor:
    reader = vtk.vtkSTLReader()
    reader.SetFileName(str(path))
    reader.Update()
    if reader.GetOutput().GetNumberOfCells() == 0:
        raise ValueError(f"Empty STL: {path}")
    mapper = vtk.vtkPolyDataMapper()
    if left_wall_only:
        # Exclude the opposite wall so the normal-to-panel view exposes the
        # actual through-holes rather than showing the green wall behind them.
        plane = vtk.vtkPlane()
        plane.SetOrigin(6.01, 0, 0)
        plane.SetNormal(-1, 0, 0)
        clipped = vtk.vtkClipPolyData()
        clipped.SetInputConnection(reader.GetOutputPort())
        clipped.SetClipFunction(plane)
        mapper.SetInputConnection(clipped.GetOutputPort())
    else:
        mapper.SetInputConnection(reader.GetOutputPort())
    part = vtk.vtkActor()
    part.SetMapper(mapper)
    part.GetProperty().SetColor(*colour)
    part.GetProperty().SetInterpolationToPhong()
    return part


def text(renderer: vtk.vtkRenderer, message: str, x: int, y: int, size: int = 25) -> None:
    label = vtk.vtkTextActor()
    label.SetInput(message)
    label.SetDisplayPosition(x, y)
    label.GetTextProperty().SetFontFamilyToArial()
    label.GetTextProperty().SetFontSize(size)
    label.GetTextProperty().SetColor(0.10, 0.13, 0.13)
    renderer.AddViewProp(label)


def render(detail: bool) -> None:
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.965, 0.955, 0.935)
    renderer.AddActor(actor(PRINT / "stl" / "tower_sump_body_uno_ports_r17.stl",
                            (0.42, 0.56, 0.47), left_wall_only=detail))
    if detail:
        camera_position = (-400, 48, 108.5)
        focal_point = (0, 48, 108.5)
        scale = 27
        text(renderer, "R17 LEFT PANEL  |  left wall isolated from exported STL", 35, 1145)
        text(renderer, "USB-C (estimated)", 300, 775, 29)
        text(renderer, "DC extension", 970, 775, 29)
        text(renderer, "USB-C 9.8 x 4.2, R1.2  |  2 x 2.8 pilots, 15.2 pitch  |  DC 10.0", 35, 70, 23)
        text(renderer, "USB dimensions estimated  |  wall 6.0 mm  |  centres 28.0 mm apart  |  coupon first", 35, 35, 23)
        name = "r17_left_panel_detail.png"
    else:
        renderer.AddActor(actor(PRINT / "stl" / "fascia_charcoal.stl", (0.18, 0.20, 0.21)))
        renderer.AddActor(actor(PRINT / "stl" / "planter_sage.stl", (0.56, 0.63, 0.51)))
        renderer.AddActor(actor(PRINT / "stl" / "top_cover_flush_r16.stl", (0.50, 0.60, 0.48)))
        camera_position = (-410, -460, 270)
        focal_point = (88, 43, 81)
        scale = 138
        text(renderer, "R17 USB-C + DC PANEL  |  assembly review", 35, 1145)
        text(renderer, "Provisional USB dimensions  |  R16 relay / R15 mounts and lid retained", 35, 35, 23)
        name = "r17_assembled_review.png"
    camera = renderer.GetActiveCamera()
    camera.SetPosition(*camera_position)
    camera.SetFocalPoint(*focal_point)
    camera.SetViewUp(0, 0, 1)
    camera.ParallelProjectionOn()
    camera.SetParallelScale(scale)
    renderer.ResetCameraClippingRange()
    window = vtk.vtkRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetSize(1600, 1200)
    window.AddRenderer(renderer)
    window.Render()
    capture = vtk.vtkWindowToImageFilter()
    capture.SetInput(window)
    capture.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(str(PREVIEWS / name))
    writer.SetInputConnection(capture.GetOutputPort())
    writer.Write()
    window.Finalize()


if __name__ == "__main__":
    render(True)
    render(False)
    print("PASS: R17 left panel detail and assembled STL previews")
