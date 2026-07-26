import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
PRIO_PATH = os.path.join(PROJ, "data", "03_processed", "cell_priority.csv")
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
os.makedirs(FIGDIR, exist_ok=True)

df_prio = pd.read_csv(PRIO_PATH)
df_ind = pd.read_csv(IND_PATH)

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Define axes
AX = ["heat", "cooling_deficit", "access_deficit", "coastal_expo", "social_vul"]
axes_labels = ["Heat", "Cooling Def.", "Access Def.", "Coastal Expo.", "Social Vul."]
colors_list = ["#E9B420", "#EBCB9C", "#A0CBBF", "#DEA6A3", "#C5AFD5"]

# Generate Dirichlet weights (2,000 runs)
rng = np.random.default_rng(0)
weights = rng.dirichlet(np.ones(5), size=2000)

fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor="#ffffff")

# --- Panel (a): Dirichlet weights boxplot ---
ax0 = axes[0, 0]
ax0.set_facecolor("#ffffff")

bp = ax0.boxplot([weights[:, i] for i in range(5)], tick_labels=axes_labels, patch_artist=True)
for patch, color in zip(bp['boxes'], colors_list):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    patch.set_edgecolor("#64748B")

for whisker in bp['whiskers']:
    whisker.set_color("#64748B")
    whisker.set_linewidth(1.0)
for cap in bp['caps']:
    cap.set_color("#64748B")
for median in bp['medians']:
    median.set_color("#1e293b")
    median.set_linewidth(1.5)

ax0.set_title("(a) Dirichlet Distribution of Weights in Monte Carlo Runs", fontsize=11, fontweight="bold", color="#1e293b")
ax0.set_ylabel("Weight Fraction", fontsize=9.5)
ax0.set_xlabel("Adaptation Axis", fontsize=9.5)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")

# --- Panel (b): Kendall rank correlation matrix between weighting regimes (cell level) ---
ax1 = axes[0, 1]
ax1.set_facecolor("#ffffff")

M_cell = df_prio[AX].values
def run_topsis(M, w):
    N = M / np.sqrt((M ** 2).sum(0))
    V = N * w
    ideal, anti = V.max(0), V.min(0)
    dp = np.sqrt(((V - ideal) ** 2).sum(1))
    dn = np.sqrt(((V - anti) ** 2).sum(1))
    return dn / (dp + dn)

w_eq = np.ones(5) / 5.0
# Calculate entropy weights dynamically from cell priority data M_cell
P = M_cell / M_cell.sum(0)
k = 1.0 / np.log(len(M_cell))
with np.errstate(divide="ignore", invalid="ignore"):
    E = -k * (np.where(P > 0, P * np.log(P), 0.0)).sum(0)
w_ent = (1.0 - E) / (1.0 - E).sum()
w_heat = np.array([0.60, 0.10, 0.10, 0.10, 0.10])
w_access = np.array([0.10, 0.10, 0.60, 0.10, 0.10])
w_social = np.array([0.10, 0.10, 0.10, 0.10, 0.60])

sc_eq = run_topsis(M_cell, w_eq)
sc_ent = run_topsis(M_cell, w_ent)
sc_heat = run_topsis(M_cell, w_heat)
sc_access = run_topsis(M_cell, w_access)
sc_social = run_topsis(M_cell, w_social)

ranks_df = pd.DataFrame({
    "Equal Weights": -sc_eq,
    "Entropy Weights": -sc_ent,
    "Heat Dominant": -sc_heat,
    "Access Dominant": -sc_access,
    "Social Dominant": -sc_social
}).corr(method="kendall")

gold_cmap = sns.light_palette("#E9B420", as_cmap=True)
sns.heatmap(ranks_df, annot=True, cmap=gold_cmap, ax=ax1, vmin=0.2, vmax=1.0, fmt=".3f", 
            annot_kws={"weight": "bold", "size": 8.5}, edgecolor="#cbd5e1", linewidths=0.5)

ax1.set_title("(b) Kendall's Rank Correlation Between Policy Scenarios", fontsize=11, fontweight="bold", color="#1e293b")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=25, ha="right", fontsize=8.5)
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=8.5)

# --- Panel (c): Continuous TOPSIS Closeness Coefficient (Ci) distributions for Strata ---
ax2 = axes[1, 0]
ax2.set_facecolor("#ffffff")

# We run TOPSIS on the aggregated strata matrix M (7 x 5) for all 2,000 runs
g = df_ind.groupby("stratum_name").agg(
    heat=("lst_summer", "mean"), green=("f_green", "mean"),
    inter=("inter_dens_800", "mean"), coast=("dist_coast_km", "mean"),
    svi=("svi", "mean")).reset_index()
g["cooling_deficit"] = 1 - g["green"]
g["access_deficit"] = 1 / (1 + g["inter"])
g["coastal_expo"] = 1 / (1 + g["coast"])
g["social_vul"] = g["svi"] - g["svi"].min()

M_strata = g[AX].values
scores_mc = np.zeros((2000, len(M_strata)))
for i in range(2000):
    scores_mc[i] = run_topsis(M_strata, weights[i])

strata_order = [
    "historic_core",
    "apartment_block",
    "waterfront_transformation",
    "hillside_incremental",
    "grid_residential",
    "industrial_logistics",
    "peripheral_expansion"
]
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

# Find columns indices mapping to strata_order
strata_in_g = g["stratum_name"].tolist()
plot_data = []
for stratum in strata_order:
    idx = strata_in_g.index(stratum)
    plot_data.append(scores_mc[:, idx])

bp_c = ax2.boxplot(plot_data, tick_labels=strata_labels, patch_artist=True)
for patch, stratum in zip(bp_c['boxes'], strata_order):
    patch.set_facecolor(colors_map[stratum])
    patch.set_alpha(0.7)
    patch.set_edgecolor("#64748B")

for whisker in bp_c['whiskers']:
    whisker.set_color("#64748B")
    whisker.set_linewidth(1.0)
for cap in bp_c['caps']:
    cap.set_color("#64748B")
for median in bp_c['medians']:
    median.set_color("#1e293b")
    median.set_linewidth(1.5)

ax2.set_title("(c) Strata TOPSIS Closeness Coefficient (Ci) Distributions", fontsize=11, fontweight="bold", color="#1e293b")
ax2.set_ylabel("TOPSIS Closeness Score (Ci)", fontsize=9.5)
ax2.set_xlabel("Fabric Stratum", fontsize=9.5)
ax2.set_xticks(range(1, len(strata_order)+1))
ax2.set_xticklabels(strata_labels, rotation=25, ha="right", fontsize=8.5)
ax2.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")

# --- Panel (d): Specific Rank Sensitivity analysis for Peripheral Expansion ---
ax3 = axes[1, 1]
ax3.set_facecolor("#ffffff")

# Calculate ranks for all 2,000 runs
ranks_mc = np.zeros((2000, len(M_strata)))
for i in range(2000):
    # rank: descending order (highest score gets rank 1)
    ranks_mc[i] = pd.Series(-scores_mc[i]).rank().values

# Peripheral expansion index in strata list
pe_idx = strata_in_g.index("peripheral_expansion")
pe_ranks = ranks_mc[:, pe_idx]
access_weights = weights[:, 2] # access deficit weight (index 2)

# Scatter plot with regression line
ax3.scatter(access_weights, pe_ranks, color=colors_map["peripheral_expansion"], alpha=0.3, s=15, edgecolors="none")

# Binned average to show clear trend
bins = np.linspace(0, 0.7, 15)
bin_centers = (bins[:-1] + bins[1:]) / 2
bin_means = []
for i in range(len(bins)-1):
    mask = (access_weights >= bins[i]) & (access_weights < bins[i+1])
    bin_means.append(pe_ranks[mask].mean() if mask.sum() > 0 else np.nan)

ax3.plot(bin_centers, bin_means, color="#1e293b", linewidth=2.5, linestyle="-", label="Binned Mean Rank")

ax3.set_title("(d) Peripheral Expansion Priority Rank vs. Access Weight", fontsize=11, fontweight="bold", color="#1e293b")
ax3.set_xlabel("Weight Allocated to Access Deficit Axis ($w_3$)", fontsize=9.5)
ax3.set_ylabel("TOPSIS Rank (1 = Highest, 7 = Lowest)", fontsize=9.5)
ax3.set_ylim(7.5, 0.5) # Invert y-axis to show higher priority (rank 1) at the top
ax3.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax3.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

fig.suptitle("Supplementary Figure S4: Multi-Objective TOPSIS Ranking Weight Sensitivity", fontsize=14, fontweight="bold", color="#0f172a", y=0.98)
plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08, wspace=0.25, hspace=0.30)

out_path = os.path.join(FIGDIR, "supp_topsis_sensitivity.png")
fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

import shutil
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(out_path, os.path.join(figs_cur, "supp_topsis_sensitivity.png"))

print(f"Wrote {out_path}")
