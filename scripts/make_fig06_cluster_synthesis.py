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
from PIL import Image, ImageDraw, ImageFont

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUTC = os.path.join(PROJ, "data", "03_processed", "cell_clusters.csv")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
OUT_FIG = os.path.join(FIGDIR, "figure6.png")

df = pd.read_csv(IND)
FEATURES = [
    "bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
    "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
    "f_green", "slope_mean",
]
X = df[FEATURES].copy()
for c in ["bld_cov", "far", "mean_floors", "bld_mean_area"]:
    X[c] = X[c].fillna(0.0)
for c in ["bld_mean_shape", "bld_orient", "mean_seg_800", "orient_ent_800"]:
    X[c] = X[c].fillna(X[c].median())
X = X.fillna(X.median())

for c in X.columns:
    lo, hi = X[c].quantile(0.01), X[c].quantile(0.99)
    X[c] = X[c].clip(lo, hi)

Xz = StandardScaler().fit_transform(X)
pca = PCA(n_components=0.90, random_state=0)
Xp = pca.fit_transform(Xz)

Z = linkage(Xp, method="ward")
best_k, best_s = 4, 0.224

labels = fcluster(Z, best_k, criterion="maxclust")
df["cluster"] = labels

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, axes = plt.subplots(1, 3, figsize=(18, 6.3), facecolor="#ffffff")

clusters = sorted(pd.Series(labels).unique())
PAL = ["#E9B420", "#A0CBBF", "#C5AFD5", "#8E8E8D", "#DEA6A3", "#EBCB9C", "#DDB5B5"]
colors_map = {c: PAL[i % len(PAL)] for i, c in enumerate(clusters)}
labels_names = {c: f"Cluster {c}" for c in clusters}

# Panel (a)
axes[0].set_facecolor("#ffffff")
set_link_color_palette([colors_map[c] for c in clusters])

cut_height = Z[-(best_k - 1), 2]
dendrogram(Z, ax=axes[0], truncate_mode="lastp", p=best_k * 3, leaf_rotation=90, 
           color_threshold=cut_height, above_threshold_color="#94a3b8")
axes[0].axhline(y=cut_height, color="#ef4444", linestyle="--", linewidth=1.2, label=f"Cut height ({cut_height:.1f})")
axes[0].set_ylabel("Linkage distance", fontsize=11)
axes[0].set_xlabel("Truncated nodes (leaf size in parentheses)", fontsize=10.5)
axes[0].legend(fontsize=9.5, loc="upper right", framealpha=0.95)
axes[0].grid(True, linestyle=":", alpha=0.4, axis="y")
for _sp in ["top", "right"]:
    axes[0].spines[_sp].set_visible(False)

# Panel (b)
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
    
    label_text = labels_names[c]
    axes[1].text(-0.03, y_lower + 0.45 * size_cluster_c, label_text, 
                 fontsize=10, fontweight="bold", color="#1e293b", ha="right", va="center")
    
    y_lower = y_upper + 15

axes[1].set_xlabel("Silhouette coefficient", fontsize=11)
axes[1].set_ylabel("Grid cells grouped by cluster", fontsize=11)
axes[1].set_yticks([])
axes[1].set_xlim([-0.12, 0.65])
axes[1].axvline(x=best_s, color="#ef4444", linestyle="--", linewidth=1.2, zorder=3)
axes[1].text(best_s + 0.02, y_lower - 20, f"Mean: {best_s:.3f}", color="#ef4444", fontsize=10.5, fontweight="bold")
axes[1].grid(True, linestyle=":", alpha=0.5)
for _sp in ["top", "right"]:
    axes[1].spines[_sp].set_visible(False)

# Panel (c)
axes[2].set_facecolor("#ffffff")
for c in clusters:
    sub = df[df["cluster"] == c]
    sns.kdeplot(
        data=sub, x="bld_cov", y="far", ax=axes[2],
        color=colors_map[c], alpha=0.25, levels=3, thresh=0.15, fill=True, zorder=1
    )

for c in clusters:
    sub = df[df["cluster"] == c]
    axes[2].scatter(sub["bld_cov"], sub["far"], c=colors_map[c], s=13,
                    edgecolor="none", alpha=0.55, label=labels_names[c], zorder=2)

axes[2].set_xlabel("Building coverage (fraction)", fontsize=11)
axes[2].set_ylabel("Floor-area ratio (FAR)", fontsize=11)
axes[2].legend(fontsize=9.5, loc="upper left", framealpha=0.95, markerscale=1.8)
axes[2].grid(True, linestyle=":", alpha=0.5)
for _sp in ["top", "right"]:
    axes[2].spines[_sp].set_visible(False)

set_link_color_palette(None)

plt.subplots_adjust(left=0.06, right=0.96, top=0.92, bottom=0.15, wspace=0.28)
fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)

img = Image.open(OUT_FIG).convert("RGB")
draw = ImageDraw.Draw(img)
w, h = img.size

try:
    font = ImageFont.truetype("arialbd.ttf", 92)
except:
    font = ImageFont.truetype("arial.ttf", 92)

draw.rectangle([250, 20, 440, 125], fill=(255, 255, 255))
draw.text((280, 30), "(a)", fill=(0, 0, 0), font=font)

draw.rectangle([w//3 + 200, 20, w//3 + 390, 125], fill=(255, 255, 255))
draw.text((w//3 + 230, 30), "(b)", fill=(0, 0, 0), font=font)

draw.rectangle([2*w//3 + 140, 20, 2*w//3 + 330, 125], fill=(255, 255, 255))
draw.text((2*w//3 + 170, 30), "(c)", fill=(0, 0, 0), font=font)

img.save(OUT_FIG)
print(f"Successfully generated Figure 6: {OUT_FIG}")
