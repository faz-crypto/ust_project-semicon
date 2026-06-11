"""
MCP server interface for the local CAD engine.
"""
import cad_file
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Local_CAD_Generator")

@mcp.tool()
def create_spacer(outer_diameter: float, inner_diameter: float, height: float) -> str:
    """
    Generates a 3D STEP file of a hollow cylindrical spacer.
    """
    try:
        filepath = cad_file.generate_spacer_step(outer_diameter, inner_diameter, height)
        return f"Generated spacer at: {filepath}"
    except ValueError as e:
        return f"Input error: {str(e)}"
    except Exception as e:
        return f"Generation failed: {str(e)}"

@mcp.tool()
def create_plate(length: float, width: float, thickness: float, hole_diameter: float) -> str:
    """
    Generates a 3D STEP file of a rectangular base plate with corner mounting holes.
    """
    try:
        filepath = cad_file.generate_plate_step(length, width, thickness, hole_diameter)
        return f"Generated plate at: {filepath}"
    except ValueError as e:
        return f"Input error: {str(e)}"
    except Exception as e:
        return f"Generation failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()