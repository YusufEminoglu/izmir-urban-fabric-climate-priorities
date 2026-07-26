import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
CLUST_PATH = os.path.join(PROJ, "data", "03_processed", "cell_clusters.csv")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
os.makedirs(FIGDIR, exist_ok=True)

df_clust = pd.read_csv(CLUST_PATH)

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

FEATURES = [
    "bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
    "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
    "f_green", "slope_mean",
]

rename_map = {
    "far": "Floor-Area Ratio (FAR)",
    "bld_cov": "Building Coverage",
    "mean_floors": "Mean Floors",
    "bld_mean_area": "Mean Footprint Area",
    "bld_mean_shape": "Footprint Shape Index",
    "bld_orient": "Building Orientation",
    "str_dens_800": "Street Density",
    "inter_dens_800": "Intersection Density",
    "node_dens_800": "Node Density",
    "mean_seg_800": "Mean Segment Length",
    "orient_ent_800": "Street Orient. Entropy",
    "f_green": "Green Cover",
    "slope_mean": "Mean Slope"
}

X = df_clust[FEATURES].copy()
X = X.fillna(X.median())

Xz = StandardScaler().fit_transform(X)
pca = PCA(n_components=Xz.shape[1], random_state=0)
Xp = pca.fit_transform(Xz)

fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor="#ffffff")

# Panel (a): Scree plot
ax0 = axes[0, 0]
ax0.set_facecolor("#ffffff")
evr = pca.explained_variance_ratio_
cum_evr = np.cumsum(evr)

ax0.bar(range(1, len(evr)+1), evr, alpha=0.75, color="#8E8E8D", label="Individual Variance Explained")
ax0.step(range(1, len(evr)+1), cum_evr, where="mid", color="#E9B420", linewidth=2.0, label="Cumulative Variance Explained")
ax0.axhline(0.90, color="#64748B", linestyle="--", alpha=0.7)
ax0.text(1.2, 0.92, "90% Variance Explained threshold", fontsize=9, color="#64748B", fontweight="bold")

ax0.set_title("(a) PCA Scree Plot", fontsize=11, fontweight="bold", color="#1e293b")
ax0.set_xlabel("Principal Component Index", fontsize=9.5)
ax0.set_ylabel("Explained Variance Ratio", fontsize=9.5)
ax0.set_xticks(range(1, len(evr)+1))
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax0.legend(loc="center right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

# Panel (b): Biplot loadings (PC1 vs PC2)
ax1 = axes[0, 1]
ax1.set_facecolor("#ffffff")
loadings = pca.components_[:2].T

for i, feature in enumerate(FEATURES):
    ax1.arrow(0, 0, loadings[i, 0], loadings[i, 1], color="#8E8E8D", alpha=0.8, head_width=0.02, linewidth=1.2)
    # Positioning offset
    offset_x = 0.03 if loadings[i, 0] > 0 else -0.15
    offset_y = 0.02 if loadings[i, 1] > 0 else -0.05
    label_text = rename_map.get(feature, feature).split(" (")[0]
    ax1.text(loadings[i, 0] + offset_x, loadings[i, 1] + offset_y, label_text, fontsize=8, color="#E9B420", fontweight="bold")

ax1.set_xlim(-0.6, 0.6)
ax1.set_ylim(-0.6, 0.6)
ax1.axhline(0, color="#64748B", linestyle=":", alpha=0.5)
ax1.axvline(0, color="#64748B", linestyle=":", alpha=0.5)
ax1.set_title("(b) PCA Component Loadings Biplot (PC1 vs PC2)", fontsize=11, fontweight="bold", color="#1e293b")
ax1.set_xlabel(f"PC 1 ({evr[0]*100:.1f}% variance)", fontsize=9.5)
ax1.set_ylabel(f"PC 2 ({evr[1]*100:.1f}% variance)", fontsize=9.5)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")

# Panel (c): Heatmap of component loadings for first 7 PCs
ax2 = axes[1, 0]
ax2.set_facecolor("#ffffff")
loadings_7 = pca.components_[:7].T
loadings_df = pd.DataFrame(
    loadings_7,
    index=[rename_map[f] for f in FEATURES],
    columns=[f"PC {i+1}" for i in range(7)]
)

sns.heatmap(
    loadings_df,
    cmap="RdBu_r",
    center=0,
    annot=True,
    fmt="+.2f",
    ax=ax2,
    cbar_kws={"label": "Loading Coefficient"},
    annot_kws={"size": 7.5, "weight": "bold"},
    edgecolor="#cbd5e1",
    linewidths=0.5
)
ax2.set_title("(c) Feature Loadings Across Retained Components (PC1-PC7)", fontsize=11, fontweight="bold", color="#1e293b")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, fontsize=8.5)
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, fontsize=8.0)

# Panel (d): PC Scatter by Unsupervised Cluster
ax3 = axes[1, 1]
ax3.set_facecolor("#ffffff")

# robust to any k: palette indexed by sorted cluster id
_clusters = sorted(df_clust["cluster"].unique())
_PAL = ["#E9B420", "#A0CBBF", "#C5AFD5", "#8E8E8D", "#DEA6A3", "#EBCB9C", "#DDB5B5"]
colors_map = {c: _PAL[i % len(_PAL)] for i, c in enumerate(_clusters)}
cluster_labels = {c: f"Cluster {int(c)}" for c in _clusters}

for c_id in _clusters:
    idx = df_clust["cluster"] == c_id
    ax3.scatter(
        Xp[idx, 0],
        Xp[idx, 1],
        color=colors_map[c_id],
        label=cluster_labels[c_id],
        alpha=0.7,
        edgecolors="#334155",
        linewidths=0.4,
        s=30
    )

ax3.set_title("(d) Fabric Clusters in Principal Component Space", fontsize=11, fontweight="bold", color="#1e293b")
ax3.set_xlabel(f"PC 1 ({evr[0]*100:.1f}% variance)", fontsize=9.5)
ax3.set_ylabel(f"PC 2 ({evr[1]*100:.1f}% variance)", fontsize=9.5)
ax3.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax3.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.0)

fig.suptitle("Supplementary Figure S2: PCA Dimensionality Reduction Diagnostics", fontsize=14, fontweight="bold", color="#0f172a", y=0.98)
plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.08, wspace=0.25, hspace=0.30)

out_path = os.path.join(FIGDIR, "supp_pca_diagnostics.png")
fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

import shutil
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(out_path, os.path.join(figs_cur, "supp_pca_diagnostics.png"))

print(f"Wrote {out_path}")
