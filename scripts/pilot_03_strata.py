"""Pilot step 3 - PROVISIONAL rule-based assignment of urban cells to 7 fabric strata.

PROVISIONAL: thresholds below are a transparent first pass from open data. They are
to be reviewed/refined with planning documents and urban-design input (H. Topcu)
before the strata are frozen. Clustering later tests/refines this classification.

Each rule is a documented open-data proxy for a fabric type in the İzmir planning
record and morphometric literature (see classify() for per-rule rationale). The
ordered "first match wins" logic encodes a planning priority: special functions
(industry) and the central/coastal city are resolved before generic residential
density bands.

REVISION (full-census prep): the waterfront_transformation rule gained a
`dist_core_km <= 15` constraint so it captures the metropolitan İzmir-Bay waterfront
ONLY and no longer mislabels remote Aegean coastal peninsulas (Çeşme/Karaburun/Foça/
Seferihisar) as waterfront — the over-capture flagged in PILOT_PROGRESS.

Strata: 1 historic_core, 2 grid_residential, 3 apartment_block,
        4 waterfront_transformation, 5 hillside_incremental,
        6 industrial_logistics, 7 peripheral_expansion
Output: data/02_interim/grid_250m_urban_strata.gpkg
        outputs/figures/strata_map_provisional.png
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
ENR = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban_enriched.gpkg")
BND = os.path.join(PROJ, "data", "00_external", "boundaries", "izmir_study_boundary.gpkg")
OUT = os.path.join(PROJ, "data", "02_interim", "grid_250m_urban_strata.gpkg")
FIG = os.path.join(PROJ, "outputs", "figures", "strata_map_provisional.png")
os.makedirs(os.path.dirname(FIG), exist_ok=True)

g = gpd.read_file(ENR)

# --- OSM industrial / port land use -> per-cell industrial fraction ---
g["f_industrial"] = 0.0
try:
    import osmnx as ox
    ox.settings.requests_timeout = 300
    poly = gpd.read_file(BND).to_crs(4326).union_all()
    tags = {"landuse": ["industrial", "port", "railway"], "man_made": ["works"],
            "aeroway": ["aerodrome", "apron", "runway"]}
    feats = ox.features_from_polygon(poly, tags)
    feats = feats[feats.geometry.type.isin(["Polygon", "MultiPolygon"])].to_crs(32635)
    print(f"OSM industrial/port/airport polygons: {len(feats)}")
    inter = gpd.overlay(g[["cell_id", "geometry"]], feats[["geometry"]], how="intersection")
    inter["a"] = inter.area
    frac = inter.groupby("cell_id")["a"].sum() / (250.0 * 250.0)
    g["f_industrial"] = g["cell_id"].map(frac).fillna(0.0).clip(0, 1)
except Exception as e:
    print("OSM industrial fetch failed (industrial stratum under-detected):", repr(e)[:160])

# --- transparent ordered rules (first match wins) ---
# Each rule is a documented, open-data proxy for a fabric type recognised in the
# İzmir planning record and the morphometric literature; thresholds are transparent
# and provisional (earmarked for planning-document refinement, H. Topçu).
def classify(r):
    # 1) industrial_logistics: dominated by OSM industrial/port/railway/airport land use.
    if r.f_industrial >= 0.30:
        return 6
    # 2) historic_core: the dense central city (Konak/Kemeraltı/Basmane) — near the
    #    metropolitan core and highly built.
    if r.dist_core_km <= 2.5 and r.f_built >= 0.45:
        return 1
    # 4) waterfront_transformation: built coastal fabric on the metropolitan GULF only.
    #    The added dist_core<=15 km confines it to the İzmir Bay ring (Alsancak,
    #    Bayraklı, Karşıyaka, Bostanlı, Mavişehir) and EXCLUDES the remote Aegean
    #    peninsulas (Çeşme, Karaburun, Foça, Seferihisar) that the bare 0.7 km coastal
    #    rule previously over-captured (see PILOT_PROGRESS: "waterfront over-broad").
    if r.dist_coast_km <= 0.7 and r.f_built >= 0.30 and r.dist_core_km <= 15.0:
        return 4
    # 5) hillside_incremental: settlement on the steep slopes ringing the basin.
    if r.slope_mean >= 8.0 and r.f_built >= 0.20:
        return 5
    # 3) apartment_block: dense, low-green mid/high-rise residential fabric.
    if r.f_built >= 0.55 and r.f_green <= 0.25:
        return 3
    # 2) grid_residential: moderately built planned residential fabric.
    if r.f_built >= 0.30:
        return 2
    # 7) peripheral_expansion: sparse low-density urban edge (residual).
    return 7

g["stratum"] = g.apply(classify, axis=1).astype(int)
names = {1: "historic_core", 2: "grid_residential", 3: "apartment_block",
         4: "waterfront_transformation", 5: "hillside_incremental",
         6: "industrial_logistics", 7: "peripheral_expansion"}
g["stratum_name"] = g["stratum"].map(names)
g.to_file(OUT, driver="GPKG")

print("\n=== PROVISIONAL strata distribution ===")
vc = g["stratum"].value_counts().sort_index()
for k in range(1, 8):
    print(f"  {k} {names[k]:26s} {int(vc.get(k,0)):6d}")
print(f"  total {len(g)}")

# --- map ---
colors = {1: "#b2182b", 2: "#ef8a62", 3: "#fddbc7", 4: "#2166ac",
          5: "#762a83", 6: "#1b7837", 7: "#999999"}
fig, ax = plt.subplots(figsize=(9, 9))
for k in range(1, 8):
    sub = g[g["stratum"] == k]
    if len(sub):
        sub.plot(ax=ax, color=colors[k], markersize=1, label=f"{names[k]} ({len(sub)})")
gpd.read_file(BND).to_crs(32635).boundary.plot(ax=ax, color="k", linewidth=0.4)
ax.set_title("İzmir FUR — provisional fabric strata (250 m urban cells)", fontsize=11)
ax.legend(loc="upper right", fontsize=7, markerscale=4)
ax.set_axis_off()
fig.tight_layout()
fig.savefig(FIG, dpi=140)
print("map ->", os.path.relpath(FIG, PROJ))
