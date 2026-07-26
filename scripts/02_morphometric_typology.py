"""
02_morphometric_typology.py
--------------------------------------------------------------------------------
Unsupervised Morphometric Clustering & Typology Diagnostics
Hierarchical Ward clustering on 13 morphometric indicators, generating
Figure 6 (Cluster synthesis) and Table 1 (Cluster profiles).
--------------------------------------------------------------------------------
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, set_link_color_palette
import seaborn as sns

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJ_DIR, "data", "03_processed", "cell_indicators.csv")
FIG_OUT = os.path.join(PROJ_DIR, "outputs", "figures", "figure6.png")
TAB_OUT = os.path.join(PROJ_DIR, "outputs", "tables", "table1.csv")

MORPH_FEATURES = [
    "bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
    "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
    "f_green", "slope_mean"
]

PALETTE = ["#E9B420", "#A0CBBF", "#C5AFD5", "#8E8E8D"]

def run_clustering():
    df = pd.read_csv(DATA_PATH)
    X = df[MORPH_FEATURES].copy().fillna(df[MORPH_FEATURES].median())
    
    # Winsorize and Z-score standardize
    X_norm = (X - X.mean()) / X.std()
    
    # Ward linkage
    Z = linkage(X_norm, method="ward")
    clusters = fcluster(Z, t=4, criterion="maxclust")
    df["cluster_id"] = clusters
    
    # Export Table 1
    profiles = df.groupby("cluster_id")[MORPH_FEATURES + ["lst_summer"]].mean()
    os.makedirs(os.path.dirname(TAB_OUT), exist_ok=True)
    profiles.to_csv(TAB_OUT)
    print(f"Exported Table 1: {TAB_OUT}")
    
    # Generate Figure 6
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.3), facecolor="#ffffff")
    
    # Panel a: Dendrogram
    set_link_color_palette(PALETTE)
    dendrogram(Z, ax=axes[0], truncate_mode="lastp", p=20, color_threshold=100, above_threshold_color="#94a3b8")
    axes[0].set_title("(a) Ward hierarchical dendrogram", fontsize=14, fontweight="bold", color="#1e293b")
    axes[0].set_xlabel("Morphometric Cluster Subtrees", fontsize=10.5)
    axes[0].set_ylabel("Euclidean Linkage Distance", fontsize=10.5)
    
    # Panel b: Profile distribution
    sns.boxplot(data=df, x="cluster_id", y="bld_cov", ax=axes[1], palette=PALETTE, hue="cluster_id", legend=False)
    axes[1].set_title("(b) Building coverage by cluster", fontsize=14, fontweight="bold", color="#1e293b")
    axes[1].set_xlabel("Morphometric Super-Type Cluster", fontsize=10.5)
    axes[1].set_ylabel("Building Coverage Fraction", fontsize=10.5)
    
    # Panel c: Bivariate coverage vs FAR
    colors_map = {c: PALETTE[(c - 1) % len(PALETTE)] for c in range(1, 5)}
    for c in range(1, 5):
        sub = df[df["cluster_id"] == c]
        axes[2].scatter(sub["bld_cov"], sub["far"], c=colors_map[c], s=14, alpha=0.55, label=f"Cluster {c}")
    axes[2].set_title("(c) Bivariate structure & density plane", fontsize=14, fontweight="bold", color="#1e293b")
    axes[2].set_xlabel("Building Coverage Fraction", fontsize=10.5)
    axes[2].set_ylabel("Floor-Area Ratio (FAR)", fontsize=10.5)
    axes[2].legend(loc="upper right", fontsize=9.5)
    
    for ax in axes:
        ax.set_facecolor("#ffffff")
        ax.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
            
    plt.tight_layout()
    os.makedirs(os.path.dirname(FIG_OUT), exist_ok=True)
    fig.savefig(FIG_OUT, dpi=300)
    plt.close()
    print(f"Exported Figure 6: {FIG_OUT}")

if __name__ == "__main__":
    run_clustering()
