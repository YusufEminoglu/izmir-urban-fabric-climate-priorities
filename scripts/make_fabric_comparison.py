import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal, mannwhitneyu

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "fabric_comparison.png")

print("Loading cell indicators...")
df = pd.read_csv(IND_PATH)

# Define strata order and colors
strata_order = [
    "historic_core",
    "apartment_block",
    "waterfront_transformation",
    "hillside_incremental",
    "grid_residential",
    "industrial_logistics",
    "peripheral_expansion"
]
# Readable labels for plot
strata_labels = [
    "Historic Core",
    "Apartment Block",
    "Waterfront Trans.",
    "Hillside / Inc.",
    "Grid Res.",
    "Industrial / Log.",
    "Peripheral Exp."
]
colors_map = {
    "historic_core": "#E9B420",
    "grid_residential": "#DDB5B5",
    "apartment_block": "#EBCB9C",
    "waterfront_transformation": "#A0CBBF",
    "hillside_incremental": "#DEA6A3",
    "industrial_logistics": "#8E8E8D",
    "peripheral_expansion": "#C5AFD5"
}

indicators = [
    ("far", "Floor-Area Ratio (FAR)", "(a) Built intensity"),
    ("bld_cov", "Building Coverage (fraction)", "(b) Ground coverage"),
    ("mean_floors", "Mean Building Floors", "(c) Building height"),
    ("inter_dens_800", "Intersections per km² (800m reach)", "(d) Street connectivity"),
    ("lst_summer", "Summer LST JJA (°C)", "(e) Measured summer heat"),
    ("svi", "Social Vulnerability Index (SVI)", "(f) Social vulnerability")
]

fig, axes = plt.subplots(2, 3, figsize=(16, 11), facecolor="#ffffff")
axes = axes.ravel()

# Holm-Bonferroni correction function
def holm_bonferroni(p_values, alpha=0.05):
    n = len(p_values)
    rejected = [False] * n
    p_adj = [0.0] * n
    sorted_indices = sorted(range(n), key=lambda k: p_values[k])
    
    for rank, idx in enumerate(sorted_indices):
        p = p_values[idx]
        threshold = alpha / (n - rank)
        if p <= threshold:
            rejected[idx] = True
        else:
            break
            
    running_max = 0.0
    for rank, idx in enumerate(sorted_indices):
        p = p_values[idx]
        adj = p * (n - rank)
        running_max = max(running_max, adj)
        p_adj[idx] = min(running_max, 1.0)
        
    return rejected, p_adj

# Compact Letter Display generator using Bron-Kerbosch
def get_cld_letters(groups_dict, alpha=0.05):
    keys = list(groups_dict.keys())
    n_groups = len(keys)
    if n_groups == 0:
        return {}
    if n_groups == 1:
        return {keys[0]: "a"}
    
    # Pairwise Mann-Whitney U tests
    p_values = []
    pairs = []
    for i in range(n_groups):
        for j in range(i + 1, n_groups):
            g1, g2 = keys[i], keys[j]
            _, p = mannwhitneyu(groups_dict[g1], groups_dict[g2], alternative="two-sided")
            p_values.append(p)
            pairs.append((g1, g2))
            
    # Holm-Bonferroni correction
    rejected, p_adj = holm_bonferroni(p_values, alpha=alpha)
    
    # Build adjacency matrix of non-significant differences
    adj = {k: set() for k in keys}
    for (g1, g2), rej in zip(pairs, rejected):
        if not rej:
            adj[g1].add(g2)
            adj[g2].add(g1)
            
    # Bron-Kerbosch cliques
    cliques = []
    def bron_kerbosch(r, p, x):
        if not p and not x:
            cliques.append(r)
            return
        for v in list(p):
            neighbors = adj[v]
            bron_kerbosch(r | {v}, p & neighbors, x & neighbors)
            p.remove(v)
            x.add(v)
            
    bron_kerbosch(set(), set(keys), set())
    
    # Sort cliques by average group mean
    clique_means = []
    for cliq in cliques:
        m = np.mean([np.mean(groups_dict[v]) for v in cliq])
        clique_means.append((m, cliq))
    clique_means.sort(key=lambda x: x[0], reverse=True)
    
    # Map cliques to letters
    letters = "abcdefghijklmnopqrstuvwxyz"
    group_letters = {k: [] for k in keys}
    for c_idx, (_, cliq) in enumerate(clique_means):
        let = letters[c_idx % len(letters)]
        for v in cliq:
            group_letters[v].append(let)
            
    result = {}
    for k in keys:
        joined = "".join(sorted(group_letters[k]))
        result[k] = joined if joined else "-"
    return result

for idx, (col, ylabel, title) in enumerate(indicators):
    ax = axes[idx]
    ax.set_facecolor("#ffffff")
    
    sub_df = df.copy()
    if col in ["mean_floors"]:
        sub_df[col] = sub_df[col].fillna(1)
        
    # 1. Violin Plot
    sns.violinplot(
        data=sub_df, x="stratum_name", y=col, ax=ax, hue="stratum_name", palette=colors_map, order=strata_order,
        linewidth=0.8, inner="box", density_norm="width", alpha=0.35, legend=False
    )
    
    # 2. Overlay Strip Plot
    sns.stripplot(
        data=sub_df, x="stratum_name", y=col, ax=ax, order=strata_order, hue="stratum_name", palette=colors_map,
        size=2.0, alpha=0.4, jitter=0.25, legend=False, zorder=1
    )
    
    # 3. Sample Mean line
    mean_val = sub_df[col].dropna().mean()
    ax.axhline(mean_val, color="#64748b", linestyle="--", linewidth=1.0, alpha=0.8, zorder=0)
    
    # Format mean label
    if col == "lst_summer":
        mean_label = f"Mean: {mean_val:.1f}°C"
    elif col == "inter_dens_800":
        mean_label = f"Mean: {mean_val:.0f}"
    else:
        mean_label = f"Mean: {mean_val:.2f}"
        
    ax.text(len(strata_order) - 0.5, mean_val, f" {mean_label}", color="#475569", 
            ha="right", va="bottom", fontsize=7.5, fontweight="bold")
            
    # Calculate Kruskal-Wallis and Eta-squared
    groups_dict = {s: sub_df[sub_df["stratum_name"] == s][col].dropna().values for s in strata_order if len(sub_df[sub_df["stratum_name"] == s][col].dropna()) > 0}
    groups = list(groups_dict.values())
    
    h_stat = 0.0
    p_val = 1.0
    eta_sq = 0.0
    
    if len(groups) > 1:
        h_stat, p_val = kruskal(*groups)
        # Eta-squared = (H - k + 1) / (n - k)
        k_groups = len(groups)
        n_obs = sum(len(g) for g in groups)
        eta_sq = (h_stat - k_groups + 1) / (n_obs - k_groups) if n_obs > k_groups else 0.0
        
        p_str = "p < 0.001" if p_val < 0.001 else f"p = {p_val:.3f}"
        stats_label = f"Kruskal-Wallis H = {h_stat:.1f}\n{p_str}\n$\\eta^2 = {eta_sq:.3f}$"
        ax.text(0.95, 0.95, stats_label, transform=ax.transAxes, ha="right", va="top",
                fontsize=8, fontweight="bold", color="#1e293b",
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#cbd5e1", alpha=0.9, lw=0.5))
                
        # Get and plot CLD letters
        cld_letters = get_cld_letters(groups_dict)
        
        # Position letters above each violin
        y_lims = ax.get_ylim()
        y_range = y_lims[1] - y_lims[0]
        
        for s_idx, s_name in enumerate(strata_order):
            if s_name in cld_letters:
                s_data = groups_dict[s_name]
                if len(s_data) > 0:
                    y_pos = np.percentile(s_data, 95) + 0.03 * y_range
                    y_pos = min(y_pos, y_lims[1] - 0.05 * y_range)
                    letter = cld_letters[s_name]
                    
                    ax.text(s_idx, y_pos, letter, ha="center", va="bottom",
                            fontsize=9, fontweight="bold", color="#334155",
                            bbox=dict(boxstyle="circle,pad=0.1", fc="#ffffff", ec="#e2e8f0", alpha=0.8, lw=0.3))
                            
    # Style axis
    ax.set_title(title, fontsize=11.5, fontweight="bold", color="#1e293b")
    ax.set_ylabel(ylabel, fontsize=9.5, color="#334155")
    ax.set_xlabel("")
    ax.set_xticks(range(len(strata_order)))
    ax.set_xticklabels(strata_labels, rotation=30, ha="right", fontsize=8.5, color="#334155")
    ax.grid(True, linestyle=":", alpha=0.5, axis="y")
    ax.tick_params(axis="y", labelsize=8.5)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

fig.tight_layout()
fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

import shutil
outputs_fig = os.path.dirname(OUT_FIG)
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(OUT_FIG, os.path.join(figs_cur, "fabric_comparison.png"))

print(f"Successfully generated fabric comparison figure: {OUT_FIG}")
