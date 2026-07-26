"""Import official İzmir BBB layers (buildings, road centrelines) into the project.

Reads from the akilli_sehir_db source, keeps the useful columns, reprojects to
EPSG:32635, writes compact GPKGs into this project. (We copy the data in; we do
not read the sibling store at analysis time.)

Outputs:
  data/01_raw/buildings/izmir_buildings_bbb.gpkg   (901k polygons; floors = ZEMINUSTUK)
  data/01_raw/roads/izmir_roads_bbb.gpkg           (208k centrelines)
"""
import os
from pyogrio import read_dataframe, write_dataframe

SRC = r"C:\Users\YE\PyCharmMiscProject\bbtmk_papers\data\00_external\akilli_sehir_db"
PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"

jobs = [
    ("yapi.shp", ["ZEMINUSTUK", "ZEMINALTIK", "YAPITIP"], "buildings", "izmir_buildings_bbb.gpkg"),
    ("yolorta.shp", ["YOLUNISLEV", "SERITSAYIS", "YOLTIP"], "roads", "izmir_roads_bbb.gpkg"),
]
for shp, cols, sub, out in jobs:
    src = os.path.join(SRC, shp)
    print(f"reading {shp} ...")
    g = read_dataframe(src, columns=cols)
    print(f"  {len(g)} features, src crs {g.crs}")
    g = g.to_crs(32635)
    # drop empty/invalid geometries
    g = g[~g.geometry.is_empty & g.geometry.notna()].reset_index(drop=True)
    outdir = os.path.join(PROJ, "data", "01_raw", sub)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, out)
    write_dataframe(g, outpath, driver="GPKG")
    print(f"  wrote {outpath}  ({round(os.path.getsize(outpath)/1e6,1)} MB)")
print("DONE")
