"""
cad_file.py
Core geometric math engine using CadQuery.
Handles validation and step file generation.
"""
import cadquery as cq

def generate_spacer_step(outer_diameter: float, inner_diameter: float, height: float) -> str:
    """Generates a hollow cylindrical spacer and saves it with a dynamic filename."""
    # 1. Validation (Catch bad math before it crashes the engine)
    if inner_diameter >= outer_diameter:
        raise ValueError("Geometry Error: Inner diameter must be smaller than outer diameter.")
    if height <= 0:
        raise ValueError("Geometry Error: Height must be greater than 0.")

    # 2. Geometric Math (CadQuery)
    result = (
        cq.Workplane("XY")
        .circle(outer_diameter / 2.0)
        .circle(inner_diameter / 2.0)
        .extrude(height)
    )
    
    # 3. Dynamic File Naming & Export
    filename = f"spacer_OD{outer_diameter}_ID{inner_diameter}_H{height}.step"
    cq.exporters.export(result, filename)
    
    return filename


def generate_plate_step(length: float, width: float, thickness: float, hole_diameter: float) -> str:
    """Generates a rectangular base plate with 4 corner holes and saves it with a dynamic filename."""
    # 1. Validation
    if thickness <= 0 or length <= 0 or width <= 0:
        raise ValueError("Geometry Error: Dimensions must be greater than 0.")
    if hole_diameter >= min(length, width) / 2:
        raise ValueError("Geometry Error: Hole diameter is too large for the plate dimensions.")

    # 2. Geometric Math (Base Plate)
    result = cq.Workplane("XY").box(length, width, thickness)
    
    # 3. Geometric Math (Calculate corner hole positions)
    margin = hole_diameter + 2  # Keep holes 2mm away from the edge
    x_offset = (length / 2) - margin
    y_offset = (width / 2) - margin
    
    # Ensure the plate isn't too small for the margin
    if x_offset <= 0 or y_offset <= 0:
        x_offset = length / 4
        y_offset = width / 4

    pts = [
        (x_offset, y_offset),
        (x_offset, -y_offset),
        (-x_offset, y_offset),
        (-x_offset, -y_offset)
    ]
    
    # Cut the holes through the Z face
    result = result.faces(">Z").workplane().pushPoints(pts).hole(hole_diameter)
    
    # 4. Dynamic File Naming & Export
    filename = f"plate_{length}x{width}_thick{thickness}.step"
    cq.exporters.export(result, filename)
    
    return filename