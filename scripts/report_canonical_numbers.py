"""Canonical headline-number reporter — single source of truth for the manuscript.

Reads ONLY the authoritative processed CSVs / output tables and RE-DERIVES every
headline number the manuscript cites (independently recomputing ARI, the burden
Gini and LISA/Gi* counts), so prose and figures can be reconciled against one dump.

Run AFTER the full pipeline (pilot_05->14):
  .venv/Scripts/python.exe scripts/report_canonical_numbers.py
Numbers not stored in any CSV (spatial-block R2, silhouette, entropy weights) are
printed by pilot_07/09/11 to stdout and are noted as such here.
"""
import os
import numpy as np
import pandas as pd

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
PROC = os.path.join(PROJ, "data", "03_processed")
TAB = os.path.join(PROJ, "outputs", "tables")


def _read(path):
    return pd.read_csv(path) if os.path.exists(path) else None


def section(title):
    print("\n" + "=" * 72 + f"\n{title}\n" + "=" * 72)


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if n == 0 or x.sum() == 0:
        return np.nan
    return (2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum())


# --- N and per-stratum fabric profile (Table 1) -----------------------------
ind = _read(os.path.join(PROC, "cell_indicators.csv"))
if ind is not None:
    section(f"N (analysis cells) = {len(ind)}")
    print("per-stratum counts:")
    print(ind.groupby("stratum_name").size().to_string())
    cols = [c for c in ["far", "mean_floors", "bld_cov", "inter_dens_800",
                        "orient_ent_800", "lst_summer", "elderly_share", "svi"]
            if c in ind.columns]
    section("Fabric profile (per-stratum means) — Table tab:fabric-profiles")
    prof = ind.groupby("stratum_name")[cols].mean().round(3)
    prof["n"] = ind.groupby("stratum_name").size()
    print(prof.to_string())
    if "lst_summer" in ind:
        m = ind.groupby("stratum_name")["lst_summer"].mean()
        print(f"\nLST hottest: {m.idxmax()} {m.max():.1f}  | coolest: {m.idxmin()} "
              f"{m.min():.1f}  | range {m.max()-m.min():.1f} C")
    if "elderly_share" in ind:
        e = ind.groupby("stratum_name")["elderly_share"].mean()
        print(f"elderly highest: {e.idxmax()} {100*e.max():.1f}%  | lowest: "
              f"{e.idxmin()} {100*e.min():.1f}%")

# --- clustering (k, sizes) ---------------------------------------------------
clu = _read(os.path.join(PROC, "cell_clusters.csv"))
if clu is not None and "cluster" in clu.columns:
    section("Typology — k and cluster sizes (silhouette: see pilot_07 stdout)")
    vc = clu["cluster"].value_counts().sort_index()
    print(f"k = {clu['cluster'].nunique()};  sizes = {vc.to_dict()}")
prof = _read(os.path.join(TAB, "cluster_profiles.csv"))
if prof is not None:
    print("\ncluster profiles (means):")
    print(prof.round(2).to_string(index=False))

# --- scale stability (ARI, recomputed) --------------------------------------
sc = _read(os.path.join(TAB, "scale_stability.csv"))
if sc is not None and {"cl250", "cl500"}.issubset(sc.columns):
    from sklearn.metrics import adjusted_rand_score
    ari = adjusted_rand_score(sc["cl250"], sc["cl500"])
    section(f"Scale stability ARI (250 vs 500 m, recomputed) = {ari:.3f}")
    print(f"250m k={sc['cl250'].nunique()} | 500m k={sc['cl500'].nunique()}")

# --- SHAP (importance ranks; R2 from pilot_09 stdout) -----------------------
imp = _read(os.path.join(TAB, "shap_global_importance.csv"))
if imp is not None:
    section("SHAP global importance (top 8) — R2/RMSE: see pilot_09 stdout")
    print(imp.head(8).to_string(index=False))

# --- geostats (Moran; LISA/Gi*/Gini recomputed) -----------------------------
ms = _read(os.path.join(TAB, "geostats_summary.csv"))
if ms is not None:
    section("Global Moran's I")
    print(ms.to_string(index=False))
geo = _read(os.path.join(PROC, "cell_geostats.csv"))
if geo is not None:
    if "gi_hot" in geo:
        vc = geo["gi_hot"].value_counts()
        print(f"\nGi*: hot={int(vc.get('hot',0))}  cold={int(vc.get('cold',0))}  "
              f"ns={int(vc.get('ns',0))}")
    if "lisa" in geo:
        print("LISA counts:", geo["lisa"].value_counts().to_dict())
        hh = geo[geo["lisa"] == "HH"].groupby("stratum_name").size().sort_values(ascending=False)
        print("HH (high-need) by stratum:\n" + hh.to_string())
    if "burden" in geo:
        print(f"burden Gini (recomputed) = {gini(geo['burden'].values):.3f}")

# --- adaptation priority (TOPSIS) -------------------------------------------
ap = _read(os.path.join(TAB, "adaptation_priority.csv"))
if ap is not None:
    section("Fabric adaptation priority — Table tab:priority (entropy weights: pilot_11 stdout)")
    show = [c for c in ["stratum_name", "topsis_equal", "topsis_entropy",
                        "pareto_frontier", "rank_mean", "rank_p10", "rank_p90"] if c in ap.columns]
    print(ap[show].round(3).to_string(index=False))

# --- cell-level Pareto -------------------------------------------------------
cp = _read(os.path.join(TAB, "cell_pareto_summary.csv"))
if cp is not None:
    section("Cell-level Pareto frontier composition")
    tot = int(cp["n_frontier"].sum()) if "n_frontier" in cp else None
    ncells = int(cp["n_cells"].sum()) if "n_cells" in cp else None
    if tot is not None and ncells:
        print(f"frontier total = {tot} / {ncells} ({100*tot/ncells:.1f}%)")
    print(cp.round(3).to_string(index=False))

print("\n" + "=" * 72 + "\nDONE — reconcile manuscript + figures against the above.\n" + "=" * 72)
