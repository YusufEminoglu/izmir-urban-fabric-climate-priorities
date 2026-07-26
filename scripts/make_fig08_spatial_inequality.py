import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from libpysal.weights import KNN
from esda.moran import Moran

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
PRIO_PATH = os.path.join(PROJ, "data", "03_processed", "cell_priority.csv")
GEO_PATH = os.path.join(PROJ, "data", "03_processed", "cell_geostats.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "spatial_inequality.png")

print("Loading cell priority and geostats data...")
df = pd.read_csv(PRIO_PATH)
df_geo = pd.read_csv(GEO_PATH)
df = df.merge(df_geo[["sample_id", "lisa", "need", "burden"]], on="sample_id")

# Calculate Moran's I and Spatial Lag of composite need (topsis_entropy)
x_coord = df["x"].values
y_coord = df["y"].values
coords = np.column_stack((x_coord, y_coord))

# Create spatial weights (k=8)
w = KNN.from_array(coords, k=8)
w.transform = 'r' # Row-standardize

need = df["need"].values  # composite adaptation-need score (z-mean of 5 axes); matches manuscript & cell_geostats

# Use dense matrix multiplication to calculate spatial lag
W = w.full()[0]
need_lag = W @ need

# Standardize need and need_lag for Moran scatterplot
need_std = (need - np.mean(need)) / np.std(need)
need_lag_std = (need_lag - np.mean(need_lag)) / np.std(need_lag)

moran = Moran(need, w)
moran_i = moran.I
moran_p = moran.p_sim

# Calculate Lorenz Curve & Gini for the impervious-exposure (1-green) x vulnerability burden
# (authoritative definition from pilot_12 / cell_geostats.csv, matching the manuscript)
burden = df["burden"].values
burden_sorted = np.sort(burden)
n = len(burden_sorted)
cum_burden = np.cumsum(burden_sorted) / np.sum(burden_sorted)
cum_pop = np.arange(1, n + 1) / n

# Gini coefficient calculated manually using trapezoid rule
gini = 1.0 - 2.0 * np.sum((cum_burden[:-1] + cum_burden[1:]) / 2.0) / n

# Calculate Share of top 20% cells
top_20_idx = int(0.8 * n)
share_top_20 = (1.0 - cum_burden[top_20_idx]) * 100

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Set up figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), facecolor="#ffffff")

# Panel a: Moran scatterplot (colored by LISA classes)
ax0 = axes[0]
ax0.set_facecolor("#ffffff")

# Moran scatterplot coloring matching Local Moran maps
LISA_COLORS = {"HH": "#E9B420", "LL": "#A0CBBF", "LH": "#C5AFD5", "HL": "#EBCB9C", "ns": "#CBD5E1"}
LISA_LABELS = {"HH": "High-High (Cluster)", "LL": "Low-Low (Cluster)", "LH": "Low-High (Outlier)", "HL": "High-Low (Outlier)", "ns": "Not Significant"}

# Plot points by LISA category
for lisa_cat in ["ns", "LH", "HL", "LL", "HH"]:
    cat_mask = df["lisa"] == lisa_cat
    if not cat_mask.any():
        continue
    ax0.scatter(
        need_std[cat_mask], need_lag_std[cat_mask],
        color=LISA_COLORS[lisa_cat], alpha=0.6,
        edgecolors="none", s=14,
        label=f"{LISA_LABELS[lisa_cat]} (n={cat_mask.sum()})"
    )

# Regression line
m, c = np.polyfit(need_std, need_lag_std, 1)
ax0.plot(need_std, m*need_std + c, color="#1e293b", linewidth=2.0, linestyle="-", label=f"Fit (Slope = Moran's I = {moran_i:.2f})")

# Quadrant dividing lines
ax0.axhline(0, color="#64748b", linestyle="--", alpha=0.6, linewidth=1.0)
ax0.axvline(0, color="#64748b", linestyle="--", alpha=0.6, linewidth=1.0)

# Quadrant text labels
ax0.text(2.2, 2.2, "High-High\n(Hotspots)", ha="right", va="top", fontsize=8, color="#64748b", fontweight="bold")
ax0.text(-2.2, -2.2, "Low-Low\n(Coldspots)", ha="left", va="bottom", fontsize=8, color="#64748b", fontweight="bold")
ax0.text(-2.2, 2.2, "Low-High\n(Outliers)", ha="left", va="top", fontsize=8, color="#64748b", fontweight="bold")
ax0.text(2.2, -2.2, "High-Low\n(Outliers)", ha="right", va="bottom", fontsize=8, color="#64748b", fontweight="bold")

ax0.set_xlim([-2.5, 2.5])
ax0.set_ylim([-2.5, 2.5])

ax0.set_title(f"(a) Spatial-lag scatterplot (Moran's I = {moran_i:.2f}, p = {moran_p:.3f})", fontsize=11.5, fontweight="bold", color="#1e293b")
ax0.set_xlabel("Adaptation Need Score (Standardized)", fontsize=9.5)
ax0.set_ylabel("Spatial Lag of Need Score (Standardized)", fontsize=9.5)
ax0.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8, framealpha=0.95, markerscale=1.8)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
for _sp in ["top", "right"]:
    ax0.spines[_sp].set_visible(False)

# Panel b: Lorenz Curve and Gini
ax1 = axes[1]
ax1.set_facecolor("#ffffff")
ax1.plot(cum_pop, cum_pop, color="#8E8E8D", linestyle="--", label="Line of Perfect Equality")
ax1.plot(cum_pop, cum_burden, color="#E9B420", linewidth=2.5, label=f"Lorenz Curve (Gini = {gini:.2f})")
ax1.fill_between(cum_pop, cum_pop, cum_burden, color="#C5AFD5", alpha=0.2, label="Inequality Area")

# Annotation of the Share of top 20%
ax1.annotate(
    f"Top 20% of cells bear {share_top_20:.1f}% of total burden",
    xy=(0.8, cum_burden[top_20_idx]),
    xytext=(0.4, 0.25),
    arrowprops=dict(facecolor="#1e293b", shrink=0.08, width=1.0, headwidth=5, headlength=5),
    fontsize=9.5, fontweight="bold", color="#1e293b",
    bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#cbd5e1", alpha=0.9, lw=0.5)
)

ax1.set_title(f"(b) Inequality in adaptation burden (Gini = {gini:.2f})", fontsize=11.5, fontweight="bold", color="#1e293b")
ax1.set_xlabel("Cumulative Proportion of Grid Cells", fontsize=9.5)
ax1.set_ylabel("Cumulative Proportion of Exposure-Vulnerability Burden", fontsize=9.5)
ax1.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5, framealpha=0.95)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

fig.suptitle("Spatial association & inequality of the urban climate-adaptation burden", fontsize=14, fontweight="bold", color="#0f172a", y=0.965)
plt.subplots_adjust(left=0.075, right=0.965, top=0.88, bottom=0.115, wspace=0.22)

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Successfully generated Figure 14 (spatial inequality): {OUT_FIG}")
