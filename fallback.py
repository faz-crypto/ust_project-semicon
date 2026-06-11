"""
fallback_demo.py
A fail-safe execution script for evaluators. 
Run this to verify the offline CAD generation if an MCP/LLM client is unavailable.
"""

import cad_file

def run_demo():
    print("Initiating Fallback Demo: Generating 3 required CAD samples...")
    
    try:
        # Sample 1: Standard Spacer
        print("\n1. Generating Standard Spacer (Outer: 40mm, Inner: 20mm, Height: 15mm)")
        file1 = cad_file.generate_spacer_step(40.0, 20.0, 15.0)
        print(f"-> Success! Saved to: {file1}")
        
        # Sample 2: Standard Base Plate
        print("\n2. Generating Base Plate (80x40x8mm, 5mm holes)")
        file2 = cad_file.generate_plate_step(80.0, 40.0, 8.0, 5.0)
        print(f"-> Success! Saved to: {file2}")
        
        # Sample 3: Intentional Failure Handling (Testing the validation logic)
        print("\n3. Testing Geometry Validation (Inner diameter larger than outer)")
        try:
            cad_file.generate_spacer_step(20.0, 40.0, 15.0)
        except ValueError as e:
            print(f"-> Success! System correctly caught the error: '{e}'")

        print("\nDemo complete. Please check the folder for the STEP files.")
        
    except Exception as e:
        print(f"Demo failed: {e}")

if __name__ == "__main__":
    run_demo()