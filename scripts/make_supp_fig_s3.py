import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
FIGDIR = os.path.join(PROJ, "outputs", "figures")
os.makedirs(FIGDIR, exist_ok=True)

df_ind = pd.read_csv(IND_PATH)

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Define features
MORPH = [
    "bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
    "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
    "f_green", "slope_mean",
]
CONTEXT = ["dist_coast_km", "dist_core_km"]
FEATURES = MORPH + CONTEXT

def prep(cols):
    Xx = df_ind[cols].copy()
    for c in ["bld_cov", "far", "mean_floors", "bld_mean_area"]:
        if c in Xx:
            Xx[c] = Xx[c].fillna(0.0)
    Xx = Xx.fillna(Xx.median())
    for c in Xx.columns:
        Xx[c] = Xx[c].clip(Xx[c].quantile(0.01), Xx[c].quantile(0.99))
    return Xx

y = df_ind["lst_summer"].values
X_full = prep(FEATURES)
X_morph = prep(MORPH)

# 6 spatial block folds
blocks = KMeans(n_clusters=6, random_state=0, n_init=10).fit_predict(df_ind[["x", "y"]].values)
gkf = GroupKFold(n_splits=6)

params = dict(
    n_estimators=400,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=0
)

# Out-of-fold storage
oof_full = np.zeros(len(y))
oof_morph = np.zeros(len(y))

# Learning curves storage
train_rmse_folds = []
val_rmse_folds = []

for train_idx, val_idx in gkf.split(X_full, y, groups=blocks):
    # Full Model
    m_full = XGBRegressor(**params)
    m_full.fit(
        X_full.iloc[train_idx], y[train_idx],
        eval_set=[(X_full.iloc[train_idx], y[train_idx]), (X_full.iloc[val_idx], y[val_idx])],
        verbose=False
    )
    oof_full[val_idx] = m_full.predict(X_full.iloc[val_idx])
    
    # Store learning curve for full model
    results = m_full.evals_result()
    train_rmse_folds.append(results["validation_0"]["rmse"])
    val_rmse_folds.append(results["validation_1"]["rmse"])
    
    # Morphology-Only Model
    m_morph = XGBRegressor(**params)
    m_morph.fit(X_morph.iloc[train_idx], y[train_idx], verbose=False)
    oof_morph[val_idx] = m_morph.predict(X_morph.iloc[val_idx])

# Calculate average learning curves across folds
avg_train_rmse = np.mean(train_rmse_folds, axis=0)
avg_val_rmse = np.mean(val_rmse_folds, axis=0)

# Calculate residuals
res_full = y - oof_full
res_morph = y - oof_morph

# Performance metrics
r2_full = r2_score(y, oof_full)
rmse_full = np.sqrt(mean_squared_error(y, oof_full))
r2_morph = r2_score(y, oof_morph)
rmse_morph = np.sqrt(mean_squared_error(y, oof_morph))

fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor="#ffffff")

# Strata definitions for plotting panel c
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

# --- Panel (a): Learning Curve (spatial-block CV) ---
ax0 = axes[0, 0]
ax0.set_facecolor("#ffffff")
ax0.plot(range(1, len(avg_train_rmse)+1), avg_train_rmse, color="#E9B420", linewidth=2.0, label="Training RMSE")
ax0.plot(range(1, len(avg_val_rmse)+1), avg_val_rmse, color="#8E8E8D", linewidth=2.0, label="Validation RMSE (Out-of-Fold)")
ax0.set_title("(a) XGBoost Spatial-Block CV Learning Curves", fontsize=11, fontweight="bold", color="#1e293b")
ax0.set_xlabel("Number of Boosting Rounds (Trees)", fontsize=9.5)
ax0.set_ylabel("RMSE (°C)", fontsize=9.5)
ax0.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax0.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

# --- Panel (b): Residuals distribution comparison (Full vs Morph-only) ---
ax1 = axes[0, 1]
ax1.set_facecolor("#ffffff")
sns.kdeplot(res_full, ax=ax1, color="#E9B420", fill=True, alpha=0.3, linewidth=2.0, label=f"Full Model (R² = {r2_full:.2f})")
sns.kdeplot(res_morph, ax=ax1, color="#8E8E8D", fill=True, alpha=0.15, linewidth=1.5, linestyle="--", label=f"Morphology-Only (R² = {r2_morph:.2f})")
ax1.axvline(0, color="#ef4444", linestyle=":", linewidth=1.2)
ax1.set_title("(b) Out-of-Fold Prediction Residuals Distribution", fontsize=11, fontweight="bold", color="#1e293b")
ax1.set_xlabel("Residual (Actual LST - Predicted LST, °C)", fontsize=9.5)
ax1.set_ylabel("Density", fontsize=9.5)
ax1.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax1.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

# --- Panel (c): Observed vs Predicted LST scatter (Full Model) ---
ax2 = axes[1, 0]
ax2.set_facecolor("#ffffff")

# Plot points colored by stratum
for stratum in strata_order:
    idx = df_ind["stratum_name"] == stratum
    ax2.scatter(
        y[idx],
        oof_full[idx],
        color=colors_map[stratum],
        label=strata_labels[strata_order.index(stratum)],
        alpha=0.7,
        edgecolors="#334155",
        linewidths=0.4,
        s=30
    )

# 1:1 Reference line
min_val, max_val = min(y), max(y)
ax2.plot([min_val, max_val], [min_val, max_val], color="#ef4444", linestyle="--", linewidth=1.5, label="1:1 Perfect Fit")

ax2.set_title("(c) Observed vs. Out-of-Fold Predicted Summer LST", fontsize=11, fontweight="bold", color="#1e293b")
ax2.set_xlabel("Observed Summer LST (°C)", fontsize=9.5)
ax2.set_ylabel("Predicted Summer LST (°C)", fontsize=9.5)
ax2.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
ax2.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.0)

# Add metrics text box
metrics_text = f"Full Model CV Metrics:\nR² = {r2_full:.2f}\nRMSE = {rmse_full:.2f}°C"
ax2.text(0.95, 0.05, metrics_text, transform=ax2.transAxes, ha="right", va="bottom",
         fontsize=9, fontweight="bold", color="#1e293b",
         bbox=dict(boxstyle="round,pad=0.4", fc="#ffffffcc", ec="#cbd5e1", lw=0.6))

# --- Panel (d): Spatial distribution of Full Model residuals ---
ax3 = axes[1, 1]
ax3.set_facecolor("#ffffff") # Light grey background to mimic maps

# Plot residuals at cell coordinates using a diverging color scale
sc = ax3.scatter(
    df_ind["x"] / 1000.0, # Convert coordinates to km for cleaner axes
    df_ind["y"] / 1000.0,
    c=res_full,
    cmap="RdBu_r",
    vmin=-4.0,
    vmax=4.0,
    edgecolors="#334155",
    linewidths=0.3,
    s=35,
    zorder=2
)
cbar = fig.colorbar(sc, ax=ax3, fraction=0.046, pad=0.04)
cbar.set_label("Prediction Error (Actual - Predicted LST, °C)", fontsize=8.5)
cbar.ax.tick_params(labelsize=8.0)

ax3.set_title("(d) Spatial Map of Prediction Residuals (Full Model)", fontsize=11, fontweight="bold", color="#1e293b")
ax3.set_xlabel("UTM Easting (X, km)", fontsize=9.5)
ax3.set_ylabel("UTM Northing (Y, km)", fontsize=9.5)
ax3.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1", zorder=1)

fig.suptitle("Supplementary Figure S3: Explainable Heat Model XGBoost Regression Diagnostics", fontsize=14, fontweight="bold", color="#0f172a", y=0.98)
plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.08, wspace=0.25, hspace=0.30)

out_path = os.path.join(FIGDIR, "supp_xgb_diagnostics.png")
fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()

import shutil
figs_cur = os.path.join(PROJ, "figs_current")
os.makedirs(figs_cur, exist_ok=True)
shutil.copy2(out_path, os.path.join(figs_cur, "supp_xgb_diagnostics.png"))

print(f"Wrote {out_path}")
