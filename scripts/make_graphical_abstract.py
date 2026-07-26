import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
STRATA_PATH = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban_strata.gpkg")
SHAP_CSV = os.path.join(PROJ, "outputs", "tables", "shap_global_importance.csv")
PRIORITY_CSV = os.path.join(PROJ, "outputs", "tables", "adaptation_priority.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "graphical_abstract.png")

print("Loading data for graphical abstract...")
strata = gpd.read_file(STRATA_PATH).to_crs(32635)
imp = pd.read_csv(SHAP_CSV)
g = pd.read_csv(PRIORITY_CSV)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# --- Panel 1: Grid-based Morphometrics (Zoomed-in central FUA) ---
ax0 = axes[0]
colors_map = {1: "#b2182b", 2: "#ef8a62", 3: "#fddbc7", 4: "#2166ac",
              5: "#762a83", 6: "#1b7837", 7: "#999999"}
names = {1: "Historic core", 2: "Grid residential", 3: "Apartment block",
         4: "Waterfront transformation", 5: "Hillside / incremental",
         6: "Industrial / logistics", 7: "Peripheral expansion"}

# Zoom into central area (near Konak/Bornova)
minx, miny, maxx, maxy = strata.total_bounds
cx, cy = (minx + maxx)/2, (miny + maxy)/2
# crop strata to a box of 12km x 12km around central coordinates
crop_box = strata.cx[cx-6000:cx+6000, cy-6000:cy+6000]

for k in range(1, 8):
    sub = crop_box[crop_box["stratum"] == k]
    if len(sub):
        sub.plot(ax=ax0, color=colors_map[k], edgecolor="black", linewidth=0.2)

ax0.set_title("1. Grid-Based Fabric Strata\n(250 m analytical cells)", fontsize=11, fontweight="bold")
ax0.set_axis_off()

# Add a small scale bar (2 km)
ax0.plot([cx - 5000, cx - 3000], [cy - 5000, cy - 5000], color="black", linewidth=3)
ax0.text(cx - 4000, cy - 4700, "2 km", fontsize=8, fontweight="bold", ha="center")

# --- Panel 2: Explainable Heat Model (SHAP Global Importance) ---
ax1 = axes[1]
top_imp = imp.head(6)
ax1.barh(top_imp["feature"][::-1], top_imp["mean_abs_shap"][::-1], color="#fc4e2a", edgecolor="k", linewidth=0.5)
ax1.set_xlabel("Mean Absolute SHAP Value (°C)", fontsize=9)
ax1.set_title("2. Explainable LST Model\n(SHAP feature importance)", fontsize=11, fontweight="bold")
ax1.grid(True, axis="x", linestyle=":", alpha=0.6)

# --- Panel 3: Equity-aware TOPSIS (Heat vs Priority Rank) ---
ax2 = axes[2]
# We want to show LST vs TOPSIS priority rank
# Map stratum names to colors for consistency
strata_colors = [colors_map[k] for k in [4, 7, 1, 6, 2, 5, 3]] # ordered by g row strata
# Plot scatter
scatter_sizes = 200 * (1 / (1 + g["coast"])) / (1 / (1 + g["coast"])).max() + 50
ax2.scatter(g["heat"], g["topsis_entropy"], s=scatter_sizes, c=["#2166ac", "#999999", "#b2182b", "#1b7837", "#ef8a62", "#762a83", "#fddbc7"],
            edgecolor="k", linewidth=1.0, zorder=3)

# Label fabrics
for _, r in g.iterrows():
    # Map name to clean label
    lbl = r["stratum_name"].replace("_", " ").title()
    if r["stratum_name"] == "waterfront_transformation":
        lbl = "Waterfront (Rank #1)"
    ax2.annotate(lbl, (r["heat"], r["topsis_entropy"]), fontsize=7.5, fontweight="bold",
                 xytext=(5, 3), textcoords="offset points")

ax2.set_xlabel("Summer Land-Surface Temp (LST, °C)", fontsize=9)
ax2.set_ylabel("TOPSIS Priority Score (higher = more need)", fontsize=9)
ax2.set_title("3. Multi-Hazard Priority\n(Waterfront ranks first despite low LST)", fontsize=11, fontweight="bold")
ax2.grid(True, linestyle=":", alpha=0.5)

fig.suptitle("GRAPHICAL ABSTRACT\nMulti-Objective Adaptation Prioritisation in the İzmir Functional Urban Region", fontsize=13, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(OUT_FIG, dpi=150)
plt.close()
print(f"Successfully generated graphical abstract: {OUT_FIG}")
