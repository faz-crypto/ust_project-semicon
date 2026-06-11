import cad_file

print("Testing Spacer...")
spacer_file = cad_file.generate_spacer_step(outer_d=40.0, inner_d=20.0, height=15.0)
print(f"Spacer generated at: {spacer_file}")

print("Testing Plate...")
plate_file = cad_file.generate_plate_step(length=80.0, width=40.0, thickness=8.0, hole_d=5.0)
print(f"Plate generated at: {plate_file}")

# Test your error handling!
try:
    cad_file.generate_spacer_step(outer_d=20.0, inner_d=40.0, height=15.0)
except ValueError as e:
    print(f"Error successfully caught: {e}")