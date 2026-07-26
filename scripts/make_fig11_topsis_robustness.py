import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "topsis_robustness.png")

print("Loading data for Figure 17...")
df_ind = pd.read_csv(IND_PATH)

# Re-run Monte Carlo weights at fabric level to get the full 2,000 x 7 matrix for boxplots
g = df_ind.groupby("stratum_name").agg(
    heat=("lst_summer", "mean"), green=("f_green", "mean"),
    inter=("inter_dens_800", "mean"), coast=("dist_coast_km", "mean"),
    svi=("svi", "mean")).reset_index()
g["cooling_deficit"] = 1 - g["green"]
g["access_deficit"] = 1 / (1 + g["inter"])
g["coastal_expo"] = 1 / (1 + g["coast"])
g["social_vul"] = g["svi"] - g["svi"].min()

AX = ["heat", "cooling_deficit", "access_deficit", "coastal_expo", "social_vul"]
M = g[AX].values

# TOPSIS
def topsis(M, w):
    N = M / np.sqrt((M ** 2).sum(0))
    V = N * w
    ideal, anti = V.max(0), V.min(0)
    dp = np.sqrt(((V - ideal) ** 2).sum(1))
    dn = np.sqrt(((V - anti) ** 2).sum(1))
    return dn / (dp + dn)

rng = np.random.default_rng(0)
R = np.zeros((2000, len(M)))
for i in range(2000):
    w = rng.dirichlet(np.ones(len(AX)))
    sc = topsis(M, w)
    R[i] = pd.Series(-sc).rank().values  # rank 1 = highest priority

# Prepare df for boxplot
strata_names = g["stratum_name"].values
mc_df = pd.DataFrame(R, columns=strata_names)
mc_melted = mc_df.melt(var_name="Stratum", value_name="Rank")

# Readability mappings & standard order
strata_labels = {
    "historic_core": "Historic Core",
    "apartment_block": "Apartment Block",
    "waterfront_transformation": "Waterfront Trans.",
    "hillside_incremental": "Hillside / Inc.",
    "grid_residential": "Grid Res.",
    "industrial_logistics": "Industrial / Log.",
    "peripheral_expansion": "Peripheral Exp."
}
mc_melted["Stratum Label"] = mc_melted["Stratum"].map(strata_labels)

# Normalize the axes to [0, 1] for parallel coordinates plot
M_norm = (M - M.min(0)) / (M.max(0) - M.min(0))
df_par = pd.DataFrame(M_norm, columns=AX)
df_par["Stratum"] = [strata_labels[s] for s in strata_names]

# Standard ordering
strata_order = [
    "historic_core",
    "apartment_block",
    "waterfront_transformation",
    "hillside_incremental",
    "grid_residential",
    "industrial_logistics",
    "peripheral_expansion"
]
strata_labels_order = [strata_labels[s] for s in strata_order]

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Set up figure
fig, axes = plt.subplots(1, 2, figsize=(14, 7.0), facecolor="#ffffff")

# Colors aligned with Figure Style Guide
colors_strata = {
    "Historic Core": "#E9B420",
    "Grid Res.": "#DDB5B5",
    "Apartment Block": "#EBCB9C",
    "Waterfront Trans.": "#A0CBBF",
    "Hillside / Inc.": "#DEA6A3",
    "Industrial / Log.": "#8E8E8D",
    "Peripheral Exp.": "#C5AFD5"
}

# Panel a: Boxplot of Monte Carlo ranks
ax0 = axes[0]
ax0.set_facecolor("#ffffff")

sns.boxplot(data=mc_melted, x="Stratum Label", y="Rank", ax=ax0,
            hue="Stratum Label", palette=colors_strata, order=strata_labels_order,
            showfliers=False, width=0.6, linewidth=1.0, legend=False)

# Overlay soft jittered strip plot to show Monte Carlo density distribution
sns.stripplot(data=mc_melted, x="Stratum Label", y="Rank", ax=ax0,
              hue="Stratum Label", palette=colors_strata, order=strata_labels_order,
              size=1.5, alpha=0.08, jitter=0.25, legend=False, zorder=1)

ax0.set_title("(a) Strata rank robustness under Monte-Carlo weight perturbation", fontsize=11.5, fontweight="bold", color="#1e293b")
ax0.set_xlabel("Fabric Stratum", fontsize=10)
ax0.set_ylabel("Rank (1 = Highest Priority)", fontsize=10)
ax0.set_yticks(range(1, 8))
ax0.set_yticklabels([str(r) for r in range(1, 8)])
ax0.set_ylim(7.5, 0.5) # Rank 1 at top
ax0.set_xticks(range(len(strata_order)), labels=strata_labels_order, rotation=30, ha="right", fontsize=9)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1", axis="y")
for _sp in ["top", "right"]:
    ax0.spines[_sp].set_visible(False)

# Panel b: Parallel coordinates
ax1 = axes[1]
ax1.set_facecolor("#ffffff")
axis_names = ["Heat (LST)", "Cooling Deficit", "Access Deficit", "Coastal Expo", "Social Vul"]
x_indices = range(len(axis_names))

# Sort df_par to plot in standard order so legend matches too
df_par = df_par.set_index("Stratum").loc[strata_labels_order].reset_index()

for idx, row in df_par.iterrows():
    y_vals = row[AX].values
    ax1.plot(x_indices, y_vals, marker="o", linewidth=2.5,
             color=colors_strata[row["Stratum"]], label=row["Stratum"], zorder=4)

ax1.set_xticks(x_indices)
ax1.set_xticklabels(axis_names, fontsize=9.5, fontweight="bold", color="#334155")
ax1.set_ylim(-0.05, 1.05)
ax1.set_title("(b) Trade-offs across adaptation-need axes by stratum", fontsize=11.5, fontweight="bold", color="#1e293b")
ax1.set_ylabel("Normalized Need Value [0-1]", fontsize=10)

# Compute entropy weights (identical formula to pilot_11) and display them
P = M / M.sum(0)
k_ent = 1.0 / np.log(len(M))
with np.errstate(divide="ignore", invalid="ignore"):
    E = -k_ent * np.where(P > 0, P * np.log(P), 0).sum(0)
w_ent = (1 - E) / (1 - E).sum()
ent_pairs = sorted(zip(axis_names, w_ent), key=lambda t: -t[1])
weights_text = "Entropy Weight Allocations:\n" + "\n".join(
    f"  • {name}: {w * 100:.0f}%" for name, w in ent_pairs)
ax1.text(0.05, 0.05, weights_text, transform=ax1.transAxes, ha="left", va="bottom",
         fontsize=8.5, fontweight="bold", color="#1e293b",
         bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#cbd5e1", alpha=0.95, lw=0.6), zorder=5)

ax1.legend(loc="upper right", fontsize=8, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", framealpha=0.95, ncol=2)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

# fig.suptitle and subtext removed per user request for clean figure image
plt.subplots_adjust(left=0.07, right=0.965, top=0.95, bottom=0.145, wspace=0.22)

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Successfully generated Figure 17: {OUT_FIG}")
