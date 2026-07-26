"""Pilot step 1 - build the 250 m analysis grid and apply exclusions.

Inputs (EPSG:32635):
  data/00_external/boundaries/izmir_study_boundary.gpkg
  data/01_raw/worldcover/izmir_worldcover2021_10m.tif   (ESA WorldCover classes)
  data/01_raw/dem/izmir_slope_glo30_30m.tif             (slope %)
Output:
  data/02_interim/grid_250m_full.gpkg     all cells intersecting the boundary, with attributes
  data/02_interim/grid_250m_urban.gpkg    cells kept after exclusion (urban fabric)
Exclusion: slope_mean > 15%, water-dominated cells, and cells with too little built cover.
WorldCover classes: 10 tree, 20 shrub, 30 grass, 40 crop, 50 built, 60 bare, 80 water, 90 wetland.
"""
import os
import numpy as np
import geopandas as gpd
import shapely
from exactextract import exact_extract

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
BOUNDARY = os.path.join(PROJ, "data", "00_external", "boundaries", "izmir_study_boundary.gpkg")
WC = os.path.join(PROJ, "data", "01_raw", "worldcover", "izmir_worldcover2021_10m.tif")
SLOPE = os.path.join(PROJ, "data", "01_raw", "dem", "izmir_slope_glo30_30m.tif")
OUT_DIR = os.path.join(PROJ, "data", "02_interim")
os.makedirs(OUT_DIR, exist_ok=True)
CELL = 250.0
BUILT_MIN = 0.10      # min built fraction to count as urban fabric
WATER_MAX = 0.50      # drop water-dominated cells
SLOPE_MAX = 15.0      # exclude steep cells (%)

# --- build fishnet aligned to a 250 m origin, covering the boundary ---
bnd = gpd.read_file(BOUNDARY).to_crs(32635)
geom = bnd.union_all()
minx, miny, maxx, maxy = geom.bounds
x0 = np.floor(minx / CELL) * CELL
y0 = np.floor(miny / CELL) * CELL
nx = int(np.ceil((maxx - x0) / CELL))
ny = int(np.ceil((maxy - y0) / CELL))
print(f"fishnet {nx} x {ny} = {nx*ny} candidate cells")

xs = x0 + np.arange(nx) * CELL
ys = y0 + np.arange(ny) * CELL
gx, gy = np.meshgrid(xs, ys)
gx = gx.ravel(); gy = gy.ravel()
cells = shapely.box(gx, gy, gx + CELL, gy + CELL)
grid = gpd.GeoDataFrame(
    {"col": np.tile(np.arange(nx), ny), "row": np.repeat(np.arange(ny), nx)},
    geometry=cells, crs=32635,
)
# keep only cells intersecting the study polygon
grid = grid[grid.intersects(geom)].reset_index(drop=True)
grid["cell_id"] = np.arange(len(grid))
print(f"cells intersecting boundary: {len(grid)}")

# --- zonal stats ---
print("extracting WorldCover fractions ...")
wc = exact_extract(WC, grid, ["unique", "frac"], output="pandas", include_cols=["cell_id"])
print("extracting slope mean ...")
sl = exact_extract(SLOPE, grid, ["mean"], output="pandas", include_cols=["cell_id"])

# expand aligned (unique, frac) arrays into one fraction column per class
classes = [10, 20, 30, 40, 50, 60, 80, 90]
frac_mat = np.zeros((len(wc), max(classes) + 1), dtype="float32")
for i, (u, f) in enumerate(zip(wc["unique"].to_numpy(), wc["frac"].to_numpy())):
    u = np.atleast_1d(u).astype(int); f = np.atleast_1d(f).astype(float)
    for cls, fr in zip(u, f):
        if 0 <= cls <= max(classes):
            frac_mat[i, cls] = fr
wc_id = wc["cell_id"].to_numpy()
fdf = {c: frac_mat[:, c] for c in classes}

sl = sl.set_index("cell_id")
grid = grid.set_index("cell_id")
import pandas as pd
fdf = pd.DataFrame(fdf, index=wc_id)

grid["f_tree"] = fdf[10]
grid["f_shrub"] = fdf[20]
grid["f_grass"] = fdf[30]
grid["f_crop"] = fdf[40]
grid["f_built"] = fdf[50]
grid["f_bare"] = fdf[60]
grid["f_water"] = fdf[80]
grid["f_wetland"] = fdf[90]
grid["f_green"] = grid["f_tree"] + grid["f_shrub"] + grid["f_grass"]
grid["slope_mean"] = sl["mean"].replace(-9999.0, np.nan)
grid = grid.reset_index()

grid.to_file(os.path.join(OUT_DIR, "grid_250m_full.gpkg"), driver="GPKG")

# --- exclusion ---
keep = (
    (grid["f_built"] >= BUILT_MIN)
    & (grid["f_water"] <= WATER_MAX)
    & (grid["slope_mean"] <= SLOPE_MAX)
)
urban = grid[keep].reset_index(drop=True)
urban.to_file(os.path.join(OUT_DIR, "grid_250m_urban.gpkg"), driver="GPKG")

print("\n=== RESULT ===")
print(f"full grid cells:   {len(grid)}")
print(f"urban (kept):      {len(urban)}  ({100*len(urban)/len(grid):.1f}%)")
print(f"  dropped low-built: {(grid['f_built'] < BUILT_MIN).sum()}")
print(f"  dropped water:     {(grid['f_water'] > WATER_MAX).sum()}")
print(f"  dropped steep:     {(grid['slope_mean'] > SLOPE_MAX).sum()}")
print(f"urban built frac:  median {urban['f_built'].median():.2f}  mean {urban['f_built'].mean():.2f}")
print(f"urban slope %%:     median {urban['slope_mean'].median():.1f}")
