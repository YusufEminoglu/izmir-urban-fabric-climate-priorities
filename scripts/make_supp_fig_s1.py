import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
os.makedirs(FIGDIR, exist_ok=True)

df_ind = pd.read_csv(IND_PATH)

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor="#ffffff")

# Strata definitions
strata_order = [
    "historic_core",
    "apartment_block",
    "waterfront_transformation",
    "hillside_incremental",
    "grid_residential",
    "industrial_logistics",
    "peripheral_expansion"
]
strata_labels = [
    "Historic Core",
    "Apartment Block",
    "Waterfront Trans.",
    "Hillside / Inc.",
    "Grid Res.",
    "Industrial / Log.",
    "Peripheral Exp."
]
colors_map = {
    "historic_core": "#E9B420",
    "grid_residential": "#DDB5B5",
    "apartment_block": "#EBCB9C",
    "waterfront_transformation": "#A0CBBF",
    "hillside_incremental": "#DEA6A3",
    "industrial_logistics": "#8E8E8D",
    "peripheral_expansion": "#C5AFD5"
}

# --- Panel (a): Landsat LST grid cell matching visualization ---
ax0 = axes[0, 0]
ax0.set_facecolor("#ffffff")

x = np.arange(-5, 5, 0.1)
y = stats.norm.pdf(x, 0, 1.2)
ax0.plot(x, y, color="#E9B420", linewidth=2.5, label="ECOSTRESS / Landsat Thermal PSF")
ax0.axvspan(-1.25, 1.25, alpha=0.2, color="#A0CBBF", label="250 m INSPIRE Grid Cell footprint")
ax0.axvspan(-2.5, 2.5, alpha=0.1, color="#C5AFD5", label="500 m Grid Cell footprint")

ax0.set_title("(a) PSF and Grid Footprint Commensurability", fontsize=11, fontweight="bold", color="#1e293b")
ax0.set_xlabel("Distance from Centroid (Standardized units)", fontsize=9.5)
ax0.set_ylabel("Sensor Sensitivity", fontsize=9.5)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax0.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

# --- Panel (b): Building Footprint Quality (official BBB building counts across strata) ---
ax1 = axes[0, 1]
ax1.set_facecolor("#ffffff")

sns.boxplot(
    data=df_ind,
    x="stratum_name",
    y="bld_count",
    ax=ax1,
    hue="stratum_name",
    legend=False,
    palette=colors_map,
    order=strata_order,
    showfliers=False,
    width=0.55,
    linewidth=1.0
)

ax1.set_title("(b) Official IMM Building Footprint Counts by Stratum (N=3,777)", fontsize=11, fontweight="bold", color="#1e293b")
ax1.set_xlabel("Fabric Stratum", fontsize=9.5)
ax1.set_ylabel("Building Footprints per Cell", fontsize=9.5)
ax1.set_xticks(range(len(strata_order)))
ax1.set_xticklabels(strata_labels, rotation=25, ha="right", fontsize=8.5)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")

# --- Panel (c): Geographic Location Distribution (dist_coast vs dist_core) ---
ax2 = axes[1, 0]
ax2.set_facecolor("#ffffff")

# Plot points colored by stratum
for stratum in strata_order:
    sub = df_ind[df_ind["stratum_name"] == stratum]
    ax2.scatter(
        sub["dist_core_km"],
        sub["dist_coast_km"],
        color=colors_map[stratum],
        label=strata_labels[strata_order.index(stratum)],
        alpha=0.75,
        edgecolors="#334155",
        linewidths=0.4,
        s=30
    )

ax2.set_title("(c) Geographic Distribution of Strata (Distance to Core vs Coast)", fontsize=11, fontweight="bold", color="#1e293b")
ax2.set_xlabel("Distance to Urban Core (Konak, km)", fontsize=9.5)
ax2.set_ylabel("Distance to Coastline (km)", fontsize=9.5)
ax2.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax2.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.0)

# --- Panel (d): Social Vulnerability Demographic Covariation (elderly_share vs age_dependency) ---
ax3 = axes[1, 1]
ax3.set_facecolor("#ffffff")

for stratum in strata_order:
    sub = df_ind[df_ind["stratum_name"] == stratum]
    ax3.scatter(
        sub["elderly_share"] * 100,  # Convert to percent
        sub["age_dependency"] * 100, # Convert to percent
        color=colors_map[stratum],
        alpha=0.7,
        edgecolors="#334155",
        linewidths=0.4,
        s=30
    )

ax3.set_title("(d) Demographic Input Covariation (Elderly Share vs Age Dependency)", fontsize=11, fontweight="bold", color="#1e293b")
ax3.set_xlabel("Elderly (65+) Population Share (%)", fontsize=9.5)
ax3.set_ylabel("Age Dependency Ratio (%)", fontsize=9.5)
ax3.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")

fig.suptitle("Supplementary Figure S1: Spatial Resolution and Input Data Characteristics", fontsize=14, fontweight="bold", color="#0f172a", y=0.98)
plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08, wspace=0.25, hspace=0.30)

out_path = os.path.join(FIGDIR, "supp_data_quality.png")
fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

import shutil
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(out_path, os.path.join(figs_cur, "supp_data_quality.png"))

print(f"Wrote {out_path}")
