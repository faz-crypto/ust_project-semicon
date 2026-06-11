import os
import cadquery as cq

def generate_spacer_step(outer_diameter: float, inner_diameter: float, height: float) -> str:
    """Generates a hollow cylindrical spacer and saves it using its dimensions."""
    
    # 1. Generate the CadQuery geometry
    result = (
        cq.Workplane("XY")
        .circle(outer_diameter / 2.0)
        .circle(inner_diameter / 2.0)
        .extrude(height)
    )
    
    # 2. Ensure the samples directory exists
    output_dir = "samples"
    os.makedirs(output_dir, exist_ok=True)
    
    # 3. Create a filename using only the dimensions
    filename = f"spacer_od{outer_diameter}_id{inner_diameter}_h{height}.step"
    filepath = os.path.join(output_dir, filename)
    
    # 4. Export natively to that path
    cq.exporters.export(result, filepath)
    
    return filepath

def generate_plate_step(length: float, width: float, thickness: float, hole_diameter: float) -> str:
    """Generates a rectangular plate and saves it using its dimensions."""
    
    # 1. Generate the CadQuery geometry
    result = (
        cq.Workplane("XY")
        .box(length, width, thickness)
        .faces(">Z").workplane()
        .rect(length - (hole_diameter * 2.5), width - (hole_diameter * 2.5), forConstruction=True)
        .vertices()
        .hole(hole_diameter)
    )
    
    # 2. Ensure the samples directory exists
    output_dir = "samples"
    os.makedirs(output_dir, exist_ok=True)
    
    # 3. Create a filename using only the dimensions
    filename = f"plate_{length}x{width}_t{thickness}_hole{hole_diameter}.step"
    filepath = os.path.join(output_dir, filename)
    
    # 4. Export natively to that path
    cq.exporters.export(result, filepath)
    
    return filepath