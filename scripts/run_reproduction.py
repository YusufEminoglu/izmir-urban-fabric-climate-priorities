"""
run_reproduction.py
--------------------------------------------------------------------------------
Master Reproduction Pipeline
Executes the full analytical workflow end-to-end to reproduce all manuscript
tables (table1.csv to table8.csv) and figures (figure1.png to figure11.png).
--------------------------------------------------------------------------------
"""

import os
import subprocess
import sys

SCRIPTS = [
    "01_spatial_grid_processing.py",
    "02_morphometric_typology.py",
    "03_explainable_heat_attribution.py",
    "04_spatial_autocorrelation.py",
    "05_pareto_topsis_prioritization.py"
]

def run_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("================================================================================")
    print("STARTING FULL MANUSCRIPT REPRODUCTION PIPELINE")
    print("================================================================================")
    
    for script_name in SCRIPTS:
        script_path = os.path.join(script_dir, script_name)
        print(f"\n[RUNNING STAGE] {script_name}...")
        res = subprocess.run([sys.executable, script_path], cwd=script_dir)
        if res.returncode != 0:
            print(f"Error running {script_name}. Aborting.")
            sys.exit(res.returncode)
            
    print("\n================================================================================")
    print("FULL MANUSCRIPT REPRODUCTION PIPELINE COMPLETED SUCCESSFULLY!")
    print("================================================================================")

if __name__ == "__main__":
    run_all()
