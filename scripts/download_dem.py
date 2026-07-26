"""Download Copernicus GLO-30 DEM clipped to the Izmir study area and derive slope.

Outputs (EPSG:32635, 30 m):
  data/01_raw/dem/izmir_dem_glo30_30m.tif      elevation (m)
  data/01_raw/dem/izmir_slope_glo30_30m.tif    slope (percent)
Source: COPERNICUS/DEM/GLO30 via Google Earth Engine (project ee-geophilo).
"""
import os
import ee
import numpy as np
import rasterio
import geopandas as gpd
import geemap

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
BOUNDARY = os.path.join(PROJ, "data", "00_external", "boundaries", "izmir_study_boundary.gpkg")
OUT_DIR = os.path.join(PROJ, "data", "01_raw", "dem")
DEM = os.path.join(OUT_DIR, "izmir_dem_glo30_30m.tif")
SLOPE = os.path.join(OUT_DIR, "izmir_slope_glo30_30m.tif")
os.makedirs(OUT_DIR, exist_ok=True)

ee.Initialize(project="ee-geophilo")

b = gpd.read_file(BOUNDARY).to_crs(4326)
minx, miny, maxx, maxy = b.total_bounds
region = ee.Geometry.Rectangle([minx, miny, maxx, maxy])

dem = ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM").mosaic().clip(region)
print("Downloading Copernicus GLO-30 DEM @30m ...")
geemap.download_ee_image(image=dem, filename=DEM, region=region, scale=30,
                         crs="EPSG:32635", dtype="float32")
print("DEM done:", round(os.path.getsize(DEM) / 1e6, 1), "MB")

# slope (percent) from local gradient in projected metres
with rasterio.open(DEM) as r:
    z = r.read(1).astype("float32")
    nodata = r.nodata
    px, py = r.res
    prof = r.profile
if nodata is not None:
    z[z == nodata] = np.nan
dzdy, dzdx = np.gradient(z, py, px)
slope_pct = np.sqrt(dzdx ** 2 + dzdy ** 2) * 100.0
slope_pct = np.where(np.isnan(slope_pct), -9999.0, slope_pct).astype("float32")
prof.update(dtype="float32", nodata=-9999.0, count=1, compress="deflate")
with rasterio.open(SLOPE, "w", **prof) as dst:
    dst.write(slope_pct, 1)
valid = slope_pct[slope_pct != -9999.0]
print("SLOPE done:", round(os.path.getsize(SLOPE) / 1e6, 1), "MB",
      "| slope %% min/med/max:", round(float(valid.min()), 1),
      round(float(np.median(valid)), 1), round(float(valid.max()), 1),
      "| cells >15%%:", round(100 * float((valid > 15).mean()), 1), "%%")
