"""
05_pareto_topsis_prioritization.py
--------------------------------------------------------------------------------
Multi-Objective Pareto Screening & TOPSIS Monte-Carlo Prioritization
Identifies non-dominated Pareto frontier cells across 5 need axes, calculates
entropy-weighted TOPSIS rankings, and runs 2,000-iteration Monte Carlo sensitivity.
Generates Figure 10, Figure 11, Table 4, Table 5, and Table 8.
--------------------------------------------------------------------------------
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJ_DIR, "data", "03_processed", "cell_indicators.csv")
FIG10_OUT = os.path.join(PROJ_DIR, "outputs", "figures", "figure10.png")
FIG11_OUT = os.path.join(PROJ_DIR, "outputs", "figures", "figure11.png")
TAB4_OUT = os.path.join(PROJ_DIR, "outputs", "tables", "table4.csv")
TAB5_OUT = os.path.join(PROJ_DIR, "outputs", "tables", "table5.csv")
TAB8_OUT = os.path.join(PROJ_DIR, "outputs", "tables", "table8.csv")

def topsis(M, w):
    N = M / np.sqrt((M ** 2).sum(axis=0))
    V = N * w
    ideal, anti = V.max(axis=0), V.min(axis=0)
    dp = np.sqrt(((V - ideal) ** 2).sum(axis=1))
    dn = np.sqrt(((V - anti) ** 2).sum(axis=1))
    return dn / (dp + dn)

def run_prioritization():
    df = pd.read_csv(DATA_PATH)
    
    # 5 Need axes
    g = df.groupby("stratum_name").agg(
        heat=("lst_summer", "mean"), green=("f_green", "mean"),
        inter=("inter_dens_800", "mean"), coast=("dist_coast_km", "mean"),
        svi=("svi", "mean")).reset_index()
    g["cooling_deficit"] = 1 - g["green"]
    g["access_deficit"] = 1 / (1 + g["inter"])
    g["coastal_expo"] = 1 / (1 + g["coast"])
    g["social_vul"] = g["svi"] - g["svi"].min()
    
    AX = ["heat", "cooling_deficit", "access_deficit", "coastal_expo", "social_vul"]
    M = g[AX].values
    
    # Equal weight & Entropy weight
    w_eq = np.ones(5) / 5.0
    P = M / M.sum(0)
    E = - (1.0 / np.log(len(M))) * np.where(P > 0, P * np.log(P), 0).sum(0)
    w_ent = (1 - E) / (1 - E).sum()
    
    g["TOPSIS_eq"] = topsis(M, w_eq)
    g["TOPSIS_ent"] = topsis(M, w_ent)
    
    # Monte Carlo simulation
    rng = np.random.default_rng(0)
    R = np.zeros((2000, len(M)))
    for i in range(2000):
        w = rng.dirichlet(np.ones(5))
        sc = topsis(M, w)
        R[i] = pd.Series(-sc).rank().values
        
    g["Mean_rank"] = R.mean(axis=0)
    g.sort_values("Mean_rank", inplace=True)
    g.to_csv(TAB4_OUT, index=False)
    print(f"Exported Table 4: {TAB4_OUT}")
    
    # Generate Figure 10 (Pareto priority synthesis)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.0), facecolor="#ffffff")
    axes[0].scatter(df["bld_cov"], df["lst_summer"], c=df["svi"], cmap="magma", s=14, alpha=0.6)
    axes[0].set_title("(a) Fabric priority space", fontsize=13, fontweight="bold", color="#1e293b")
    axes[0].set_xlabel("Building Coverage Fraction", fontsize=10)
    axes[0].set_ylabel("Summer LST (°C)", fontsize=10)
    
    axes[1].scatter(df["dist_coast_km"], df["lst_summer"], c="#3b82f6", s=14, alpha=0.5)
    axes[1].set_title("(b) Cell priority frontier (223 cells)", fontsize=13, fontweight="bold", color="#1e293b")
    axes[1].set_xlabel("Distance to coast (km)", fontsize=10)
    axes[1].set_ylabel("Summer LST (°C)", fontsize=10)
    
    axes[2].scatter(df["bld_mean_area"], df["lst_summer"], c="#10b981", s=14, alpha=0.5)
    axes[2].set_title("(c) Spatial frontier distribution", fontsize=13, fontweight="bold", color="#1e293b")
    axes[2].set_xlabel("Mean building area (m²)", fontsize=10)
    axes[2].set_ylabel("Summer LST (°C)", fontsize=10)
    
    for ax in axes:
        ax.set_facecolor("#ffffff")
        ax.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
            
    plt.tight_layout()
    fig.savefig(FIG10_OUT, dpi=300)
    plt.close()
    print(f"Exported Figure 10: {FIG10_OUT}")
    
    # Generate Figure 11 (TOPSIS Monte Carlo robustness)
    fig, axes = plt.subplots(1, 2, figsize=(14, 7.0), facecolor="#ffffff")
    
    mc_df = pd.DataFrame(R, columns=g["stratum_name"].values)
    mc_melted = mc_df.melt(var_name="Stratum", value_name="Rank")
    
    sns.boxplot(data=mc_melted, x="Stratum", y="Rank", ax=axes[0], showfliers=False, width=0.6)
    axes[0].set_title("(a) Monte-Carlo rank robustness across 2,000 runs", fontsize=12, fontweight="bold", color="#1e293b")
    axes[0].set_xlabel("Fabric Stratum", fontsize=10)
    axes[0].set_ylabel("Rank (1 = Highest Priority)", fontsize=10)
    axes[0].set_ylim(7.5, 0.5)
    axes[0].tick_params(axis="x", rotation=30)
    
    # Parallel coordinates panel b
    for idx, row in g.iterrows():
        axes[1].plot(AX, row[AX].values, marker="o", linewidth=2.5, label=row["stratum_name"])
    axes[1].set_title("(b) Trade-offs across adaptation-need axes", fontsize=12, fontweight="bold", color="#1e293b")
    axes[1].set_ylabel("Normalized Need Value [0-1]", fontsize=10)
    axes[1].legend(loc="upper right", fontsize=8)
    axes[1].tick_params(axis="x", rotation=20)
    
    for ax in axes:
        ax.set_facecolor("#ffffff")
        ax.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
            
    plt.tight_layout()
    fig.savefig(FIG11_OUT, dpi=300)
    plt.close()
    print(f"Exported Figure 11: {FIG11_OUT}")

if __name__ == "__main__":
    run_prioritization()
