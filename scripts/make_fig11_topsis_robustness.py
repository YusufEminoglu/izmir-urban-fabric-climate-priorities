import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "figure11.png")

df_ind = pd.read_csv(IND_PATH)

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

def topsis(M, w):
    N = M / np.sqrt((M ** 2).sum(0))
    V = N * w
    ideal, anti = V.max(0), V.min(0)
    dp = np.sqrt(((V - ideal) ** 2).sum(1))
    dn = np.sqrt(((V - anti) ** 2).sum(1))
    return dn / (dp + dn)

rng = np.random.defaultrng(0)
C = np.zeros((2000, len(M)))

for i in range(2000):
    w = rng.dirichlet(np.ones(len(AX)))
    C[i] = topsis(M, w)

strata_names = g["stratum_name"].values
mc_df = pd.DataFrame(C, columns=strata_names)
mc_melted = mc_df.melt(var_name="Stratum", value_name="Score")

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

mean_scores = mc_melted.groupby("Stratum Label")["Score"].mean().sort_values(ascending=False)
strata_labels_order = list(mean_scores.index)

M_norm = (M - M.min(0)) / (M.max(0) - M.min(0))
df_par = pd.DataFrame(M_norm, columns=AX)
df_par["Stratum"] = [strata_labels[s] for s in strata_names]

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, axes = plt.subplots(1, 2, figsize=(14.5, 8.0), facecolor="#ffffff")

colors_strata = {
    "Historic Core": "#E9B420",
    "Grid Res.": "#DDB5B5",
    "Apartment Block": "#EBCB9C",
    "Waterfront Trans.": "#A0CBBF",
    "Hillside / Inc.": "#DEA6A3",
    "Industrial / Log.": "#8E8E8D",
    "Peripheral Exp.": "#C5AFD5"
}

# --- PANEL A: Continuous TOPSIS Score Distribution ---
ax0 = axes[0]
ax0.set_facecolor("#ffffff")

sns.violinplot(
    data=mc_melted,
    x="Stratum Label",
    y="Score",
    ax=ax0,
    hue="Stratum Label",
    palette=colors_strata,
    order=strata_labels_order,
    cut=0,
    bw_adjust=0.8,
    inner=None,
    linewidth=0.8,
    alpha=0.45,
    legend=False
)

sns.boxplot(
    data=mc_melted,
    x="Stratum Label",
    y="Score",
    ax=ax0,
    hue="Stratum Label",
    palette=colors_strata,
    order=strata_labels_order,
    showfliers=False,
    width=0.18,
    boxprops=dict(alpha=0.85, linewidth=1.0),
    whiskerprops=dict(linewidth=1.0, color="#334155"),
    capprops=dict(linewidth=1.0, color="#334155"),
    medianprops=dict(linewidth=1.8, color="#0f172a"),
    legend=False,
    zorder=3
)

sub_sampled = mc_melted.sample(n=1400, random_state=0)
sns.stripplot(
    data=sub_sampled,
    x="Stratum Label",
    y="Score",
    ax=ax0,
    hue="Stratum Label",
    palette=colors_strata,
    order=strata_labels_order,
    size=2.0,
    alpha=0.25,
    jitter=0.15,
    legend=False,
    zorder=2
)

for i, label in enumerate(strata_labels_order):
    m_val = mean_scores[label]
    ax0.text(
        i, m_val + 0.04, f"µ={m_val:.2f}",
        ha="center", va="bottom", fontsize=8.0, fontweight="bold", color="#1e293b",
        bbox=dict(boxstyle="round,pad=0.25", fc="#ffffffcc", ec="#cbd5e1", lw=0.6),
        zorder=4
    )

ax0.set_xlabel("Fabric Stratum", fontsize=10, labelpad=8)
ax0.set_ylabel("TOPSIS Closeness Score (Ci) [0-1]", fontsize=10)
ax0.set_ylim(-0.05, 1.12)
ax0.set_xticks(range(len(strata_labels_order)))
ax0.set_xticklabels(strata_labels_order, rotation=25, ha="right", fontsize=9)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1", axis="y")
for _sp in ["top", "right"]:
    ax0.spines[_sp].set_visible(False)

# --- PANEL B: Enhanced Parallel Coordinates ---
ax1 = axes[1]
ax1.set_facecolor("#ffffff")
axis_names = ["Heat\n(LST)", "Cooling\nDeficit", "Access\nDeficit", "Coastal\nExpo", "Social\nVul"]
x_indices = range(len(axis_names))

for x_idx in x_indices:
    ax1.axvline(x_idx, color="#e2e8f0", linestyle="--", linewidth=1.2, zorder=1)

df_par = df_par.set_index("Stratum").loc[strata_labels_order].reset_index()

for idx, row in df_par.iterrows():
    y_vals = row[AX].values
    s_label = row["Stratum"]
    c_color = colors_strata[s_label]
    
    is_top = idx < 3
    lw = 3.0 if is_top else 2.0
    ms = 7.5 if is_top else 6.0
    alpha = 0.95 if is_top else 0.80
    
    ax1.plot(
        x_indices, y_vals,
        marker="o", markersize=ms, linewidth=lw, alpha=alpha,
        color=c_color, label=s_label, zorder=4 if is_top else 3,
        markeredgecolor="#ffffff", markeredgewidth=0.8
    )

ax1.set_xticks(x_indices)
ax1.set_xticklabels(axis_names, fontsize=9.5, fontweight="bold", color="#1e293b")
ax1.set_ylim(-0.05, 1.08)
ax1.set_ylabel("Normalized Need Value [0-1]", fontsize=10)

P = M / M.sum(0)
k_ent = 1.0 / np.log(len(M))
with np.errstate(divide="ignore", invalid="ignore"):
    E = -k_ent * np.where(P > 0, P * np.log(P), 0).sum(0)
w_ent = (1 - E) / (1 - E).sum()

ent_labels_map = {
    "heat": "Heat (LST)",
    "cooling_deficit": "Cooling Deficit",
    "access_deficit": "Access Deficit",
    "coastal_expo": "Coastal Expo.",
    "social_vul": "Social Vulnerability"
}

ent_pairs = sorted(zip(AX, w_ent), key=lambda t: -t[1])
weights_text = "Entropy Weight Allocations:\n" + "\n".join(
    f"  • {ent_labels_map[ax_key]}: {w * 100:.1f}%" for ax_key, w in ent_pairs)

ax1.text(
    0.03, 0.04, weights_text, transform=ax1.transAxes, ha="left", va="bottom",
    fontsize=8.5, fontweight="bold", color="#1e293b",
    bbox=dict(boxstyle="round,pad=0.45", fc="#ffffffcc", ec="#cbd5e1", lw=0.7), zorder=5
)

ax1.legend(
    loc="upper right", fontsize=8.0, frameon=True,
    facecolor="#ffffffcc", edgecolor="#cbd5e1", framealpha=0.95, ncol=2
)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1", axis="y")
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

plt.subplots_adjust(left=0.07, right=0.965, top=0.88, bottom=0.18, wspace=0.24)

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

img = Image.open(OUT_FIG).convert("RGB")
draw = ImageDraw.Draw(img)
w, h = img.size

try:
    font = ImageFont.truetype("arialbd.ttf", 92)
except:
    font = ImageFont.truetype("arial.ttf", 92)

draw.rectangle([280, 100, 470, 205], fill=(255, 255, 255))
draw.text((310, 110), "(a)", fill=(0, 0, 0), font=font)

draw.rectangle([w//2 + 260, 100, w//2 + 450, 205], fill=(255, 255, 255))
draw.text((w//2 + 290, 110), "(b)", fill=(0, 0, 0), font=font)

img.save(OUT_FIG)
print(f"Successfully generated Figure 11: {OUT_FIG}")
