"""Pilot step 5 - morphometric + network indicators per sampled cell (LOCAL BBB data).

Uses official İzmir BBB layers (no OSM web queries):
  data/01_raw/buildings/izmir_buildings_bbb.gpkg  (ZEMINUSTUK = floors above ground)
  data/01_raw/roads/izmir_roads_bbb.gpkg          (road centrelines)

Per sampled 250 m cell:
  building (within cell): count, coverage, FAR (floors), mean floors, mean area,
                          mean shape index, orientation; built-form intensity.
  network service area (NETWORK-distance 400 m and 800 m reach along the BBB road
                          graph, not Euclidean buffers): street-length density,
                          intersection density, node density, mean segment length,
                          orientation entropy.
Output: data/03_processed/cell_indicators.csv
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import momepy

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
SAMPLE = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
BLD = os.path.join(PROJ, "data", "01_raw", "buildings", "izmir_buildings_bbb.gpkg")
ROAD = os.path.join(PROJ, "data", "01_raw", "roads", "izmir_roads_bbb.gpkg")
OUT = os.environ.get("PILOT05_OUT",
                     os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
CELL_A = 250.0 * 250.0

print("loading layers ...")
sample = gpd.read_file(SAMPLE).to_crs(32635)
bld = gpd.read_file(BLD).to_crs(32635)
road = gpd.read_file(ROAD).to_crs(32635)
bld["floors"] = pd.to_numeric(bld["ZEMINUSTUK"], errors="coerce").fillna(1).clip(1, 60)
bsi = bld.sindex
print(f"  {len(bld)} buildings, {len(road)} road lines, {len(sample)} cells")

# optional smoke-test on a few cells: PILOT05_SMOKE=20
SMOKE = int(os.environ.get("PILOT05_SMOKE", "0"))
if SMOKE:
    sample = sample.iloc[:SMOKE].copy()
    print(f"  SMOKE mode: first {len(sample)} cells only")

# ---- build a routable graph from the BBB road centre-lines (built once) ----
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

print("building routable road graph ...")
_node_id = {}
eu, ev, elen, ebrg = [], [], [], []
def _nid(p):
    key = (round(p[0], 1), round(p[1], 1))
    i = _node_id.get(key)
    if i is None:
        i = len(_node_id); _node_id[key] = i
    return i
for geom in road.geometry:
    if geom is None:
        continue
    parts = geom.geoms if geom.geom_type == "MultiLineString" else [geom]
    for ls in parts:
        cs = list(ls.coords)
        for a, b in zip(cs[:-1], cs[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = float(np.hypot(dx, dy))
            if L <= 0:
                continue
            eu.append(_nid(a)); ev.append(_nid(b))
            elen.append(L); ebrg.append(np.degrees(np.arctan2(dx, dy)) % 180.0)
NN = len(_node_id)
node_xy = np.empty((NN, 2))
for (x, y), i in _node_id.items():
    node_xy[i] = (x, y)
eu = np.asarray(eu); ev = np.asarray(ev)
elen = np.asarray(elen, float); ebrg = np.asarray(ebrg, float)
# undirected length-weighted adjacency (both directions)
A = csr_matrix((np.concatenate([elen, elen]),
               (np.concatenate([eu, ev]), np.concatenate([ev, eu]))), shape=(NN, NN))
deg = np.asarray((A > 0).sum(1)).ravel()       # node degree (>=3 => intersection)
ktree = cKDTree(node_xy)
print(f"  graph: {NN} nodes, {len(eu)} segments")

REACHES = (400, 800)


def building_metrics(cell):
    idx = list(bsi.query(cell, predicate="intersects"))
    if not idx:
        return dict(bld_count=0, bld_cov=0.0, far=0.0, mean_floors=np.nan,
                    bld_mean_area=np.nan, bld_mean_shape=np.nan, bld_orient=np.nan)
    sub = bld.iloc[idx].copy()
    clipped = sub.geometry.intersection(cell)
    area = clipped.area
    keep = area > 1.0
    sub, area = sub[keep], area[keep]
    if len(sub) == 0:
        return dict(bld_count=0, bld_cov=0.0, far=0.0, mean_floors=np.nan,
                    bld_mean_area=np.nan, bld_mean_shape=np.nan, bld_orient=np.nan)
    full_area = sub.geometry.area
    per = sub.geometry.length
    shape = per / (2.0 * np.sqrt(np.pi * full_area.clip(lower=1)))
    try:
        orient = float(np.nanmean(momepy.orientation(sub)))
    except Exception:
        orient = np.nan
    return dict(
        bld_count=int(len(sub)),
        bld_cov=float(area.sum() / CELL_A),
        far=float((area.values * sub["floors"].values).sum() / CELL_A),
        mean_floors=float(sub["floors"].mean()),
        bld_mean_area=float(full_area.mean()),
        bld_mean_shape=float(shape.mean()),
        bld_orient=orient,
    )


def network_metrics(centroid):
    """Network-distance service-area metrics at each reach (one capped SSSP per cell).

    A street segment counts toward the d-metre reach when BOTH its endpoints are
    within network distance d of the cell's nearest road node (true service area
    along the topological graph, not a Euclidean buffer). Densities are normalised
    by the nominal catchment area (pi*d^2) so they stay comparable across cells.
    """
    out = {}
    _, src = ktree.query([centroid.x, centroid.y])
    dist = dijkstra(A, directed=False, indices=int(src), limit=float(max(REACHES)))
    for d in REACHES:
        reach = dist <= d                      # graph nodes within network distance d
        em = reach[eu] & reach[ev]             # segments fully inside the service area
        sl = elen[em]
        area_km2 = np.pi * (d / 1000.0) ** 2
        if sl.size == 0:
            out.update({f"str_len_km_{d}": 0.0, f"str_dens_{d}": 0.0, f"node_dens_{d}": 0.0,
                        f"inter_dens_{d}": 0.0, f"mean_seg_{d}": np.nan, f"orient_ent_{d}": np.nan})
            continue
        total = float(sl.sum())
        n_nodes = int(reach.sum())
        n_inter = int((reach & (deg >= 3)).sum())
        bins = np.zeros(18)
        np.add.at(bins, np.minimum((ebrg[em] // 10).astype(int), 17), sl)
        p = bins / bins.sum()
        pp = p[p > 0]                          # only positive bins (no divide-by-zero warning)
        ent = float(-(pp * np.log(pp)).sum() / np.log(18))
        out.update({f"str_len_km_{d}": total / 1000.0,
                    f"str_dens_{d}": (total / 1000.0) / area_km2,
                    f"node_dens_{d}": n_nodes / area_km2,
                    f"inter_dens_{d}": n_inter / area_km2,
                    f"mean_seg_{d}": float(sl.mean()),
                    f"orient_ent_{d}": ent})
    return out


rows = []
for i, (_, r) in enumerate(sample.iterrows()):
    cell = r.geometry
    cent = cell.centroid
    rec = dict(sample_id=int(r.sample_id), stratum=int(r.stratum),
               stratum_name=r.stratum_name, x=cent.x, y=cent.y,
               f_built=r.f_built, f_green=r.f_green, slope_mean=r.slope_mean,
               dist_coast_km=r.dist_coast_km, dist_core_km=r.dist_core_km)
    rec.update(building_metrics(cell))
    rec.update(network_metrics(cent))
    rows.append(rec)
    if (i + 1) % 50 == 0:
        print(f"  {i+1}/{len(sample)}")

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print("\nwrote", os.path.relpath(OUT, PROJ), "| shape", df.shape)
agg = df.groupby("stratum_name").agg(
    n=("sample_id", "size"), bld=("bld_count", "mean"), cov=("bld_cov", "mean"),
    far=("far", "mean"), floors=("mean_floors", "mean"),
    str_dens800=("str_dens_800", "mean"), inter800=("inter_dens_800", "mean"),
    orient800=("orient_ent_800", "mean"))
print(agg.round(2).to_string())
