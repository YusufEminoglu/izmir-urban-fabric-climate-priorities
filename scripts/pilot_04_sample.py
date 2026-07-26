"""Pilot step 4 - analysis-cell selection per fabric stratum.

FULL_CENSUS mode (default, for the journal version): take ALL retained urban cells
(no sampling) so the analysis is a full census of the İzmir FUR urban grid rather
than an N=700 pilot sample. Set FULL_CENSUS=False to recover the original stratified
random sample (~100/stratum, seed 42) used in the pilot.

Output (filename kept stable so the whole downstream pipeline runs unchanged):
  data/02_interim/grid_250m_sample.gpkg  (now the full census when FULL_CENSUS=True)
"""
import os
import geopandas as gpd

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
STR = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban_strata.gpkg")
OUT = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
FULL_CENSUS = True
TARGET = 100
SEED = 42

g = gpd.read_file(STR)
parts = []
for k, sub in g.groupby("stratum"):
    take = sub if (FULL_CENSUS or len(sub) <= TARGET) else sub.sample(n=TARGET, random_state=SEED)
    parts.append(take)
sample = gpd.GeoDataFrame(__import__("pandas").concat(parts), crs=g.crs).reset_index(drop=True)
sample["sample_id"] = range(len(sample))
sample.to_file(OUT, driver="GPKG")

mode = "FULL CENSUS (all urban cells)" if FULL_CENSUS else f"stratified sample (~{TARGET}/stratum, seed {SEED})"
print(f"{mode}: {len(sample)} cells -> {os.path.basename(OUT)}")
print(sample.groupby("stratum_name").size().to_string())
