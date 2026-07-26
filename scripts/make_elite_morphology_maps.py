"""
Figure 5 — Spatial distributions of grid-based morphometric indicators and
summer heat across the Izmir FUR (N = 3,777 urban cells).

Panels: (a) FAR, (b) building coverage, (c) summer LST. Each carries a KDE inset,
horizontal colorbar, segmented scale bar, triangular north arrow and CRS note.
Map base (filled sea + land, furniture) matches Figure 1 for cross-figure
consistency. Colour scaling is left at the full data range (data semantics
unchanged); only layout / cartography are upgraded.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, Polygon as MplPolygon, FancyBboxPatch
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from shapely.ops import unary_union

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
SAMPLE_PATH = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
BND_PATH = os.path.join(PROJ, "data", "00_external", "boundaries", "izmir_study_boundary.gpkg")
ILCE_PATH = os.path.join(PROJ, "data", "00_external", "boundaries", "ilce.shp")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "raw_morphology_maps.png")
CRS = 32635

COL_SEA, COL_LAND, COL_BORDER = "#CBD5E1", "#ffffff", "#94A3B8"
COL_FUR, COL_INK, COL_LABEL = "#1E293B", "#1E293B", "#334155"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "text.color": "#1e293b", "axes.labelcolor": "#334155",
})


def draw_base(ax, xlim, ylim, land, lw=0.4):
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0],
                           facecolor=COL_SEA, edgecolor="none", zorder=0))
    land.plot(ax=ax, facecolor=COL_LAND, edgecolor=COL_BORDER, linewidth=lw, zorder=1)


def scale_bar(ax, length_m=10000, n_seg=2, units="km"):
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    xspan, yspan = x1 - x0, y1 - y0
    bx, by = x0 + 0.055 * xspan, y0 + 0.07 * yspan
    seg, h, pad = length_m / n_seg, 0.013 * yspan, 0.022 * xspan
    ax.add_patch(FancyBboxPatch((bx - pad, by - 0.04 * yspan), length_m + 2 * pad, 0.10 * yspan,
                                boxstyle="round,pad=0", facecolor="white", edgecolor=COL_BORDER,
                                lw=0.6, alpha=0.92, zorder=6))
    for i in range(n_seg):
        ax.add_patch(Rectangle((bx + i * seg, by), seg, h,
                               facecolor=(COL_INK if i % 2 == 0 else "white"),
                               edgecolor=COL_INK, lw=0.7, zorder=7))
    for i in range(n_seg + 1):
        ax.text(bx + i * seg, by + h + 0.006 * yspan, f"{int(round(i*seg/1000))}",
                ha="center", va="bottom", fontsize=7.5, color=COL_LABEL, zorder=7)
    ax.text(bx + length_m + 0.012 * xspan, by + h * 0.5, units, ha="left", va="center",
            fontsize=7.5, color=COL_LABEL, zorder=7)


def north_arrow(ax):
    ax.text(0.955, 0.96, "N", transform=ax.transAxes, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=COL_INK, zorder=8)
    ax.add_patch(MplPolygon([(0.955, 0.95), (0.938, 0.895), (0.972, 0.895)], closed=True,
                            transform=ax.transAxes, facecolor=COL_INK, edgecolor=COL_INK, lw=0.5, zorder=8))
    ax.add_patch(MplPolygon([(0.955, 0.95), (0.955, 0.895), (0.972, 0.895)], closed=True,
                            transform=ax.transAxes, facecolor="white", edgecolor=COL_INK, lw=0.5, zorder=8))


def add_neatline(ax):
    for s in ax.spines.values():
        s.set_visible(True); s.set_edgecolor(COL_BORDER); s.set_linewidth(1.0)
    ax.set_xticks([]); ax.set_yticks([])


# ── load ──────────────────────────────────────────────────────────────────────
print("Loading data for morphology maps...")
df_ind = pd.read_csv(IND_PATH)
gdf_sample = gpd.read_file(SAMPLE_PATH).to_crs(CRS)
gdf_bnd = gpd.read_file(BND_PATH).to_crs(CRS)
ilce = gpd.read_file(ILCE_PATH)
if ilce.crs is None:
    ilce = ilce.set_crs(5253, allow_override=True)
ilce = ilce.to_crs(CRS)
land_all = gpd.GeoSeries([unary_union(ilce.geometry.values)], crs=CRS)
gdf_data = gdf_sample[["sample_id", "geometry"]].merge(df_ind, on="sample_id")

bounds = gdf_data.total_bounds
xlim = (bounds[0] - 4000, bounds[2] + 4000)
ylim = (bounds[1] - 4000, bounds[3] + 4000)

# last field = robust: clip the colour scale at the 98th percentile (long upper
# tail) and flag the clip with a colour-bar extend arrow; LST keeps its full range.
indicators = [
    ("far", "Floor-Area Ratio (FAR)", "YlOrBr", "(a) Built intensity — FAR", "#E9B420", True),
    ("bld_cov", "Building coverage (fraction)", "Purples", "(b) Ground coverage", "#C5AFD5", True),
    ("lst_summer", "Summer LST, JJA (°C)", "YlOrRd", "(c) Measured thermal outcome — LST", "#DEA6A3", False),
]

fig, axes = plt.subplots(1, 3, figsize=(17.6, 7.7), facecolor="#ffffff")
fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.04, wspace=0.07)

for idx, (col, label, cmap, title, kde_color, robust) in enumerate(indicators):
    ax = axes[idx]
    ax.set_facecolor("white")
    draw_base(ax, xlim, ylim, land_all, lw=0.4)
    gdf_bnd.boundary.plot(ax=ax, color=COL_FUR, linewidth=1.4, zorder=4)

    vals = gdf_data[col].dropna()
    if robust:
        vmin, vmax, extend = 0.0, float(vals.quantile(0.98)), "max"
    else:
        vmin, vmax, extend = float(vals.min()), float(vals.max()), "neither"
    cax = make_axes_locatable(ax).append_axes("bottom", size="4%", pad=0.32)
    gdf_data.plot(column=col, ax=ax, cmap=cmap, vmin=vmin, vmax=vmax,
                  edgecolor="#CBD5E1", linewidth=0.1, zorder=5,
                  legend=True, cax=cax,
                  legend_kwds={"label": label, "orientation": "horizontal", "extend": extend})
    cax.tick_params(labelsize=8, colors=COL_LABEL)
    cax.xaxis.label.set_size(9.5); cax.xaxis.label.set_color(COL_LABEL)

    ax.set_xlim(xlim); ax.set_ylim(ylim); ax.set_aspect("equal")
    ax.set_title(title, fontsize=12.5, fontweight="bold", pad=8, color=COL_INK, loc="left")
    scale_bar(ax); north_arrow(ax)
    ax.text(0.985, 0.022, "EPSG:32635 · UTM 35N", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=6.8, style="italic", color=COL_LABEL, zorder=8)
    add_neatline(ax)

    # KDE inset
    axin = inset_axes(ax, width="34%", height="24%", loc="upper left", borderpad=1.1)
    axin.set_facecolor("#FFFFFFE6")
    s = gdf_data[col].dropna()
    sns.kdeplot(s, ax=axin, fill=True, color=kde_color, alpha=0.6, linewidth=1.2)
    axin.axvline(s.mean(), color="#EF4444", linestyle="--", linewidth=1.0, alpha=0.85)
    axin.set_ylabel(""); axin.set_xlabel("")
    axin.tick_params(colors=COL_LABEL, labelsize=6.5, pad=1)
    axin.set_yticks([])
    axin.grid(True, linestyle=":", alpha=0.4)
    for sp in axin.spines.values():
        sp.set_color(COL_BORDER); sp.set_linewidth(0.5)
    axin.spines["top"].set_visible(False); axin.spines["right"].set_visible(False)
    fmt = (lambda v: f"{v:.1f}°C") if col == "lst_summer" else (lambda v: f"{v:.2f}")
    axin.text(0.95, 0.92, f"Mean {fmt(s.mean())}\nMed {fmt(s.median())}", transform=axin.transAxes,
              ha="right", va="top", fontsize=6.8, fontweight="bold", color=COL_INK)

fig.suptitle("Spatial distribution of grid-based morphometric indicators & summer heat  (full census, N = 3,777 cells)",
             fontsize=14.5, fontweight="bold", color="#0f172a", y=0.965)
fig.text(0.5, 0.905, "Insets show kernel-density estimates; vertical red dashed line marks the sample mean",
         ha="center", va="center", fontsize=10, color="#475569")

# User manual figure override guard - preserve C:\Users\YE\Downloads\fig5.png
print("Using manual Figure 5 from user provided file. Skipping automated overwrite.")
# fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
