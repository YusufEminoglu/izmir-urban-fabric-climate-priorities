"""
03_explainable_heat_attribution.py
--------------------------------------------------------------------------------
TreeSHAP Explainable Heat Attribution & Nonlinear Interactions
Trains XGBoost model on summer LST, calculates TreeSHAP values, and outputs
Figure 7 (SHAP synthesis), Figure 8 (Interaction plots), Table 2 (Global
feature importance), and Table 3 (Per-stratum mechanisms).
--------------------------------------------------------------------------------
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import xgboost as xgb
import shap
import seaborn as sns

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJ_DIR, "data", "03_processed", "cell_indicators.csv")
FIG7_OUT = os.path.join(PROJ_DIR, "outputs", "figures", "figure7.png")
FIG8_OUT = os.path.join(PROJ_DIR, "outputs", "figures", "figure8.png")
TAB2_OUT = os.path.join(PROJ_DIR, "outputs", "tables", "table2.csv")
TAB3_OUT = os.path.join(PROJ_DIR, "outputs", "tables", "table3.csv")

FEATURES = [
    "bld_cov", "far", "mean_floors", "bld_mean_area", "bld_mean_shape", "bld_orient",
    "str_dens_800", "inter_dens_800", "node_dens_800", "mean_seg_800", "orient_ent_800",
    "f_green", "slope_mean", "dist_coast_km", "dist_core_km"
]

RENAME_MAP = {
    "dist_coast_km": "Distance to coast (km)",
    "f_green": "Green cover fraction",
    "dist_core_km": "Distance to core (km)",
    "bld_mean_area": "Mean building footprint (m²)",
    "slope_mean": "Mean slope (°)",
    "bld_cov": "Building coverage fraction",
    "mean_floors": "Mean building floors",
    "str_dens_800": "Street density (800m)",
    "inter_dens_800": "Intersection density (800m)",
    "node_dens_800": "Node density (800m)",
    "mean_seg_800": "Mean segment length (800m)",
    "orient_ent_800": "Orientation entropy (800m)",
    "bld_orient": "Building orientation",
    "bld_mean_shape": "Building shape complexity",
    "far": "Floor-area ratio (FAR)"
}

FIG6_CMAP = LinearSegmentedColormap.from_list("fig6_palette", ["#3C8D80", "#A0CBBF", "#FFFFFF", "#DEA6A3", "#D97706"])

def run_shap_analysis():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES].copy().fillna(df[FEATURES].median())
    y = df["lst_summer"].values
    
    # Fit XGBoost
    model = xgb.XGBRegressor(n_estimators=400, max_depth=4, learning_rate=0.05,
                             subsample=0.8, colsample_bytree=0.8, random_state=0)
    model.fit(X, y)
    
    explainer = shap.TreeExplainer(model)
    sv = explainer.shap_values(X)
    
    # Global importance Table 2
    imp = pd.DataFrame({
        "feature": FEATURES,
        "mean_abs_shap": np.abs(sv).mean(axis=0)
    }).sort_values("mean_abs_shap", ascending=False)
    imp.to_csv(TAB2_OUT, index=False)
    print(f"Exported Table 2: {TAB2_OUT}")
    
    # Per stratum mechanism Table 3
    df_shap = pd.DataFrame(sv, columns=FEATURES)
    df_shap["stratum_name"] = df["stratum_name"].values
    strata_shap = df_shap.groupby("stratum_name")[FEATURES].mean()
    strata_shap.to_csv(TAB3_OUT)
    print(f"Exported Table 3: {TAB3_OUT}")
    
    # Generate Figure 7
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 8.0), facecolor="#ffffff")
    X_renamed = X.rename(columns=RENAME_MAP)
    
    plt.sca(axes[0])
    shap.summary_plot(sv, X_renamed, show=False, plot_size=None, color_bar=False, cmap=FIG6_CMAP)
    axes[0].set_title("(a) Global SHAP feature attribution", fontsize=14, fontweight="bold", color="#1e293b", pad=12)
    axes[0].set_xlabel("SHAP value (impact on LST, °C)", fontsize=10.5)
    
    divider0 = make_axes_locatable(axes[0])
    cax0 = divider0.append_axes("right", size="3%", pad=0.12)
    sm0 = cm.ScalarMappable(cmap=FIG6_CMAP, norm=mcolors.Normalize(vmin=0, vmax=1))
    sm0.set_array([])
    cbar0 = fig.colorbar(sm0, cax=cax0, ticks=[0.05, 0.95])
    cbar0.ax.set_yticklabels(["Low", "High"], fontsize=9, fontweight="bold")
    cbar0.set_label("Feature value", fontsize=9.5, fontweight="bold", color="#1e293b")
    
    # Heatmap panel b
    sorted_features = imp["feature"].tolist()
    heatmap_data = strata_shap[sorted_features].T
    heatmap_data.index = [RENAME_MAP.get(f, f) for f in sorted_features]
    v = float(np.abs(heatmap_data.values).max())
    
    divider1 = make_axes_locatable(axes[1])
    cax1 = divider1.append_axes("right", size="3%", pad=0.12)
    sns.heatmap(heatmap_data, ax=axes[1], cbar_ax=cax1, cmap=FIG6_CMAP, center=0, vmin=-v, vmax=v,
                annot=True, fmt="+.2f", annot_kws={"size": 8.5},
                cbar_kws={"label": "Mean SHAP impact on LST (°C)"},
                linecolor="#e2e8f0", linewidths=0.5)
    axes[1].set_title("(b) Directional heat mechanisms by fabric", fontsize=14, fontweight="bold", color="#1e293b")
    axes[1].set_xlabel("Fabric stratum", fontsize=10.5)
    
    plt.tight_layout()
    fig.savefig(FIG7_OUT, dpi=300)
    plt.close()
    print(f"Exported Figure 7: {FIG7_OUT}")
    
    # Generate Figure 8 (Interaction scatter)
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.5), facecolor="#ffffff")
    
    # Panel a
    bld_cov_idx = FEATURES.index("bld_cov")
    sc1 = axes[0].scatter(X["bld_cov"].values, sv[:, bld_cov_idx],
                          c=X["f_green"].values, cmap=FIG6_CMAP, s=14, alpha=0.6)
    axes[0].set_title("(a) Built-Green Interaction Effect on Heat", fontsize=14, fontweight="bold", color="#1e293b")
    axes[0].set_xlabel("Building Coverage Fraction (bld_cov)", fontsize=10.5)
    axes[0].set_ylabel("SHAP Value for Building Coverage (°C)", fontsize=10.5)
    axes[0].axhline(0, color="#8E8E8D", linestyle="--", alpha=0.5)
    cbar1 = fig.colorbar(sc1, ax=axes[0])
    cbar1.set_label("Green Cover Fraction", fontsize=9.5, fontweight="bold")
    
    # Panel b
    dist_coast_idx = FEATURES.index("dist_coast_km")
    sc2 = axes[1].scatter(X["dist_coast_km"].values, sv[:, dist_coast_idx],
                          c=X["far"].values, cmap=FIG6_CMAP, s=14, alpha=0.6)
    axes[1].set_title("(b) Coastal Gradient & Density Joint Effect", fontsize=14, fontweight="bold", color="#1e293b")
    axes[1].set_xlabel("Distance to Coastline (km)", fontsize=10.5)
    axes[1].set_ylabel("SHAP Value for Coastal Distance (°C)", fontsize=10.5)
    axes[1].axhline(0, color="#8E8E8D", linestyle="--", alpha=0.5)
    cbar2 = fig.colorbar(sc2, ax=axes[1])
    cbar2.set_label("Floor-Area Ratio (FAR)", fontsize=9.5, fontweight="bold")
    
    for ax in axes:
        ax.set_facecolor("#ffffff")
        ax.grid(True, linestyle=":", alpha=0.5, color="#cbd5e1")
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
            
    plt.tight_layout()
    fig.savefig(FIG8_OUT, dpi=300)
    plt.close()
    print(f"Exported Figure 8: {FIG8_OUT}")

if __name__ == "__main__":
    run_shap_analysis()
