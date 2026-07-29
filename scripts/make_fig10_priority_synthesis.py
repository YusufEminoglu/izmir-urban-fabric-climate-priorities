import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import pandas as pd
import numpy as np
import geopandas as gpd
from PIL import Image, ImageDraw, ImageFont

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
PRIO_PATH = os.path.join(PROJ, "data", "03_processed", "cell_priority.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "figure10.png")

df_ind = pd.read_csv(IND_PATH)
df_prio = pd.read_csv(PRIO_PATH)
df = pd.merge(df_ind, df_prio, on="sample_id", suffixes=("", "_prio"))

df["cooling_deficit"] = 1 - df["f_green"]
df["access_deficit"] = 1 / (1 + df["inter_dens_800"])
df["coastal_expo"] = 1 / (1 + df["dist_coast_km"])
df["social_vul"] = df["svi"] - df["svi"].min()
df["heat"] = df["lst_summer"]

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

# Panel a
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
    
    if s_name == "industrial_logistics":
        ax0.annotate(label_txt, (r["heat_f"], r["cooling_deficit_f"]), fontsize=12.0,
                     fontweight="bold", color="#1e293b", xytext=(-8, 6), textcoords="offset points", ha="right")
    else:
        ax0.annotate(label_txt, (r["heat_f"], r["cooling_deficit_f"]), fontsize=12.0,
                     fontweight="bold", color="#1e293b", xytext=(6, 6), textcoords="offset points")

ax0.set_xlabel("Mean Summer LST (°C)", fontsize=12)
ax0.set_ylabel("Cooling Deficit (1 - Green Cover fraction)", fontsize=12)

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

# Panel b
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

ax1.legend(loc="lower left", fontsize=11.0, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.95)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

# Panel c
ax2 = fig.add_subplot(gs[1, :])
ax2.set_facecolor("#ffffff")
gpkg12 = os.path.join(PROJ, "outputs", "figure_gpkgs", "figure_12_priority_synthesis.gpkg")
gpkg01 = os.path.join(PROJ, "outputs", "figure_01_study_area_map.gpkg")

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

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)

img = Image.open(OUT_FIG).convert("RGB")
draw = ImageDraw.Draw(img)
w, h = img.size

try:
    font = ImageFont.truetype("arialbd.ttf", 92)
except:
    font = ImageFont.truetype("arial.ttf", 92)

draw.rectangle([280, 100, 470, 205], fill=(255, 255, 255))
draw.text((310, 110), "(a)", fill=(0, 0, 0), font=font)

draw.rectangle([w//2 + 260, 100, w//2 + 450, 205], fill=(255, 255, 255))
draw.text((w//2 + 290, 110), "(b)", fill=(0, 0, 0), font=font)

draw.rectangle([280, 2070, 470, 2175], fill=(255, 255, 255))
draw.text((310, 2080), "(c)", fill=(0, 0, 0), font=font)

img.save(OUT_FIG)
print(f"Successfully generated Figure 10: {OUT_FIG}")
