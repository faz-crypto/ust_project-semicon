"""
Offline execution script for verifying CAD generation and validation logic.
"""
import logging
import cad_file

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def run_demo():
    logging.info("Initiating CAD generation fallback demo...")

    try:
        # 1. Standard Spacer
        filepath, metrics = cad_file.generate_spacer_step(40.0, 20.0, 15.0)
        logging.info(f"Spacer generated successfully at {filepath}")

        # 2. Standard Base Plate
        filepath, metrics = cad_file.generate_plate_step(80.0, 40.0, 8.0, 5.0)
        logging.info(f"Plate generated successfully at {filepath}")

        # 3. Validation Logic Test (Intentional Failure)
        try:
            cad_file.generate_spacer_step(20.0, 40.0, 15.0)
            logging.error("Validation failed: System did not catch invalid geometry.")
        except ValueError as e:
            logging.info(f"Validation successful: Caught expected error -> '{e}'")

        logging.info("Demo complete. Output files are available in the target directory.")

    except Exception as e:
        logging.error(f"Demo execution failed: {e}")

if __name__ == "__main__":
    run_demo()
