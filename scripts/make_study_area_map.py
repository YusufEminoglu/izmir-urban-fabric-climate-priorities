"""
Figure 1 — Izmir functional urban region study area map.

Panel (a): regional context (districts, filled sea, FUR outline, labelled
           central districts, subtle hillshade, locator inset).
Panel (b): provisional fabric strata over the full urban census (N = 3,777).

Journal-quality cartography per docs/notes/figure_style_guide.md:
filled land/sea, segmented scale bar, triangular north arrow, locator inset,
shared bottom legend, neatline frames, sans-serif typography, 300 dpi.
"""
import os
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.windows import from_bounds as window_from_bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Patch, Rectangle, Polygon as MplPolygon, FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath
from shapely.ops import unary_union
from shapely.geometry import box

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
BND_PATH = os.path.join(PROJ, "data", "00_external", "boundaries", "izmir_study_boundary.gpkg")
ILCE_PATH = os.path.join(PROJ, "data", "00_external", "boundaries", "ilce.shp")
STRATA_PATH = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban_strata.gpkg")
DEM_PATH = os.path.join(PROJ, "data", "01_raw", "dem", "izmir_dem_glo30_30m.tif")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "study_area_map.png")
CRS = 32635

# ── Style guide palette ───────────────────────────────────────────────────────
COL_SEA       = "#CBD5E1"   # Slate-300  (water bodies)
COL_LAND      = "#ffffff"   # Slate-100  (land surface)
COL_BORDER    = "#94A3B8"   # Slate-400  (district outlines)
COL_FUR       = "#1E293B"   # Slate-800  (FUR boundary / ink)
COL_INK       = "#1E293B"
COL_LABEL     = "#334155"   # Slate-700
COL_FACE      = "#ffffff"   # Slate-50   (figure background)

STRATA_COLORS = {
    1: "#E9B420",  # Historic core           — Primary Gold
    2: "#DDB5B5",  # Grid residential        — Soft Pink
    3: "#EBCB9C",  # Apartment block         — Soft Orange
    4: "#A0CBBF",  # Waterfront transformation — Soft Teal
    5: "#DEA6A3",  # Hillside / incremental  — Soft Rose
    6: "#8E8E8D",  # Industrial / logistics  — Secondary Grey
    7: "#C5AFD5",  # Peripheral expansion    — Soft Purple
}
STRATA_NAMES = {
    1: "Historic core", 2: "Grid residential", 3: "Apartment block",
    4: "Waterfront transformation", 5: "Hillside / incremental",
    6: "Industrial / logistics", 7: "Peripheral expansion",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "axes.linewidth": 0.8,
    "savefig.dpi": 300,
})

# ── Helpers ───────────────────────────────────────────────────────────────────
def geom_to_path(geom):
    """Compound matplotlib Path from a (Multi)Polygon, holes included."""
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    verts, codes = [], []
    for poly in polys:
        for ring in [poly.exterior, *poly.interiors]:
            xy = np.asarray(ring.coords)
            if len(xy) < 3:
                continue
            verts.extend(xy)
            codes.append(MplPath.MOVETO)
            codes.extend([MplPath.LINETO] * (len(xy) - 2))
            codes.append(MplPath.CLOSEPOLY)
    return MplPath(np.asarray(verts), codes)


def add_neatline(ax, color=COL_BORDER, lw=1.0):
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_edgecolor(color)
        s.set_linewidth(lw)
    ax.set_xticks([]); ax.set_yticks([])


def draw_base(ax, xlim, ylim, land, sea=COL_SEA, land_c=COL_LAND, lw=0.4):
    """Fill the frame with sea, overlay dissolved land; the gulf appears as gaps."""
    ax.add_patch(Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0],
                            facecolor=sea, edgecolor="none", zorder=0))
    land.plot(ax=ax, facecolor=land_c, edgecolor=COL_BORDER, linewidth=lw, zorder=1)


def add_hillshade(ax, land_view, xlim, ylim, alpha=0.27):
    """Subtle grey hillshade from the DEM, clipped to land within the view."""
    try:
        with rasterio.open(DEM_PATH) as r:
            win = window_from_bounds(xlim[0], ylim[0], xlim[1], ylim[1], r.transform)
            scale = max(1, int(max(win.width, win.height) / 1400))
            out_h = max(1, int(win.height // scale)); out_w = max(1, int(win.width // scale))
            dem = r.read(1, window=win, out_shape=(out_h, out_w),
                         boundless=True, fill_value=np.nan).astype("float64")
        dem = np.where(np.isfinite(dem), dem, np.nanmedian(dem[np.isfinite(dem)]))
        az, alt = np.deg2rad(315), np.deg2rad(45)
        dy, dx = np.gradient(dem, 30.0 * scale)
        slope = np.pi / 2 - np.arctan(np.hypot(dx, dy))
        aspect = np.arctan2(-dx, dy)
        hs = (np.sin(alt) * np.sin(slope) +
              np.cos(alt) * np.cos(slope) * np.cos(az - aspect))
        hs = np.clip((hs - hs.min()) / (np.ptp(hs) + 1e-9), 0, 1)
        im = ax.imshow(hs, cmap="gray", extent=[xlim[0], xlim[1], ylim[0], ylim[1]],
                       origin="upper", alpha=alpha, zorder=2, interpolation="bilinear")
        clip = PathPatch(geom_to_path(land_view), transform=ax.transData,
                         facecolor="none", edgecolor="none")
        ax.add_patch(clip); im.set_clip_path(clip)
    except Exception as e:  # hillshade is a non-critical enhancement
        print(f"  [hillshade skipped: {e}]")


def scale_bar(ax, length_m=10000, n_seg=2, units="km"):
    """Segmented black/white scale bar on a white pill, lower-left of the axes."""
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    xspan, yspan = x1 - x0, y1 - y0
    bx = x0 + 0.055 * xspan
    by = y0 + 0.075 * yspan
    seg = length_m / n_seg
    h = 0.013 * yspan
    pad = 0.022 * xspan
    ax.add_patch(FancyBboxPatch((bx - pad, by - 0.045 * yspan),
                                length_m + 2 * pad, 0.105 * yspan,
                                boxstyle="round,pad=0", mutation_aspect=1,
                                facecolor="white", edgecolor=COL_BORDER, lw=0.6,
                                alpha=0.92, zorder=6))
    for i in range(n_seg):
        ax.add_patch(Rectangle((bx + i * seg, by), seg, h,
                               facecolor=(COL_INK if i % 2 == 0 else "white"),
                               edgecolor=COL_INK, lw=0.7, zorder=7))
    for i in range(n_seg + 1):
        val = int(round(i * seg / 1000))
        ax.text(bx + i * seg, by + h + 0.006 * yspan, f"{val}",
                ha="center", va="bottom", fontsize=7.5, color=COL_LABEL, zorder=7)
    ax.text(bx + length_m + 0.012 * xspan, by + h * 0.5, units,
            ha="left", va="center", fontsize=7.5, color=COL_LABEL, zorder=7)


def north_arrow(ax):
    """Clean filled triangular north arrow with 'N', upper-right of the axes."""
    ax.text(0.962, 0.965, "N", transform=ax.transAxes, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=COL_INK, zorder=8)
    tri = MplPolygon([(0.962, 0.955), (0.945, 0.90), (0.979, 0.90)],
                     closed=True, transform=ax.transAxes,
                     facecolor=COL_INK, edgecolor=COL_INK, lw=0.5, zorder=8)
    ax.add_patch(tri)
    ax.add_patch(MplPolygon([(0.962, 0.955), (0.962, 0.90), (0.979, 0.90)],
                            closed=True, transform=ax.transAxes,
                            facecolor="white", edgecolor=COL_INK, lw=0.5, zorder=8))


# ── Load layers ───────────────────────────────────────────────────────────────
print("Loading layers for study area map...")
bnd = gpd.read_file(BND_PATH).to_crs(CRS)
ilce = gpd.read_file(ILCE_PATH)
if ilce.crs is None:
    ilce = ilce.set_crs(5253, allow_override=True)
ilce = ilce.to_crs(CRS)
strata = gpd.read_file(STRATA_PATH).to_crs(CRS)

land_all = gpd.GeoSeries([unary_union(ilce.geometry.values)], crs=CRS)

minx, miny, maxx, maxy = bnd.total_bounds
xlim = (minx - 4000, maxx + 4000)
ylim = (miny - 4000, maxy + 4000)
land_view = land_all.clip(box(*xlim, *ylim)).union_all()

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.0), facecolor=COL_FACE)
fig.subplots_adjust(left=0.012, right=0.988, top=0.925, bottom=0.15, wspace=0.04)

# ---- Panel (a): regional context ----
ax0 = axes[0]
ax0.set_facecolor("white")
draw_base(ax0, xlim, ylim, land_all, lw=0.5)
add_hillshade(ax0, land_view, xlim, ylim)
ilce.boundary.plot(ax=ax0, color=COL_BORDER, linewidth=0.5, zorder=3)
bnd.boundary.plot(ax=ax0, color=COL_FUR, linewidth=1.8, zorder=5)

district_labels = {
    "KONAK": "Konak", "BORNOVA": "Bornova", "BUCA": "Buca", "BAYRAKLI": "Bayraklı",
    "KARŞIYAKA": "Karşıyaka", "ÇİĞLİ": "Çiğli", "BALÇOVA": "Balçova", "GAZİEMİR": "Gaziemir",
}
for _, row in ilce.iterrows():
    nm = row.get("ADINUMARAS")
    if nm in district_labels:
        p = row.geometry.representative_point()
        if xlim[0] < p.x < xlim[1] and ylim[0] < p.y < ylim[1]:
            ax0.text(p.x, p.y, district_labels[nm], fontsize=8.5, fontweight="bold",
                     ha="center", va="center", color=COL_INK, zorder=9,
                     path_effects=[pe.withStroke(linewidth=2.4, foreground="white")])

ax0.set_xlim(xlim); ax0.set_ylim(ylim); ax0.set_aspect("equal")
ax0.set_title("(a) İzmir Functional Urban Region — Context",
              fontsize=12, fontweight="bold", color=COL_INK, pad=8, loc="left")
scale_bar(ax0); north_arrow(ax0)
ax0.text(0.985, 0.025, "EPSG:32635 · UTM 35N", transform=ax0.transAxes,
         ha="right", va="bottom", fontsize=7, style="italic", color=COL_LABEL, zorder=8)
add_neatline(ax0)

# locator inset: full province + FUR study box
iax = ax0.inset_axes([0.015, 0.62, 0.30, 0.36])
iax.set_facecolor("white")
pminx, pminy, pmaxx, pmaxy = ilce.total_bounds
iax.add_patch(Rectangle((pminx, pminy), pmaxx - pminx, pmaxy - pminy,
                        facecolor=COL_SEA, edgecolor="none", zorder=0))
land_all.plot(ax=iax, facecolor=COL_LAND, edgecolor=COL_BORDER, linewidth=0.3, zorder=1)
bnd.boundary.plot(ax=iax, color="#C0392B", linewidth=1.1, zorder=3)
iax.set_xlim(pminx, pmaxx); iax.set_ylim(pminy, pmaxy); iax.set_aspect("equal")
iax.set_title("İzmir Province", fontsize=7.5, color=COL_LABEL, pad=2)
for s in iax.spines.values():
    s.set_edgecolor(COL_BORDER); s.set_linewidth(0.7)
iax.set_xticks([]); iax.set_yticks([])

# ---- Panel (b): provisional fabric strata ----
ax1 = axes[1]
ax1.set_facecolor("white")
draw_base(ax1, xlim, ylim, land_all, lw=0.35)
for k in range(1, 8):
    sub = strata[strata["stratum"] == k]
    if len(sub):
        sub.plot(ax=ax1, facecolor=STRATA_COLORS[k], edgecolor=STRATA_COLORS[k],
                 linewidth=0.05, zorder=3)
bnd.boundary.plot(ax=ax1, color=COL_FUR, linewidth=1.4, zorder=5)
ax1.set_xlim(xlim); ax1.set_ylim(ylim); ax1.set_aspect("equal")
ax1.set_title("(b) Provisional Fabric Strata — full census (N = 3,777, 250 m cells)",
              fontsize=12, fontweight="bold", color=COL_INK, pad=8, loc="left")
scale_bar(ax1); north_arrow(ax1)
ax1.text(0.985, 0.025, "EPSG:32635 · UTM 35N", transform=ax1.transAxes,
         ha="right", va="bottom", fontsize=7, style="italic", color=COL_LABEL, zorder=8)
add_neatline(ax1)

# ---- shared bottom legend ----
counts = strata["stratum"].value_counts()
legend_elems = [
    Patch(facecolor=STRATA_COLORS[k], edgecolor=COL_INK, linewidth=0.5,
          label=f"{STRATA_NAMES[k]}  (n = {int(counts.get(k, 0)):,})")
    for k in range(1, 8)
]
fig.legend(handles=legend_elems, loc="lower center", ncol=4, fontsize=9,
           frameon=True, framealpha=0.95, facecolor="white", edgecolor=COL_BORDER,
           bbox_to_anchor=(0.5, 0.01), columnspacing=1.6, handlelength=1.4,
           borderpad=0.7, title="Provisional fabric strata",
           title_fontsize=9.5)

plt.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

import shutil
outputs_fig = os.path.dirname(OUT_FIG)
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(OUT_FIG, os.path.join(outputs_fig, "fig1.png"))
shutil.copy2(OUT_FIG, os.path.join(figs_cur, "study_area_map.png"))
shutil.copy2(OUT_FIG, os.path.join(figs_cur, "fig1.png"))

print(f"Successfully generated study area map: {OUT_FIG}")
