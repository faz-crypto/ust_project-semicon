"""
mcp_server.py
Exposes the CAD Engine to an LLM via the Model Context Protocol.
"""
import cad_file
from mcp.server.fastmcp import FastMCP

# Initialize the MCP erver
mcp = FastMCP("Local_CAD_Generator")

@mcp.tool()
def create_spacer(outer_diameter: float, inner_diameter: float, height: float) -> str:
    """
    Generates a 3D STEP file of a hollow cylindrical spacer.
    Use this tool when the user asks to create a spacer, cylinder, or washer.
    """
    try:
        # Pass the LLM's extracted arguments directly to the CAD engine
        filename = cad_file.generate_spacer_step(outer_diameter, inner_diameter, height)
        return f"Success! The spacer STEP file was generated at: {filename}"
    except ValueError as e:
        # If the LLM passed bad math, return the error so the LLM can try again
        return f"Tool Error: {str(e)}"
    except Exception as e:
        return f"System Error during CAD generation: {str(e)}"


@mcp.tool()
def create_plate(length: float, width: float, thickness: float, hole_diameter: float) -> str:
    """
    Generates a 3D STEP file of a rectangular base plate with 4 corner mounting holes.
    Use this tool when the user asks to create a plate, board, or rectangular base.
    """
    try:
        filename = cad_file.generate_plate_step(length, width, thickness, hole_diameter)
        return f"Success! The plate STEP file was generated at: {filename}"
    except ValueError as e:
        return f"Tool Error: {str(e)}"
    except Exception as e:
        return f"System Error during CAD generation: {str(e)}"

if __name__ == "__main__":
    mcp.run()