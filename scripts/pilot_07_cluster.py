"""Pilot step 7 - PCA + Ward clustering of cells into fabric-resilience profiles.

Clusters on morphometric + network descriptors (NOT on LST, which is the outcome).
Chooses k by silhouette; cross-tabulates clusters against the provisional strata
(a-priori-then-test logic). Outputs:
  data/03_processed/cell_clusters.csv
  outputs/figures/cluster_synthesis.png
  outputs/tables/cluster_profiles.csv
  outputs/tables/cluster_vs_stratum.csv
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, set_link_color_palette
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUTC = os.path.join(PROJ, "data", "03_processed", "cell_clusters.csv")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
TABDIR = os.path.join(PROJ, "outputs", "tables")
os.makedirs(FIGDIR, exist_ok=True); os.makedirs(TABDIR, exist_ok=True)

df = pd.read_csv(IND)
FEATURES = [
    "bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
    "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
    "f_green", "slope_mean",
]
X = df[FEATURES].copy()
# no-building cells: structural zeros for built metrics, median for shape/orient
for c in ["bld_cov", "far", "mean_floors", "bld_mean_area"]:
    X[c] = X[c].fillna(0.0)
for c in ["bld_mean_shape", "bld_orient", "mean_seg_800", "orient_ent_800"]:
    X[c] = X[c].fillna(X[c].median())
X = X.fillna(X.median())

# winsorize each feature to [1, 99] percentiles to stop single-building artefacts
# (e.g. one giant footprint) from dominating the Euclidean clustering
for c in X.columns:
    lo, hi = X[c].quantile(0.01), X[c].quantile(0.99)
    X[c] = X[c].clip(lo, hi)

Xz = StandardScaler().fit_transform(X)
pca = PCA(n_components=0.90, random_state=0)
Xp = pca.fit_transform(Xz)
print(f"PCA: {Xp.shape[1]} components retain {pca.explained_variance_ratio_.sum():.2f} variance")

Z = linkage(Xp, method="ward")
# choose k by silhouette, but require every cluster to have >= 10 cells
best_k, best_s = None, -1
sil_curve = []
for k in range(3, 10):
    lab = fcluster(Z, k, criterion="maxclust")
    sizes = pd.Series(lab).value_counts()
    s = silhouette_score(Xp, lab)
    ok = sizes.min() >= 10
    sil_curve.append({"k": k, "silhouette": round(float(s), 4),
                      "min_cluster": int(sizes.min()), "ok": bool(ok)})
    print(f"  k={k}  silhouette={s:.3f}  min_cluster={sizes.min()}  {'ok' if ok else 'rejected (tiny cluster)'}")
    if ok and s > best_s:
        best_k, best_s = k, s
pd.DataFrame(sil_curve).to_csv(os.path.join(TABDIR, "silhouette_curve_250.csv"), index=False)
print(f"chosen k={best_k} (silhouette {best_s:.3f})")

labels = fcluster(Z, best_k, criterion="maxclust")
df["cluster"] = labels
df.to_csv(OUTC, index=False)

# profiles (means per cluster, incl. the LST outcome for interpretation)
prof_cols = FEATURES + ["lst_summer", "dist_coast_km", "dist_core_km"]
profiles = df.groupby("cluster")[prof_cols].mean().round(2)
profiles["n"] = df.groupby("cluster").size()
profiles.to_csv(os.path.join(TABDIR, "cluster_profiles.csv"))

ct = pd.crosstab(df["cluster"], df["stratum_name"])
ct.to_csv(os.path.join(TABDIR, "cluster_vs_stratum.csv"))

# cluster synthesis map (3 panels)
fig, axes = plt.subplots(1, 3, figsize=(18, 6.3), facecolor="#ffffff")

# robust to any k: palette indexed by sorted cluster id (interpretive names live in
# the manuscript text / caption, not hard-coded here)
clusters = sorted(pd.Series(labels).unique())
PAL = ["#E9B420", "#A0CBBF", "#C5AFD5", "#8E8E8D", "#DEA6A3", "#EBCB9C", "#DDB5B5"]
colors_map = {c: PAL[i % len(PAL)] for i, c in enumerate(clusters)}
labels_names = {c: f"Cluster {c}" for c in clusters}

# Panel (a): Dendrogram
axes[0].set_facecolor("#ffffff")
# Match dendrogram coloring with cluster palette
# SciPy dendrogram picks colors from the link color palette.
# Let's set the link color palette temporarily to match our cluster colors.
# Note: fcluster labels are 1, 2, 3. Dendrogram link colors will follow the order in link palette.
set_link_color_palette([colors_map[c] for c in clusters])

cut_height = Z[-(best_k - 1), 2]
dendrogram(Z, ax=axes[0], truncate_mode="lastp", p=best_k * 3, leaf_rotation=90, 
           color_threshold=cut_height, above_threshold_color="#94a3b8")
axes[0].axhline(y=cut_height, color="#ef4444", linestyle="--", linewidth=1.2, label=f"Cut height ({cut_height:.1f})")
axes[0].set_title("(a) Ward hierarchical dendrogram", fontsize=14.5, fontweight="bold", color="#1e293b")
axes[0].set_ylabel("Linkage distance", fontsize=11)
axes[0].set_xlabel("Truncated nodes (leaf size in parentheses)", fontsize=10.5)
axes[0].legend(fontsize=9.5, loc="upper right", framealpha=0.95)
axes[0].grid(True, linestyle=":", alpha=0.4, axis="y")
for _sp in ["top", "right"]:
    axes[0].spines[_sp].set_visible(False)

# Panel (b): Silhouette width analysis
axes[1].set_facecolor("#ffffff")
sample_silhouette_values = silhouette_samples(Xp, labels)

y_lower = 10
for c in clusters:
    ith_cluster_silhouette_values = sample_silhouette_values[labels == c]
    ith_cluster_silhouette_values.sort()
    
    size_cluster_c = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_c
    
    color = colors_map[c]
    axes[1].fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values,
                         facecolor=color, edgecolor=color, alpha=0.7, zorder=2)
    
    # Label the silhouette plots with their cluster names
    label_text = labels_names[c]
    axes[1].text(-0.03, y_lower + 0.45 * size_cluster_c, label_text, 
                 fontsize=10, fontweight="bold", color="#1e293b", ha="right", va="center")
    
    y_lower = y_upper + 15

axes[1].set_title("(b) Silhouette profile diagnostics", fontsize=14.5, fontweight="bold", color="#1e293b")
axes[1].set_xlabel("Silhouette coefficient", fontsize=11)
axes[1].set_ylabel("Grid cells grouped by cluster", fontsize=11)
axes[1].set_yticks([]) # Clear the y-axis labels
axes[1].set_xlim([-0.12, 0.65])
axes[1].axvline(x=best_s, color="#ef4444", linestyle="--", linewidth=1.2, zorder=3)
axes[1].text(best_s + 0.02, y_lower - 20, f"Mean: {best_s:.3f}", color="#ef4444", fontsize=10.5, fontweight="bold")
axes[1].grid(True, linestyle=":", alpha=0.5)
for _sp in ["top", "right"]:
    axes[1].spines[_sp].set_visible(False)

# Panel (c): Scatter plot of building coverage vs far with bivariate KDE
axes[2].set_facecolor("#ffffff")
# Plot bivariate KDE contours first (soft background density)
for c in clusters:
    sub = df[df["cluster"] == c]
    sns.kdeplot(
        data=sub, x="bld_cov", y="far", ax=axes[2],
        color=colors_map[c], alpha=0.25, levels=3, thresh=0.15, fill=True, zorder=1
    )

# Plot scatter points on top
for c in clusters:
    sub = df[df["cluster"] == c]
    axes[2].scatter(sub["bld_cov"], sub["far"], c=colors_map[c], s=13,
                    edgecolor="none", alpha=0.55, label=labels_names[c], zorder=2)

axes[2].set_xlabel("Building coverage (fraction)", fontsize=11)
axes[2].set_ylabel("Floor-area ratio (FAR)", fontsize=11)
axes[2].set_title("(c) Bivariate structure & density contours", fontsize=14.5, fontweight="bold", color="#1e293b")
axes[2].legend(fontsize=9.5, loc="upper left", framealpha=0.95, markerscale=1.8)
axes[2].grid(True, linestyle=":", alpha=0.5)
for _sp in ["top", "right"]:
    axes[2].spines[_sp].set_visible(False)

# Restore default SciPy colors
set_link_color_palette(None)

plt.tight_layout()
fig.savefig(os.path.join(FIGDIR, "cluster_synthesis.png"), dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)
print("wrote outputs/figures/cluster_synthesis.png")

print("\n=== cluster profiles (means) ===")
print(profiles.to_string())
print("\n=== cluster x provisional stratum ===")
print(ct.to_string())
