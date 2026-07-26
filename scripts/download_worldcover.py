"""Download ESA WorldCover 2021 (v200) land cover clipped to the Izmir study area.

Output: data/01_raw/worldcover/izmir_worldcover2021_10m.tif  (EPSG:32635, 10 m)
Source: ESA WorldCover v200 via Google Earth Engine (CC-BY 4.0). Project ee-geophilo.
The 'Map' band is the discrete land-cover class (10=tree,...,50=built-up,80=water,...).
"""
import os
import ee
import geopandas as gpd
import geemap

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
BOUNDARY = r"C:\Users\YE\PyCharmMiscProject\bbtmk_papers\data\02_interim\paper1\izmir_study_boundary.gpkg"
OUT_DIR = os.path.join(PROJ, "data", "01_raw", "worldcover")
OUT = os.path.join(OUT_DIR, "izmir_worldcover2021_10m.tif")
os.makedirs(OUT_DIR, exist_ok=True)

ee.Initialize(project="ee-geophilo")

# study bbox in WGS84 -> ee region
b = gpd.read_file(BOUNDARY).to_crs(4326)
minx, miny, maxx, maxy = b.total_bounds
region = ee.Geometry.Rectangle([minx, miny, maxx, maxy])

img = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map").clip(region)

print("Downloading ESA WorldCover 2021 @10m to:", OUT)
geemap.download_ee_image(
    image=img,
    filename=OUT,
    region=region,
    scale=10,
    crs="EPSG:32635",
    dtype="uint8",
)
print("DONE:", OUT, "size MB:", round(os.path.getsize(OUT) / 1e6, 1))
