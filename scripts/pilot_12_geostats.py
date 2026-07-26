"""Pilot step 10b - spatial statistics on the cell sample (GeoStats demonstration).

Builds a cell-level adaptation-need score (z-mean of heat, cooling deficit, access
deficit, coastal exposure, social vulnerability) and reports:
  - global Moran's I (autocorrelation) for LST, SVI, need score;
  - LISA cluster types for the need score (HH / LL / HL / LH, significant);
  - Getis-Ord Gi* hot/cold spots of the need score;
  - Gini and spatial Gini of the equity burden (impervious exposure x vulnerability).
Outputs:
  data/03_processed/cell_geostats.csv  (need score, LISA, Gi* per cell)
  outputs/tables/geostats_summary.csv
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from libpysal.weights import KNN
from esda.moran import Moran, Moran_Local
from esda.getisord import G_Local

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
SAMPLE = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
TABDIR = os.path.join(PROJ, "outputs", "tables")
os.makedirs(TABDIR, exist_ok=True)

df = pd.read_csv(IND)
gdf = gpd.read_file(SAMPLE).to_crs(32635)[["sample_id", "geometry"]].merge(df, on="sample_id")
pts = gpd.GeoDataFrame(df.merge(gdf[["sample_id", "geometry"]], on="sample_id"), geometry="geometry", crs=32635)
pts["geometry"] = pts.geometry.centroid


def z(s):
    s = pd.to_numeric(s, errors="coerce").fillna(0.0)
    return (s - s.mean()) / s.std()

pts["need"] = (z(pts["lst_summer"]) + z(1 - pts["f_green"]) +
               z(1 / (1 + pts["inter_dens_800"])) + z(1 / (1 + pts["dist_coast_km"])) +
               z(pts["svi"])) / 5.0

w = KNN.from_dataframe(pts, k=8)
w.transform = "r"
np.random.seed(0)

rows = []
for col in ["lst_summer", "svi", "need"]:
    mi = Moran(pts[col].values, w, permutations=999)
    rows.append(dict(variable=col, morans_I=round(mi.I, 3), p_sim=round(mi.p_sim, 3)))
moran_tab = pd.DataFrame(rows)

# LISA on need
lisa = Moran_Local(pts["need"].values, w, permutations=999, seed=0)
q = lisa.q.copy()
sig = lisa.p_sim < 0.05
labels = np.array(["ns"] * len(pts), dtype=object)
names = {1: "HH", 2: "LH", 3: "LL", 4: "HL"}
for i in range(len(pts)):
    if sig[i]:
        labels[i] = names.get(q[i], "ns")
pts["lisa"] = labels

# Gi* hot spots of need
gi = G_Local(pts["need"].values, w, star=True, permutations=999, seed=0)
pts["gi_z"] = gi.Zs
pts["gi_hot"] = np.where(gi.p_sim >= 0.05, "ns",
                         np.where(gi.Zs > 0, "hot", "cold"))

# equity burden = impervious exposure (1 - green) x vulnerability (svi shifted)
burden = (1 - pts["f_green"]).clip(0, 1) * (pts["svi"] - pts["svi"].min())
pts["burden"] = burden.values


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if x.sum() == 0:
        return np.nan
    return (2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum())

g_all = gini(burden)
# spatial Gini (Rey & Smith): share of overall Gini from neighbour vs non-neighbour pairs
W = w.full()[0]
xb = burden.values
n = len(xb)
absdiff = np.abs(xb[:, None] - xb[None, :])
denom = 2 * n * n * xb.mean()
neigh = (W > 0).astype(float)
g_neighbor = absdiff[neigh > 0].sum() / denom
g_nonneighbor = absdiff[(neigh == 0)].sum() / denom - (absdiff.diagonal().sum() / denom)

out = pts[["sample_id", "stratum_name", "need", "lisa", "gi_z", "gi_hot", "burden"]].copy()
out.to_csv(os.path.join(PROJ, "data", "03_processed", "cell_geostats.csv"), index=False)
moran_tab.to_csv(os.path.join(TABDIR, "geostats_summary.csv"), index=False)

print("=== global Moran's I ===")
print(moran_tab.to_string(index=False))
print("\n=== LISA clusters of adaptation need (sig p<0.05) ===")
print(pts["lisa"].value_counts().to_string())
print("\n=== Gi* hot/cold spots of need ===")
print(pts["gi_hot"].value_counts().to_string())
print("\nHH (high-need) clusters by stratum:")
print(pts[pts.lisa == "HH"].groupby("stratum_name").size().to_string())
print(f"\nequity burden Gini = {g_all:.3f}  | spatial decomposition: "
      f"neighbour share {g_neighbor/ (g_neighbor+g_nonneighbor):.2f}")
