"""Pilot step 13 - CELL-LEVEL adaptation priority (selective Pareto frontier).

The fabric-level Pareto (pilot_11) was uninformative: with five need-axes and only
seven fabrics every fabric was non-dominated. This step applies the same dominance
screen at the level of the 700 sampled grid cells, where it can be selective, and
ranks the cells with TOPSIS + Monte-Carlo weight robustness.

Need-axes (higher = more adaptation need), identical definitions to pilot_11:
  heat            = mean summer LST
  cooling_deficit = 1 - green fraction
  access_deficit  = 1 / (1 + intersection density 800 m)
  coastal_expo    = 1 / (1 + distance to coast km)
  social_vul      = SVI (ADNKS elderly share + age dependency), shifted >= 0

A cell is on the priority frontier if no other cell has >= need on ALL five axes
and > need on at least one. Outputs:
  data/03_processed/cell_priority.csv          (per-cell axes + flags + scores)
  outputs/tables/cell_pareto_summary.csv       (frontier composition by stratum)
  outputs/tables/cell_priority_top20.csv       (highest-priority cells)
  outputs/figures/priority_synthesis.png
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
PROC = os.path.join(PROJ, "data", "03_processed")
TABDIR = os.path.join(PROJ, "outputs", "tables")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
for d in (TABDIR, FIGDIR):
    os.makedirs(d, exist_ok=True)

df = pd.read_csv(IND).copy()
df["heat"] = df["lst_summer"]
df["cooling_deficit"] = 1 - df["f_green"]
df["access_deficit"] = 1 / (1 + df["inter_dens_800"])
df["coastal_expo"] = 1 / (1 + df["dist_coast_km"])
df["social_vul"] = df["svi"] - df["svi"].min()  # shift to >= 0 for TOPSIS
AX = ["heat", "cooling_deficit", "access_deficit", "coastal_expo", "social_vul"]
M = df[AX].to_numpy(float)
n = len(M)

# --- Pareto frontier (maximisation of need), vectorised over 700 cells ---
ge = (M[None, :, :] >= M[:, None, :]).all(axis=2)   # ge[i,j] = M[j] >= M[i] (all axes)
gt = (M[None, :, :] > M[:, None, :]).any(axis=2)    # gt[i,j] = M[j] >  M[i] (some axis)
dom = ge & gt                                       # dom[i,j] = j dominates i
np.fill_diagonal(dom, False)
df["pareto_frontier"] = ~dom.any(axis=1)

# --- TOPSIS ---
def topsis(M, w):
    N = M / np.sqrt((M ** 2).sum(0))
    V = N * w
    ideal, anti = V.max(0), V.min(0)
    dp = np.sqrt(((V - ideal) ** 2).sum(1))
    dn = np.sqrt(((V - anti) ** 2).sum(1))
    return dn / (dp + dn)

w_eq = np.ones(len(AX)) / len(AX)
P = M / M.sum(0); k = 1 / np.log(n)
with np.errstate(divide="ignore", invalid="ignore"):
    E = -k * (np.where(P > 0, P * np.log(P), 0.0)).sum(0)
w_ent = (1 - E) / (1 - E).sum()
df["topsis_equal"] = topsis(M, w_eq)
df["topsis_entropy"] = topsis(M, w_ent)

# Monte-Carlo weight robustness: rank distribution under 2000 random weightings
rng = np.random.default_rng(0)
R = np.zeros((2000, n))
for i in range(2000):
    w = rng.dirichlet(np.ones(len(AX)))
    R[i] = pd.Series(-topsis(M, w)).rank().to_numpy()  # rank 1 = highest priority
df["rank_mean"] = R.mean(0)
df["rank_p10"] = np.percentile(R, 10, axis=0)
df["rank_p90"] = np.percentile(R, 90, axis=0)

# --- save per-cell table ---
keep = ["sample_id", "stratum_name", "x", "y"] + AX + \
       ["pareto_frontier", "topsis_equal", "topsis_entropy",
        "rank_mean", "rank_p10", "rank_p90"]
df[keep].round(4).to_csv(os.path.join(PROC, "cell_priority.csv"), index=False)

# --- frontier composition by stratum ---
n_front = int(df["pareto_frontier"].sum())
comp = (df.groupby("stratum_name")
          .agg(n_cells=("pareto_frontier", "size"),
               n_frontier=("pareto_frontier", "sum"))
          .assign(share_of_frontier=lambda t: (t["n_frontier"] / n_front).round(3),
                  frontier_rate=lambda t: (t["n_frontier"] / t["n_cells"]).round(3))
          .sort_values("n_frontier", ascending=False)
          .reset_index())
comp.to_csv(os.path.join(TABDIR, "cell_pareto_summary.csv"), index=False)

top = df.sort_values("topsis_entropy", ascending=False).head(20)
top[["sample_id", "stratum_name"] + AX +
    ["topsis_entropy", "pareto_frontier", "rank_mean", "rank_p10", "rank_p90"]] \
    .round(3).to_csv(os.path.join(TABDIR, "cell_priority_top20.csv"), index=False)

print(f"N cells = {n}; on Pareto frontier = {n_front} ({100*n_front/n:.1f}%)")
print(f"entropy weights {dict(zip(AX, w_ent.round(2)))}")

# --- priority synthesis plot (3 panels: a, b, c) ---
g = df.groupby("stratum_name").agg(
    heat_f=("heat", "mean"),
    cooling_deficit_f=("cooling_deficit", "mean"),
    access_deficit_f=("access_deficit", "mean"),
    coastal_expo_f=("coastal_expo", "mean"),
    social_vul_f=("social_vul", "mean")
).reset_index()

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

colors_map = {
    "historic_core": "#E9B420",
    "grid_residential": "#DDB5B5",
    "apartment_block": "#EBCB9C",
    "waterfront_transformation": "#A0CBBF",
    "hillside_incremental": "#DEA6A3",
    "industrial_logistics": "#8E8E8D",
    "peripheral_expansion": "#C5AFD5"
}

strata_order = [
    "historic_core",
    "apartment_block",
    "waterfront_transformation",
    "hillside_incremental",
    "grid_residential",
    "industrial_logistics",
    "peripheral_expansion"
]

strata_labels = {
    "historic_core": "Historic Core",
    "apartment_block": "Apartment Block",
    "waterfront_transformation": "Waterfront Trans.",
    "hillside_incremental": "Hillside / Inc.",
    "grid_residential": "Grid Res.",
    "industrial_logistics": "Industrial / Log.",
    "peripheral_expansion": "Peripheral Exp."
}

fig = plt.figure(figsize=(17.5, 20.0), facecolor="#ffffff")
gs = GridSpec(2, 2, figure=fig, height_ratios=[1.0, 2.25], hspace=0.18, wspace=0.18)

# Panel a (top-left): Fabric-level priority (heat vs cooling deficit)
ax0 = fig.add_subplot(gs[0, 0])
ax0.set_facecolor("#ffffff")

for _, r in g.iterrows():
    s_name = r["stratum_name"]
    color = colors_map.get(s_name, "#8E8E8D")
    label_txt = strata_labels.get(s_name, s_name)
    size = 200 * r["access_deficit_f"] / g["access_deficit_f"].max() + 40
    
    ax0.scatter(r["heat_f"], r["cooling_deficit_f"], 
                s=size,
                color=color, label=label_txt,
                edgecolor="#1e293b", linewidth=1.0, zorder=3)
    
    ax0.annotate(label_txt, (r["heat_f"], r["cooling_deficit_f"]), fontsize=12.0,
                 fontweight="bold", color="#1e293b", xytext=(6, 6), textcoords="offset points")

ax0.set_xlabel("Mean Summer LST (°C)", fontsize=12)
ax0.set_ylabel("Cooling Deficit (1 - Green Cover fraction)", fontsize=12)
ax0.set_title("(a) Fabric-level priority space", loc="left", fontsize=15, fontweight="bold", color="#1e293b", pad=10)

size_vals = [0.05, 0.15, 0.25]
size_handles = []
for v in size_vals:
    sz = 200 * v / g["access_deficit_f"].max() + 40
    h = ax0.scatter([], [], s=sz, c="#94a3b8", edgecolor="#1e293b", alpha=0.75, linewidth=0.8, label=f"{v:.2f}")
    size_handles.append(h)

ax0.legend(handles=size_handles, title="Access Deficit (bubble size)", loc="lower right",
           fontsize=11.0, title_fontsize=11.5, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.95)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
for _sp in ["top", "right"]:
    ax0.spines[_sp].set_visible(False)

# Panel b (top-right): Cell-level priority (heat vs cooling deficit)
ax1 = fig.add_subplot(gs[0, 1])
ax1.set_facecolor("#ffffff")

int_ = df[~df["pareto_frontier"]]
fro = df[df["pareto_frontier"]]

ax1.scatter(int_["heat"], int_["cooling_deficit"], s=18, c="#cbd5e1",
            edgecolor="none", alpha=0.35, label=f"Dominated Cells (n={len(int_)})", zorder=2)

for s_name in strata_order:
    s_fro = fro[fro["stratum_name"] == s_name]
    if len(s_fro) == 0:
        continue
    color = colors_map.get(s_name, "#8E8E8D")
    label_txt = strata_labels.get(s_name, s_name)
    size = 25 + 120 * (s_fro["social_vul"] / df["social_vul"].max())
    
    ax1.scatter(s_fro["heat"], s_fro["cooling_deficit"],
                s=size,
                color=color, edgecolor="#1e293b", linewidth=0.5,
                label=f"{label_txt} Frontier (n={len(s_fro)})", zorder=3)

ax1.set_xlabel("Mean Summer LST (°C)", fontsize=12)
ax1.set_ylabel("Cooling Deficit (1 - Green Cover fraction)", fontsize=12)
ax1.set_title("(b) Cell-level multi-objective Pareto frontier", loc="left", fontsize=15, fontweight="bold", color="#1e293b", pad=10)

ax1.legend(loc="lower left", fontsize=11.0, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.95)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

# Panel c (full bottom): cell-level Pareto-frontier spatial map
ax2 = fig.add_subplot(gs[1, :])
ax2.set_facecolor("#ffffff")
gpkg12 = os.path.join(PROJ, "outputs", "figure_gpkgs", "figure_12_priority_synthesis.gpkg")
gpkg01 = os.path.join(PROJ, "outputs", "figure_gpkgs", "figure_01_study_area_map.gpkg")

if os.path.exists(gpkg12) and os.path.exists(gpkg01):
    priority_geo = gpd.read_file(gpkg12, layer="priority_cells")
    boundary = gpd.read_file(gpkg01, layer="study_boundary").to_crs(priority_geo.crs)
    coastline = gpd.read_file(gpkg01, layer="coastline").to_crs(priority_geo.crs)
    dom_geo = priority_geo[~priority_geo["pareto_frontier"].astype(bool)]
    front_geo = priority_geo[priority_geo["pareto_frontier"].astype(bool)]

    boundary.boundary.plot(ax=ax2, color="#64748b", linewidth=0.7, zorder=1)
    dom_geo.plot(ax=ax2, color="#d7dde5", edgecolor="none", alpha=0.75, zorder=2)
    for s_name in strata_order:
        part = front_geo[front_geo["stratum_name"] == s_name]
        if not part.empty:
            part.plot(ax=ax2, color=colors_map[s_name], edgecolor="#1e293b",
                      linewidth=0.45, zorder=4)
    coastline.plot(ax=ax2, color="#4f7f8c", linewidth=0.7, zorder=5)
    ax2.set_xlim(boundary.total_bounds[[0, 2]])
    ax2.set_ylim(boundary.total_bounds[[1, 3]])
    ax2.set_aspect("equal")

ax2.set_axis_off()
ax2.set_title("(c) Spatial distribution of priority cells", loc="left", fontsize=15, fontweight="bold", color="#1e293b", pad=10)

# Five-kilometre scale bar and north arrow
x0, x1 = ax2.get_xlim(); y0, y1 = ax2.get_ylim()
sx = x0 + 0.04 * (x1 - x0)
sy_bar = y0 + 0.05 * (y1 - y0)
sy_north = y0 + 0.14 * (y1 - y0)

ax2.plot([sx, sx + 5000], [sy_bar, sy_bar], color="#1e293b", linewidth=2.4, zorder=7)
ax2.plot([sx, sx], [sy_bar - 250, sy_bar + 250], color="#1e293b", linewidth=1.4, zorder=7)
ax2.plot([sx + 5000, sx + 5000], [sy_bar - 250, sy_bar + 250], color="#1e293b", linewidth=1.4, zorder=7)
ax2.text(sx + 2500, sy_bar + 400, "5 km", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1e293b", zorder=7)

ax2.annotate("N", xy=(sx + 2500, sy_north + 1500),
             xytext=(sx + 2500, sy_north - 500),
             ha="center", va="center", fontsize=12, fontweight="bold",
             arrowprops=dict(arrowstyle="-|>", color="#1e293b", lw=2.2), zorder=8)

legend_handles_c = [mpatches.Patch(color="#d7dde5", label="Dominated Cells")]
for s_name in strata_order:
    legend_handles_c.append(mpatches.Patch(color=colors_map[s_name], label=f"{strata_labels[s_name]} Frontier"))

leg = ax2.legend(handles=legend_handles_c, title="Map Key", loc="lower left", bbox_to_anchor=(0.015, 0.40),
                 fontsize=12.0, title_fontsize=13.0, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.95, ncol=1)
leg.get_title().set_fontweight("bold")

plt.subplots_adjust(left=0.04, right=0.96, top=0.96, bottom=0.02, wspace=0.18, hspace=0.14)

out_path = os.path.join(FIGDIR, "priority_synthesis.png")
fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)

import shutil
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(out_path, os.path.join(figs_cur, "priority_synthesis.png"))

print(f"\nwrote cell_priority.csv, cell_pareto_summary.csv, cell_priority_top20.csv, priority_synthesis.png")
