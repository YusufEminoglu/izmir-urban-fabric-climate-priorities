"""Pilot step 2 - enrich urban grid cells with geographic signals for stratification.

Adds, per urban cell:
  dist_coast_km  - distance to OSM coastline
  dist_core_km   - distance to the historic core (Konak/Kemeralti, Izmir)
  (keeps f_built, f_green, f_water, slope_mean from step 1)
These are unambiguous inputs available to any stratification scheme; the actual
7-stratum labelling is decided separately (planning docs + urban-design input).
Output: data/02_interim/grid_250m_urban_enriched.gpkg
"""
import os
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
URBAN = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban.gpkg")
COAST = os.path.join(PROJ, "data", "01_raw", "coastline", "izmir_coastline_osm.gpkg")
OUT = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban_enriched.gpkg")

g = gpd.read_file(URBAN)
cent = g.geometry.centroid

# distance to coast (use union of coastline lines)
coast = gpd.read_file(COAST).to_crs(32635)
coast_u = coast.union_all()
g["dist_coast_km"] = cent.distance(coast_u) / 1000.0

# distance to historic core: Konak Square, Izmir (27.1287 E, 38.4192 N)
tr = Transformer.from_crs(4326, 32635, always_xy=True)
cx, cy = tr.transform(27.1287, 38.4192)
core = Point(cx, cy)
g["dist_core_km"] = cent.distance(core) / 1000.0

g.to_file(OUT, driver="GPKG")

print(f"enriched {len(g)} urban cells -> {os.path.basename(OUT)}")
for c in ["f_built", "f_green", "f_water", "slope_mean", "dist_coast_km", "dist_core_km"]:
    s = g[c]
    print(f"  {c:14s} min {s.min():7.2f} | p25 {s.quantile(.25):7.2f} | med {s.median():7.2f} "
          f"| p75 {s.quantile(.75):7.2f} | max {s.max():7.2f}")
