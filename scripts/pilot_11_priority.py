"""Pilot step 11 - adaptation priority per fabric (Pareto frontier + TOPSIS + robustness).

Need-axes (higher = more adaptation need), aggregated to the 7 provisional strata:
  heat            = mean summer LST
  cooling_deficit = 1 - green fraction
  access_deficit  = 1 / (1 + intersection density 800 m)
  coastal_expo    = 1 / (1 + distance to coast km)
  social_vul      = mean SVI (ADNKS elderly share + age dependency), shifted >=0

Pareto: a fabric is on the priority frontier if no other fabric has greater need
on ALL axes. TOPSIS ranks fabrics; robustness via equal/entropy/Monte-Carlo weights.
Outputs:
  outputs/tables/adaptation_priority.csv
  outputs/figures/priority_pareto.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
TABDIR = os.path.join(PROJ, "outputs", "tables"); FIGDIR = os.path.join(PROJ, "outputs", "figures")
os.makedirs(TABDIR, exist_ok=True); os.makedirs(FIGDIR, exist_ok=True)

df = pd.read_csv(IND)
g = df.groupby("stratum_name").agg(
    heat=("lst_summer", "mean"), green=("f_green", "mean"),
    inter=("inter_dens_800", "mean"), coast=("dist_coast_km", "mean"),
    svi=("svi", "mean")).reset_index()
g["cooling_deficit"] = 1 - g["green"]
g["access_deficit"] = 1 / (1 + g["inter"])
g["coastal_expo"] = 1 / (1 + g["coast"])
g["social_vul"] = g["svi"] - g["svi"].min()  # shift to >=0 for TOPSIS
AX = ["heat", "cooling_deficit", "access_deficit", "coastal_expo", "social_vul"]
M = g[AX].values

# --- Pareto frontier (maximisation of need) ---
def non_dominated(M):
    n = len(M); nd = np.ones(n, bool)
    for i in range(n):
        for j in range(n):
            if i != j and np.all(M[j] >= M[i]) and np.any(M[j] > M[i]):
                nd[i] = False; break
    return nd
g["pareto_frontier"] = non_dominated(M)

# --- TOPSIS ---
def topsis(M, w):
    N = M / np.sqrt((M ** 2).sum(0))
    V = N * w
    ideal, anti = V.max(0), V.min(0)
    dp = np.sqrt(((V - ideal) ** 2).sum(1)); dn = np.sqrt(((V - anti) ** 2).sum(1))
    return dn / (dp + dn)

w_eq = np.ones(len(AX)) / len(AX)
# entropy weights
P = M / M.sum(0); k = 1 / np.log(len(M))
E = -k * (np.where(P > 0, P * np.log(P), 0)).sum(0)
w_ent = (1 - E) / (1 - E).sum()
g["topsis_equal"] = topsis(M, w_eq)
g["topsis_entropy"] = topsis(M, w_ent)

# Monte-Carlo weight robustness: rank distribution under random weights
rng = np.random.default_rng(0)
R = np.zeros((2000, len(M)))
for i in range(2000):
    w = rng.dirichlet(np.ones(len(AX)))
    sc = topsis(M, w)
    R[i] = pd.Series(-sc).rank().values  # rank 1 = highest priority
g["rank_mean"] = R.mean(0)
g["rank_p10"] = np.percentile(R, 10, axis=0)
g["rank_p90"] = np.percentile(R, 90, axis=0)

g = g.sort_values("topsis_entropy", ascending=False)
g.round(3).to_csv(os.path.join(TABDIR, "adaptation_priority.csv"), index=False)

print(f"entropy weights {dict(zip(AX, w_ent.round(2)))}")
print("\n=== adaptation priority (sorted by TOPSIS-entropy) ===")
print(g[["stratum_name", "heat", "cooling_deficit", "access_deficit", "coastal_expo",
         "social_vul", "topsis_equal", "topsis_entropy", "pareto_frontier", "rank_mean",
         "rank_p10", "rank_p90"]].round(3).to_string(index=False))

# --- Pareto plot: heat vs cooling_deficit, sized by access_deficit ---
plt.figure(figsize=(7, 6))
sc = plt.scatter(g["heat"], g["cooling_deficit"], s=200 * g["access_deficit"] / g["access_deficit"].max() + 40,
                 c=np.where(g["pareto_frontier"], "#b2182b", "#999999"), edgecolor="k", zorder=3)
for _, r in g.iterrows():
    plt.annotate(r["stratum_name"], (r["heat"], r["cooling_deficit"]), fontsize=7,
                 xytext=(4, 4), textcoords="offset points")
plt.xlabel("heat (mean summer LST, °C)"); plt.ylabel("cooling deficit (1 − green)")
plt.title("Fabric adaptation priority — Pareto frontier (red) ; size = access deficit")
plt.tight_layout(); plt.savefig(os.path.join(FIGDIR, "priority_pareto.png"), dpi=140); plt.close()
print("\nfrontier fabrics:", list(g[g.pareto_frontier]["stratum_name"]))
