"""Download OSM coastline (natural=coastline) within the Izmir study boundary.

Output: data/01_raw/coastline/izmir_coastline_osm.gpkg  (EPSG:32635)
Source: OpenStreetMap via Overpass API (ODbL). Disclosed shared open data.
"""
import os
import time
import requests
import geopandas as gpd
from shapely.geometry import LineString

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
BOUNDARY = r"C:\Users\YE\PyCharmMiscProject\bbtmk_papers\data\02_interim\paper1\izmir_study_boundary.gpkg"
OUT_DIR = os.path.join(PROJ, "data", "01_raw", "coastline")
OUT = os.path.join(OUT_DIR, "izmir_coastline_osm.gpkg")
os.makedirs(OUT_DIR, exist_ok=True)

# study bbox in WGS84
b = gpd.read_file(BOUNDARY).to_crs(4326)
minx, miny, maxx, maxy = b.total_bounds
bbox = f"{miny},{minx},{maxy},{maxx}"  # S,W,N,E
print("bbox (S,W,N,E):", bbox)

query = f"""
[out:json][timeout:180];
way["natural"="coastline"]({bbox});
(._;>;);
out body;
"""

endpoints = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]
headers = {"User-Agent": "icus2026-izmir-research/1.0 (yusuf.emnglu@gmail.com)"}
data = None
for url in endpoints:
    for attempt in range(2):
        try:
            print("querying", url, "attempt", attempt + 1, "...")
            r = requests.post(url, data={"data": query}, headers=headers, timeout=240)
            r.raise_for_status()
            data = r.json()
            break
        except Exception as e:
            print("  failed:", repr(e)[:160])
            time.sleep(3)
    if data is not None:
        break
if data is None:
    raise SystemExit("All Overpass endpoints failed.")

nodes = {e["id"]: (e["lon"], e["lat"]) for e in data["elements"] if e["type"] == "node"}
lines = []
for e in data["elements"]:
    if e["type"] == "way" and e.get("nodes"):
        coords = [nodes[n] for n in e["nodes"] if n in nodes]
        if len(coords) >= 2:
            lines.append({"osm_id": e["id"], "geometry": LineString(coords)})

if not lines:
    raise SystemExit("No coastline ways returned.")

gdf = gpd.GeoDataFrame(lines, crs=4326).to_crs(32635)
# clip to the actual study polygon's bounding area (keep full lines that intersect)
boundary_32635 = gpd.read_file(BOUNDARY).to_crs(32635)
gdf = gdf[gdf.intersects(boundary_32635.union_all().buffer(2000))].reset_index(drop=True)
gdf.to_file(OUT, driver="GPKG")
print(f"WROTE {OUT}")
print(f"  features: {len(gdf)} | total length: {gdf.length.sum()/1000:.1f} km | CRS: {gdf.crs}")
