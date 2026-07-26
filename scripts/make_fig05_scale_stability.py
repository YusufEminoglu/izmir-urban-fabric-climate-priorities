import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import adjusted_rand_score

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
STAB_PATH = os.path.join(PROJ, "outputs", "tables", "scale_stability.csv")
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "scale_stability.png")

print("Loading scale stability data...")
df_stab = pd.read_csv(STAB_PATH)
df_ind = pd.read_csv(IND_PATH)

# Compute ARI
ari = adjusted_rand_score(df_stab["cl250"], df_stab["cl500"])
print(f"ARI: {ari:.3f}")

# Cross tab
ct = pd.crosstab(df_stab["cl250"], df_stab["cl500"])
# Normalize by row sums (250m clusters)
ct_norm = ct.div(ct.sum(axis=1), axis=0) * 100

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Set up matplotlib figure
fig, axes = plt.subplots(1, 2, figsize=(13, 6.0), facecolor="#ffffff")
axes[0].set_facecolor("#ffffff")
axes[1].set_facecolor("#ffffff")

# Panel a: Confusion matrix heatmap (use sequential colormap based on Primary Gold)
# dynamic tick labels (robust to any k at either resolution)
cluster_names_250 = [f"C{int(i)} (250m)" for i in ct.index]
cluster_names_500 = [f"C{int(j)} (500m)" for j in ct.columns]

gold_cmap = sns.light_palette("#E9B420", as_cmap=True)

sns.heatmap(ct, annot=True, fmt="d", cmap=gold_cmap, cbar=True, ax=axes[0],
            xticklabels=cluster_names_500, yticklabels=cluster_names_250,
            annot_kws={"size": 11, "weight": "bold"}, edgecolor="#cbd5e1", linewidths=0.5)
axes[0].set_title(f"(a) Classification scale agreement (ARI = {ari:.3f})", fontsize=11.5, fontweight="bold", color="#1e293b")
axes[0].set_ylabel("250 m Grid Clustering (Super-types)", fontsize=10)
axes[0].set_xlabel("500 m Grid Clustering (Super-types)", fontsize=10)

# silhouette-vs-k curves read from the authoritative pipeline outputs (no hardcoding)
TAB = os.path.join(PROJ, "outputs", "tables")
sc250 = pd.read_csv(os.path.join(TAB, "silhouette_curve_250.csv"))
sc500 = pd.read_csv(os.path.join(TAB, "silhouette_curve_500.csv"))
ks = sc250["k"].tolist()
axes[1].plot(sc250["k"], sc250["silhouette"], marker="o", color="#E9B420", linewidth=2.0, label="250 m Grid")
axes[1].plot(sc500["k"], sc500["silhouette"], marker="s", color="#8E8E8D", linewidth=2.0, label="500 m Grid")
# optimal k at each scale = argmax silhouette among admissible partitions (min cluster >= 10)
k_opt_250 = int(sc250[sc250["ok"]].sort_values("silhouette").iloc[-1]["k"])
k_opt_500 = int(sc500[sc500["ok"]].sort_values("silhouette").iloc[-1]["k"])
axes[1].axvline(k_opt_250, color="#E9B420", linestyle="--", alpha=0.8)
axes[1].axvline(k_opt_500, color="#8E8E8D", linestyle="--", alpha=0.8)
axes[1].text(0.975, 0.96,
             f"Optimal k (max silhouette)\n• 250 m grid  →  k = {k_opt_250}\n• 500 m grid  →  k = {k_opt_500}",
             transform=axes[1].transAxes, ha="right", va="top", fontsize=9, color="#334155",
             bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#cbd5e1", lw=0.8, alpha=0.95))
axes[1].set_title("(b) Clustering quality & optimal cluster size (k)", fontsize=11.5, fontweight="bold", color="#1e293b")
axes[1].set_xlabel("Number of Clusters (k)", fontsize=10)
ax1 = axes[1]
ax1.set_ylabel("Mean Silhouette Score", fontsize=10)
ax1.set_xticks(ks)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax1.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.95)
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

fig.suptitle("Grid-resolution scale-stability analysis — 250 m vs. 500 m", fontsize=14, fontweight="bold", color="#0f172a", y=0.975)
fig.text(0.5, 0.918, "Cluster classifications compared across grid resolutions; ARI quantifies agreement, silhouette guides the choice of k",
         ha="center", va="center", fontsize=9.5, color="#475569")
fig.tight_layout(rect=(0, 0, 1, 0.88))
fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Successfully generated Figure 5: {OUT_FIG}")
