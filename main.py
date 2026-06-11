"""
Pure Python 3.11+ CAD Generation Module using CadQuery.
Completely Offline. Designed to be imported by an external MCP Server.
"""

import os
import cadquery as cq

def generate_spacer_step(outer_d: float, inner_d: float, height: float, output_dir: str = "./output") -> str:
    """
    Validates dimensions and renders a 3D STEP asset for a hollow cylindrical spacer.
    """
    # 1. Logic check before sending to the CAD kernel (Raises exception instead of sys.exit)
    if inner_d >= outer_d:
        raise ValueError("Inner diameter cannot be equal to or larger than outer diameter!")
    if height <= 0:
        raise ValueError("Height must be a positive value.")
        
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.abspath(os.path.join(output_dir, "spacer_output.step"))

    # 2. Extrude base profile solid cylinder
    model = cq.Workplane("XY").circle(outer_d / 2.0).extrude(height)
    
    # 3. Cut core bore out of center if an inner diameter exists
    if inner_d > 0:
        model = model.faces(">Z").workplane().circle(inner_d / 2.0).cutThruAll()

    # 4. Export out cleanly to disk
    cq.exporters.export(model, full_path)
    return full_path


def generate_plate_step(length: float, width: float, thickness: float, hole_d: float, output_dir: str = "./output") -> str:
    """
    Validates dimensions and renders a 3D STEP asset for a rectangular base plate.
    """
    # 1. Logic check
    if hole_d >= min(length, width):
        raise ValueError("Screwhole diameter cannot exceed the physical plate boundaries!")
    if thickness <= 0:
        raise ValueError("Thickness must be a positive value.")

    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.abspath(os.path.join(output_dir, "plate_output.step"))

    # 2. Generate solid block box
    model = cq.Workplane("XY").box(length, width, thickness)
    
    # 3. Symmetrical 4-corner drilling layout
    if hole_d > 0:
        margin = hole_d * 1.5
        coordinate_x = (length / 2.0) - margin
        coordinate_y = (width / 2.0) - margin
        
        model = (model.faces(">Z").workplane()
                 .rect(coordinate_x * 2, coordinate_y * 2, forConstruction=True)
                 .vertices().hole(hole_d))

    # 4. Export
    cq.exporters.export(model, full_path)
    return full_path