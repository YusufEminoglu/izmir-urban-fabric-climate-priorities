"""Pilot step 8 - grid-resolution stability (250 m vs 500 m) via Adjusted Rand Index.

For the same 700 sampled locations, recompute the cell-area-dependent indicators on
a 500 m cell (centred on the 250 m cell centroid): building morphometrics, land-cover
fractions, slope. Reach-based network metrics (400/800 m) are scale-independent and
reused. Cluster the 500 m feature set with the identical pipeline and compare to the
250 m clustering with ARI. Output:
  outputs/tables/scale_stability.csv
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely
import momepy
from exactextract import exact_extract
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score, adjusted_rand_score

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
SAMPLE = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
CLUST = os.path.join(PROJ, "data", "03_processed", "cell_clusters.csv")
BLD = os.path.join(PROJ, "data", "01_raw", "buildings", "izmir_buildings_bbb.gpkg")
WC = os.path.join(PROJ, "data", "01_raw", "worldcover", "izmir_worldcover2021_10m.tif")
SLOPE = os.path.join(PROJ, "data", "01_raw", "dem", "izmir_slope_glo30_30m.tif")
TABDIR = os.path.join(PROJ, "outputs", "tables")

sample = gpd.read_file(SAMPLE).to_crs(32635)
clust = pd.read_csv(CLUST)[["sample_id", "cluster"]].rename(columns={"cluster": "cl250"})
bld = gpd.read_file(BLD).to_crs(32635)
bld["floors"] = pd.to_numeric(bld["ZEMINUSTUK"], errors="coerce").fillna(1).clip(1, 60)
bsi = bld.sindex

# build 500 m cells centred on each 250 m centroid
cents = sample.geometry.centroid
cells500 = gpd.GeoDataFrame(
    {"sample_id": sample["sample_id"].values},
    geometry=[shapely.box(c.x - 250, c.y - 250, c.x + 250, c.y + 250) for c in cents],
    crs=32635)
A500 = 500.0 * 500.0


def bmetrics(cell):
    idx = list(bsi.query(cell, predicate="intersects"))
    if not idx:
        return [0, 0.0, 0.0, np.nan, np.nan, np.nan, np.nan]
    sub = bld.iloc[idx]
    clip = sub.geometry.intersection(cell); a = clip.area
    keep = a > 1.0; sub, a = sub[keep], a[keep]
    if len(sub) == 0:
        return [0, 0.0, 0.0, np.nan, np.nan, np.nan, np.nan]
    fa = sub.geometry.area; per = sub.geometry.length
    shape = (per / (2 * np.sqrt(np.pi * fa.clip(lower=1)))).mean()
    try:
        orient = float(np.nanmean(momepy.orientation(sub)))
    except Exception:
        orient = np.nan
    return [int(len(sub)), float(a.sum() / A500), float((a.values * sub.floors.values).sum() / A500),
            float(sub.floors.mean()), float(fa.mean()), float(shape), orient]


print("building metrics at 500 m ...")
bm = np.array([bmetrics(g) for g in cells500.geometry], dtype=object)
b = pd.DataFrame(bm, columns=["bld_count", "bld_cov", "far", "mean_floors",
                              "bld_mean_area", "bld_mean_shape", "bld_orient"])
b["sample_id"] = cells500["sample_id"].values

print("land cover + slope at 500 m ...")
wc = exact_extract(WC, cells500, ["unique", "frac"], output="pandas", include_cols=["sample_id"])
fg = []
for u, f in zip(wc["unique"], wc["frac"]):
    u = np.atleast_1d(u).astype(int); f = np.atleast_1d(f).astype(float)
    fg.append(sum(fr for cls, fr in zip(u, f) if cls in (10, 20, 30)))
b["f_green"] = fg
sl = exact_extract(SLOPE, cells500, ["mean"], output="pandas", include_cols=["sample_id"])
b["slope_mean"] = sl["mean"].replace(-9999.0, np.nan).values

# assemble 500 m feature set: reuse reach-based network metrics from 250 m table
base = pd.read_csv(os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv"))
net = base[["sample_id", "stratum_name", "str_dens_800", "inter_dens_800", "node_dens_800",
            "mean_seg_800", "orient_ent_800"]]
feat = b.merge(net, on="sample_id").merge(clust, on="sample_id")

FEATURES = ["bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
            "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
            "f_green", "slope_mean"]
X = feat[FEATURES].copy()
for c in ["bld_cov", "far", "mean_floors", "bld_mean_area"]:
    X[c] = X[c].fillna(0.0)
X = X.fillna(X.median())
for c in X.columns:
    X[c] = X[c].clip(X[c].quantile(0.01), X[c].quantile(0.99))

Xp = PCA(n_components=0.90, random_state=0).fit_transform(StandardScaler().fit_transform(X))
Z = linkage(Xp, method="ward")
best_k, best_s = None, -1
sil_curve = []
for k in range(3, 10):
    lab = fcluster(Z, k, criterion="maxclust")
    mn = pd.Series(lab).value_counts().min()
    s = silhouette_score(Xp, lab)
    sil_curve.append({"k": k, "silhouette": round(float(s), 4),
                      "min_cluster": int(mn), "ok": bool(mn >= 10)})
    if mn >= 10 and s > best_s:
        best_k, best_s = k, s
pd.DataFrame(sil_curve).to_csv(os.path.join(TABDIR, "silhouette_curve_500.csv"), index=False)
feat["cl500"] = fcluster(Z, best_k, criterion="maxclust")

ari = adjusted_rand_score(feat["cl250"], feat["cl500"])
feat[["sample_id", "stratum_name", "cl250", "cl500"]].to_csv(
    os.path.join(TABDIR, "scale_stability.csv"), index=False)

print(f"\n500 m clustering: k={best_k} (silhouette {best_s:.3f})")
print(f"250 m clusters: {sorted(pd.Series(feat['cl250']).unique())} | "
      f"500 m clusters: {sorted(pd.Series(feat['cl500']).unique())}")
print(f"\n=== Adjusted Rand Index (250 m vs 500 m) = {ari:.3f} ===")
print("\ncross-tab 250m (rows) x 500m (cols):")
print(pd.crosstab(feat["cl250"], feat["cl500"]).to_string())
