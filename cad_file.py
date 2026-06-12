"""The main cadquery engine with advanced features 
"""
import os
import cadquery as cq

OUTPUT_DIR = "samples"

def generate_spacer_step(outer_diameter: float, inner_diameter: float, height: float) -> tuple[str, dict]:
    """Generates a spacer, validates physical constraints, and exports STEP and SVG."""
    
    # Validate manufacturability constraints (minimum wall thickness)
    wall_thickness = (outer_diameter - inner_diameter) / 2.0
    if wall_thickness <= 0.5:
        raise ValueError(f"Manufacturability error: Wall thickness ({wall_thickness}mm) is too thin to machine/print.")
    
    # Generate core parametric geometry
    result = (
        cq.Workplane("XY")
        .circle(outer_diameter / 2.0)
        .circle(inner_diameter / 2.0)
        .extrude(height)
    )
    
    # Validate topology and physical properties
    if not result.val().isValid():
        raise ValueError("Topological error: Generated spacer geometry is invalid.")
    
    volume = result.val().Volume()
    if volume <= 0:
        raise ValueError("Physics error: Spacer geometry has zero or negative volume.")

    # Extract quantitative physical metrics
    bbox = result.val().BoundingBox()
    metrics = {
        "volume_mm3": round(volume, 2),
        "x_length": round(bbox.xlen, 2),
        "y_width": round(bbox.ylen, 2),
        "z_height": round(bbox.zlen, 2),
        "wall_thickness_mm": round(wall_thickness, 2)
    }
    
    # Export native 3D model and 2D visual rendering
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base_name = f"spacer_od{outer_diameter}_id{inner_diameter}_h{height}"
    
    step_path = os.path.join(OUTPUT_DIR, f"{base_name}.step")
    svg_path = os.path.join(OUTPUT_DIR, f"{base_name}.svg")
    
    cq.exporters.export(result, step_path)
    cq.exporters.export(result, svg_path, opt={"width": 400, "height": 400, "projectionDir": (1, 1, 1)})
    
    return step_path, metrics


def generate_plate_step(length: float, width: float, thickness: float, hole_diameter: float) -> tuple[str, dict]:
    """Generates a rectangular plate, validates physical constraints, and exports STEP and SVG."""
    
    # Validate manufacturability constraints (hole proximity to edges)
    edge_clearance = min(length, width) - (hole_diameter * 2.5)
    if edge_clearance <= hole_diameter:
        raise ValueError("Manufacturability error: Holes are too close to the plate edges and risk structural failure.")
    
    # Generate core parametric geometry
    result = (
        cq.Workplane("XY")
        .box(length, width, thickness)
        .faces(">Z").workplane()
        .rect(length - (hole_diameter * 2.5), width - (hole_diameter * 2.5), forConstruction=True)
        .vertices()
        .hole(hole_diameter)
    )
    
    # Validate topology and physical properties
    if not result.val().isValid():
        raise ValueError("Topological error: Generated plate geometry is invalid.")
    
    volume = result.val().Volume()
    if volume <= 0:
        raise ValueError("Physics error: Plate geometry has zero or negative volume.")

    # Extract quantitative physical metrics
    bbox = result.val().BoundingBox()
    metrics = {
        "volume_mm3": round(volume, 2),
        "x_length": round(bbox.xlen, 2),
        "y_width": round(bbox.ylen, 2),
        "z_height": round(bbox.zlen, 2)
    }
    
    # Export native 3D model and 2D visual rendering
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base_name = f"plate_{length}x{width}_t{thickness}_hole{hole_diameter}"
    
    step_path = os.path.join(OUTPUT_DIR, f"{base_name}.step")
    svg_path = os.path.join(OUTPUT_DIR, f"{base_name}.svg")
    
    cq.exporters.export(result, step_path)
    cq.exporters.export(result, svg_path, opt={"width": 400, "height": 400, "projectionDir": (1, 1, 1)})
    
    return step_path, metrics