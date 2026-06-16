# Local CAD Generator (MCP Server)

A Model Context Protocol (MCP) server that acts as a secure bridge between Large Language Models (LLMs) and a local 3D CAD engine (CadQuery). This system allows AI agents to dynamically generate physical geometry and natively output professional-grade `.step` files based on natural language requests.

## System Architecture

The project is split into three core modules to ensure clean separation of concerns between the communication layer, the geometry engine, and offline evaluation:

* **`mcp_server.py`**: The FastMCP interface. It defines the LLM-facing tools, handles input extraction, and returns clean system outputs containing exact physical metrics.
* **`cad_file.py`**: The core CAD engine. It handles the parametric math, validates the physical geometry, and exports both 3D `.step` files and 2D `.svg` renders natively to the `samples` directory.
* **`fallback_demo.py`**: An offline execution script. Designed specifically for system evaluators, it allows the CAD engine and validation logic to be tested and graded without requiring an active LLM connection or API keys.

## Advanced Features

* **Physics Validation:** The engine mathematically proves the generated geometry is manifold and has a positive volume before saving. Impossible inputs trigger a handled `ValueError`.
* **Quantitative Evaluation:** The server automatically calculates the bounding box and exact volume (mm³) of the generated part, returning this physical data to the LLM for self-correction.
* **Multi-View Rendering:** Every successful 3D `.step` generation is accompanied by an automatically rendered 2D `.svg` file for rapid visual inspection.
* **Dynamic File Routing:** All generated files are safely isolated in the `/samples` folder and named using their exact dimensions (e.g., `plate_80.0x40.0_t8.0_hole5.0.step`) to prevent messy overwrites.

## Setup & Installation

Ensure you have Python(version 3.12 or below) and nodejs(version 20.12.2)  installed, along with the required libraries. 
*Note: If you are using a virtual environment, ensure it is activated before installing dependencies.*

```bash
pip install mcp
pip install cadquery
```

check the versions in requirements.txt

Run the mcp server using nodejs

```bash
npx -y @modelcontextprotocol/inspector python mcp_server.py
```
1. once mcp server opens go to tools --> list tools 
2. choose the shape, enter the dimensions and run
3. A step file and svg file is generated if successful.
4. These  files can be further cvisually viewed  with tool like 3dvieweroline.com



