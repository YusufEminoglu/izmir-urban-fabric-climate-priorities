import os
import subprocess
import sys

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
PYTHON = os.path.join(PROJ, ".venv", "Scripts", "python.exe")

scripts = [
    "make_study_area_map.py",
    "make_flowchart.py",
    "make_fabric_comparison.py",
    "pilot_07_cluster.py",
    "make_fig05_scale_stability.py",
    "pilot_09_shap.py",
    "pilot_14_geomap.py",
    "make_fig08_spatial_inequality.py",
    "make_fig09_flow_sankey.py",
    "pilot_13_cell_pareto.py",
    "make_fig11_topsis_robustness.py",
    "make_elite_tissue_comparison.py",
    "make_elite_morphology_maps.py",
    "make_elite_statistical_collage.py",
    "make_supp_fig_s1.py",
    "make_supp_fig_s2.py",
    "make_supp_fig_s3.py",
    "make_supp_fig_s4.py"
]

print("Starting figure regeneration workflow...")
for script in scripts:
    path = os.path.join(PROJ, "scripts", script)
    print(f"\n==========================================")
    print(f"Running {script}...")
    print(f"==========================================")
    res = subprocess.run([PYTHON, path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR running {script}:")
        print(res.stderr)
        sys.exit(1)
    else:
        print(res.stdout.strip())
        print(f"Finished {script} successfully.")

print("\nAll figures regenerated successfully.")
