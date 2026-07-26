import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import xgboost as xgb
import shap
from PIL import Image, ImageDraw, ImageFont

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "figure8.png")

df_ind = pd.read_csv(IND_PATH)

MORPH = ["bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
         "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
         "f_green", "slope_mean"]
CONTEXT = ["dist_coast_km", "dist_core_km"]
FEATURES = MORPH + CONTEXT

def prep(df_in):
    Xx = df_in[FEATURES].copy()
    for c in ["bld_cov", "far", "mean_floors", "bld_mean_area"]:
        Xx[c] = Xx[c].fillna(0.0)
    Xx = Xx.fillna(Xx.median())
    for c in Xx.columns:
        Xx[c] = Xx[c].clip(Xx[c].quantile(0.01), Xx[c].quantile(0.99))
    return Xx

X = prep(df_ind)
y = df_ind["lst_summer"].values

params = dict(n_estimators=400, max_depth=4, learning_rate=0.05, subsample=0.8,
              colsample_bytree=0.8, random_state=0)
model = xgb.XGBRegressor(**params).fit(X, y)
expl = shap.TreeExplainer(model)
sv = expl.shap_values(X)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.5), facecolor="#ffffff")

def draw_trendline(x_vals, y_vals, ax, color="#475569"):
    idx_sort = np.argsort(x_vals)
    x_s = x_vals[idx_sort]
    y_s = y_vals[idx_sort]
    y_smooth = pd.Series(y_s).rolling(window=60, center=True, min_periods=10).mean().values
    ax.plot(x_s, y_smooth, color=color, linewidth=2.5, zorder=3, label="Smoothed Trend")

from matplotlib.colors import LinearSegmentedColormap
fig6_cmap = LinearSegmentedColormap.from_list("fig6_palette", ["#3C8D80", "#A0CBBF", "#FFFFFF", "#DEA6A3", "#D97706"])

# Panel a
ax0 = axes[0]
ax0.set_facecolor("#ffffff")
bld_cov_idx = FEATURES.index("bld_cov")
f_green_idx = FEATURES.index("f_green")

sc1 = ax0.scatter(X["bld_cov"].values, sv[:, bld_cov_idx],
                  c=X["f_green"].values, cmap=fig6_cmap, edgecolor="none", s=14, alpha=0.6, zorder=2)
draw_trendline(X["bld_cov"].values, sv[:, bld_cov_idx], ax0, color="#ef4444")
ax0.set_xlabel("Building Coverage Fraction (bld_cov)", fontsize=10.5)
ax0.set_ylabel("SHAP Value for Building Coverage (°C)", fontsize=10.5)
ax0.axhline(0, color="#8E8E8D", linestyle="--", alpha=0.5, zorder=1)

divider0 = make_axes_locatable(ax0)
cax0 = divider0.append_axes("right", size="3%", pad=0.12)
cbar1 = fig.colorbar(sc1, cax=cax0)
cbar1.set_label("Green Cover Fraction (f_green)", fontsize=9.5, fontweight="bold", color="#1e293b")
cbar1.ax.tick_params(labelsize=9)

ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax0.legend(loc="upper right", fontsize=9.5, framealpha=0.95)
for _sp in ["top", "right"]:
    ax0.spines[_sp].set_visible(False)

# Panel b
ax1 = axes[1]
ax1.set_facecolor("#ffffff")
dist_coast_idx = FEATURES.index("dist_coast_km")
far_idx = FEATURES.index("far")

sc2 = ax1.scatter(X["dist_coast_km"].values, sv[:, dist_coast_idx],
                  c=X["far"].values, cmap=fig6_cmap, edgecolor="none", s=14, alpha=0.6, zorder=2)
draw_trendline(X["dist_coast_km"].values, sv[:, dist_coast_idx], ax1, color="#ef4444")
ax1.set_xlabel("Distance to Coastline (km)", fontsize=10.5)
ax1.set_ylabel("SHAP Value for Coastal Distance (°C)", fontsize=10.5)
ax1.axhline(0, color="#8E8E8D", linestyle="--", alpha=0.5, zorder=1)

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="3%", pad=0.12)
cbar2 = fig.colorbar(sc2, cax=cax1)
cbar2.set_label("Floor-Area Ratio (FAR)", fontsize=9.5, fontweight="bold", color="#1e293b")
cbar2.ax.tick_params(labelsize=9)

ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax1.legend(loc="upper right", fontsize=9.5, framealpha=0.95)
for _sp in ["top", "right"]:
    ax1.spines[_sp].set_visible(False)

plt.subplots_adjust(top=0.92, bottom=0.14, left=0.08, right=0.94, wspace=0.38)

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

img = Image.open(OUT_FIG).convert("RGB")
draw = ImageDraw.Draw(img)
w, h = img.size

try:
    font = ImageFont.truetype("arialbd.ttf", 92)
except:
    font = ImageFont.truetype("arial.ttf", 92)

draw.rectangle([280, 10, 470, 115], fill=(255, 255, 255))
draw.text((310, 20), "(a)", fill=(0, 0, 0), font=font)

draw.rectangle([w//2 + 260, 10, w//2 + 450, 115], fill=(255, 255, 255))
draw.text((w//2 + 290, 20), "(b)", fill=(0, 0, 0), font=font)

img.save(OUT_FIG)
print(f"Successfully generated Figure 8: {OUT_FIG}")
