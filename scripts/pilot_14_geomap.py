"""Pilot step 14 - spatial map of adaptation-need clustering (Gi* and LISA).

Two polygon choropleth panels over the full urban census:
  (A) Getis-Ord Gi* hot/cold spots of the need score.
  (B) Local Moran (LISA) cluster types of the need score.

Map base (filled sea + land, furniture) matches Figure 1 for cross-figure
consistency. Reads precomputed geostatistics; no analysis is recomputed here.

Inputs : data/03_processed/cell_geostats.csv, data/02_interim/grid_250m_sample.gpkg,
         boundaries (ilce.shp, izmir_study_boundary.gpkg)
Output : outputs/figures/geostats_map.png
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle, Polygon as MplPolygon, FancyBboxPatch
from shapely.ops import unary_union

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
FIGDIR = os.path.join(PROJ, "outputs", "figures")
GEO_PATH = os.path.join(PROJ, "data", "03_processed", "cell_geostats.csv")
SAMPLE_PATH = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
BND_PATH = os.path.join(PROJ, "data", "00_external", "boundaries", "izmir_study_boundary.gpkg")
ILCE_PATH = os.path.join(PROJ, "data", "00_external", "boundaries", "ilce.shp")
CRS = 32635
os.makedirs(FIGDIR, exist_ok=True)

COL_SEA, COL_LAND, COL_BORDER = "#CBD5E1", "#ffffff", "#94A3B8"
COL_FUR, COL_INK, COL_LABEL = "#1E293B", "#1E293B", "#334155"
COL_NS = "#E5E7EB"  # not-significant cells (neutral grey, distinct from sea)

GI = {"hot": "#E9B420", "cold": "#A0CBBF", "ns": COL_NS}
LI = {"HH": "#E9B420", "LL": "#A0CBBF", "LH": "#C5AFD5", "HL": "#EBCB9C", "ns": COL_NS}
ORDER_GI = ["ns", "cold", "hot"]          # draw order: ns first
ORDER_LI = ["ns", "LH", "HL", "LL", "HH"]
LEG_GI = ["hot", "cold", "ns"]            # legend order: salient first
LEG_LI = ["HH", "LL", "HL", "LH", "ns"]
LABELS_GI = {"hot": "Hot spot (high need)", "cold": "Cold spot (low need)", "ns": "Not significant"}
LABELS_LI = {"HH": "High–High (cluster)", "LL": "Low–Low (cluster)", "LH": "Low–High (outlier)",
             "HL": "High–Low (outlier)", "ns": "Not significant"}

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "text.color": "#1e293b", "axes.labelcolor": "#334155",
})


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
geo = pd.read_csv(GEO_PATH)
samp = gpd.read_file(SAMPLE_PATH).to_crs(CRS)
gdf = samp[["sample_id", "geometry"]].merge(geo, on="sample_id", how="inner")
bnd = gpd.read_file(BND_PATH).to_crs(CRS)
ilce = gpd.read_file(ILCE_PATH)
if ilce.crs is None:
    ilce = ilce.set_crs(5253, allow_override=True)
ilce = ilce.to_crs(CRS)
land_all = gpd.GeoSeries([unary_union(ilce.geometry.values)], crs=CRS)

minx, miny, maxx, maxy = bnd.total_bounds
xlim = (minx - 4000, maxx + 4000)
ylim = (miny - 4000, maxy + 4000)

fig, axes = plt.subplots(1, 2, figsize=(14.6, 6.7), facecolor="#ffffff")
fig.subplots_adjust(left=0.015, right=0.985, top=0.88, bottom=0.03, wspace=0.05)


def panel(ax, col, cmap, labels_map, draw_order, leg_order, title):
    ax.set_facecolor("white")
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0],
                           facecolor=COL_SEA, edgecolor="none", zorder=0))
    land_all.plot(ax=ax, facecolor=COL_LAND, edgecolor=COL_BORDER, linewidth=0.4, zorder=1)
    for cat in draw_order:
        sub = gdf[gdf[col] == cat]
        if len(sub):
            sub.plot(ax=ax, facecolor=cmap[cat], edgecolor="none",
                     zorder=(2 if cat == "ns" else 3))
    bnd.boundary.plot(ax=ax, color=COL_FUR, linewidth=1.4, zorder=4)

    ax.set_xlim(xlim); ax.set_ylim(ylim); ax.set_aspect("equal")
    ax.set_title(title, fontsize=12, fontweight="bold", color=COL_INK, pad=8, loc="left")
    scale_bar(ax); north_arrow(ax)
    ax.text(0.985, 0.022, "EPSG:32635 · UTM 35N", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=6.8, style="italic", color=COL_LABEL, zorder=8)
    add_neatline(ax)

    counts = gdf[col].value_counts().to_dict()
    handles = [Patch(facecolor=cmap[c], edgecolor="#64748B", linewidth=0.5,
                     label=f"{labels_map[c]}  (n = {counts.get(c, 0):,})")
               for c in leg_order if counts.get(c, 0) > 0]
    ax.legend(handles=handles, loc="lower right", fontsize=9, framealpha=0.96,
              facecolor="#ffffff", edgecolor=COL_BORDER, borderpad=0.7)


panel(axes[0], "gi_hot", GI, LABELS_GI, ORDER_GI, LEG_GI,
      "(a) Getis-Ord $G_i^*$ hot / cold spots of adaptation need")
panel(axes[1], "lisa", LI, LABELS_LI, ORDER_LI, LEG_LI,
      "(b) Local Moran (LISA) clusters of adaptation need")

n = len(gdf)
fig.suptitle(f"Spatial concentration of adaptation need — full urban census "
             f"(N = {n:,}; KNN spatial weights, k = 8)",
             fontsize=14, fontweight="bold", color="#0f172a", y=0.965)

# User manual figure override guard - preserve C:\Users\YE\Downloads\fig9.png
print("Using manual Figure 9 from user provided file. Skipping automated overwrite.")
# out_path = os.path.join(FIGDIR, "geostats_map.png")
# fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)
