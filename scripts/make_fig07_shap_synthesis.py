import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import xgboost as xgb
import shap
from sklearn.cluster import KMeans
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_squared_error
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "figure7.png")

df = pd.read_csv(IND_PATH)

MORPH = ["bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
         "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
         "f_green", "slope_mean"]
CONTEXT = ["dist_coast_km", "dist_core_km"]
FEATURES = MORPH + CONTEXT

def prep(cols):
    Xx = df[cols].copy()
    for c in ["bld_cov", "far", "mean_floors", "bld_mean_area"]:
        if c in Xx:
            Xx[c] = Xx[c].fillna(0.0)
    Xx = Xx.fillna(Xx.median())
    for c in Xx.columns:
        Xx[c] = Xx[c].clip(Xx[c].quantile(0.01), Xx[c].quantile(0.99))
    return Xx

y = df["lst_summer"].values
blocks = KMeans(n_clusters=6, random_state=0, n_init=10).fit_predict(df[["x", "y"]].values)
params = dict(n_estimators=400, max_depth=4, learning_rate=0.05, subsample=0.8,
              colsample_bytree=0.8, random_state=0)
gkf = GroupKFold(n_splits=6)

def cv_r2(cols):
    Xx = prep(cols)
    oof = np.zeros(len(y))
    for tr, te in gkf.split(Xx, y, groups=blocks):
        m = xgb.XGBRegressor(**params).fit(Xx.iloc[tr], y[tr])
        oof[te] = m.predict(Xx.iloc[te])
    return r2_score(y, oof), np.sqrt(mean_squared_error(y, oof))

r2_m, rmse_m = cv_r2(MORPH)
r2, rmse = cv_r2(FEATURES)

X = prep(FEATURES)
model = xgb.XGBRegressor(**params).fit(X, y)
expl = shap.TreeExplainer(model)
sv = expl.shap_values(X)

imp = pd.DataFrame({"feature": FEATURES, "mean_abs_shap": np.abs(sv).mean(0)}) \
        .sort_values("mean_abs_shap", ascending=False)

svdf = pd.DataFrame(sv, columns=FEATURES)
svdf["stratum_name"] = df["stratum_name"].values
per = svdf.groupby("stratum_name").mean()

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
    "slope_mean": "Mean Slope",
    "dist_coast_km": "Distance to Coast",
    "dist_core_km": "Distance to Core"
}

X_renamed = X.rename(columns=rename_map)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, axes = plt.subplots(1, 2, figsize=(15.5, 8.0), facecolor="#ffffff")

fig6_cmap = LinearSegmentedColormap.from_list("fig6_palette", ["#3C8D80", "#A0CBBF", "#FFFFFF", "#DEA6A3", "#D97706"])

# Panel a
ax0 = axes[0]
ax0.set_facecolor("#ffffff")
plt.sca(ax0)
shap.summary_plot(sv, X_renamed, show=False, plot_size=None, color_bar=False, cmap=fig6_cmap)
ax0.set_xlabel("SHAP value (impact on LST, °C)", fontsize=10.5)
ax0.tick_params(labelsize=9.5)

divider0 = make_axes_locatable(ax0)
cax0 = divider0.append_axes("right", size="3%", pad=0.12)
sm0 = cm.ScalarMappable(cmap=fig6_cmap, norm=mcolors.Normalize(vmin=0, vmax=1))
sm0.set_array([])
cbar0 = fig.colorbar(sm0, cax=cax0, ticks=[0.05, 0.95])
cbar0.ax.set_yticklabels(["Low", "High"], fontsize=9, fontweight="bold")
cbar0.set_label("Feature value", fontsize=9.5, fontweight="bold", color="#1e293b")

# Panel b
ax1 = axes[1]
ax1.set_facecolor("#ffffff")
sorted_features = imp["feature"].tolist()
heatmap_data = per.loc[strata_order, sorted_features].T
heatmap_data.index = [rename_map[f] for f in sorted_features]
heatmap_data.columns = strata_labels
v = float(np.abs(heatmap_data.values).max())

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="3%", pad=0.12)

sns.heatmap(heatmap_data, ax=ax1, cbar_ax=cax1, cmap=fig6_cmap, center=0, vmin=-v, vmax=v,
            annot=True, fmt="+.2f", annot_kws={"size": 8.5},
            cbar_kws={"label": "Mean SHAP impact on LST (°C)"},
            linecolor="#e2e8f0", linewidths=0.5)
cax1.tick_params(labelsize=9)

ax1.set_xlabel("Fabric stratum", fontsize=10.5)
ax1.set_ylabel("Feature (sorted by global importance)", fontsize=10.5)
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=9.5)
ax1.set_xticklabels(strata_labels, rotation=40, ha="right", fontsize=9.5)
ax1.tick_params(length=0)

metrics_text = (
    f"Spatial-Block Cross-Validation Performance Summary:\n"
    f"Full Model (Morphology + Context): R² = {r2:.2f}, RMSE = {rmse:.2f}°C  |  "
    f"Morphology-Only Model: R² = {r2_m:.2f}, RMSE = {rmse_m:.2f}°C"
)
fig.text(0.5, 0.035, metrics_text, ha="center", fontsize=10.0, fontweight="bold",
         color="#1e293b", bbox=dict(boxstyle="round,pad=0.5", fc="#ffffff", ec="#cbd5e1", alpha=0.9, lw=0.6))

plt.subplots_adjust(left=0.135, right=0.965, top=0.93, bottom=0.24, wspace=0.42)

fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)

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
print(f"Successfully generated Figure 7: {OUT_FIG}")
