import os
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
SAMPLE_PATH = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
BLD_PATH = os.path.join(PROJ, "data", "01_raw", "buildings", "izmir_buildings_bbb.gpkg")
ROADS_PATH = os.path.join(PROJ, "data", "01_raw", "roads", "izmir_roads_bbb.gpkg")
IND_PATH = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")
OUT_FIG = os.path.join(PROJ, "outputs", "figures", "tissue_comparisons.png")

print("Loading metadata...")
df_ind = pd.read_csv(IND_PATH)
sample_gdf = gpd.read_file(SAMPLE_PATH).to_crs(32635)

# Standardized strata list with all 7 strata
strata_list = [
    ("historic_core", "Historic Core"),
    ("apartment_block", "Apartment Block"),
    ("waterfront_transformation", "Waterfront Trans."),
    ("hillside_incremental", "Hillside / Inc."),
    ("grid_residential", "Grid Res."),
    ("industrial_logistics", "Industrial / Log."),
    ("peripheral_expansion", "Peripheral Exp.")
]

# Matplotlib configuration for consistency
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'

# Create a 7 rows x 5 columns plot
fig, axes = plt.subplots(7, 5, figsize=(12, 14.5), facecolor="#ffffff")

# Custom colors for buildings based on floors using style guide colors
def get_bld_color(floors):
    if floors <= 2:
        return "#EBCB9C"  # Soft Orange/Peach
    elif floors <= 4:
        return "#A0CBBF"  # Soft Teal/Green
    elif floors <= 8:
        return "#DDB5B5"  # Soft Pink/Red
    else:
        return "#E9B420"  # Primary Gold

for row_idx, (stratum, label) in enumerate(strata_list):
    # Sort cells of this stratum by building count to find percentiles
    sub_ind = df_ind[df_ind["stratum_name"] == stratum].copy().sort_values("bld_count")
    n_cells = len(sub_ind)
    
    idx_10 = int(n_cells * 0.10)
    idx_30 = int(n_cells * 0.30)
    idx_50 = int(n_cells * 0.50)
    idx_70 = int(n_cells * 0.70)
    idx_90 = int(n_cells * 0.90)
    
    cell_indices = [idx_10, idx_30, idx_50, idx_70, idx_90]
    density_labels = ["Very Low (10%)", "Low (30%)", "Median (50%)", "High (70%)", "Very High (90%)"]
    
    for col_idx, cell_pos in enumerate(cell_indices):
        ax = axes[row_idx, col_idx]
        ax.set_facecolor("#ffffff")
        
        best_cell = sub_ind.iloc[cell_pos]
        sample_id = best_cell["sample_id"]
        bld_count_val = int(best_cell["bld_count"])
        far_val = float(best_cell["far"]) if not pd.isna(best_cell["far"]) else 0.0
        cov_val = float(best_cell["bld_cov"]) if not pd.isna(best_cell["bld_cov"]) else 0.0
        lst_val = float(best_cell["lst_summer"]) if not pd.isna(best_cell["lst_summer"]) else 0.0
        
        # Get grid geometry
        grid_cell = sample_gdf[sample_gdf["sample_id"] == sample_id].iloc[0]
        geom = grid_cell.geometry
        centroid = geom.centroid
        
        minx, miny, maxx, maxy = geom.bounds
        bbox = (minx, miny, maxx, maxy)
        bbox_geom = shapely.box(*bbox)
        
        # Load clipped data directly using bbox argument
        print(f"Querying spatial data for {stratum} (Col {col_idx}, bld_count={bld_count_val})...")
        local_bld = gpd.read_file(BLD_PATH, bbox=bbox).to_crs(32635)
        local_roads = gpd.read_file(ROADS_PATH, bbox=bbox).to_crs(32635)
        
        if not local_bld.empty:
            local_bld["floors"] = pd.to_numeric(local_bld["ZEMINUSTUK"], errors="coerce").fillna(1).clip(1, 40)
            local_bld_clipped = gpd.clip(local_bld, bbox_geom)
        else:
            local_bld_clipped = local_bld
            
        if not local_roads.empty:
            local_roads_clipped = gpd.clip(local_roads, bbox_geom)
        else:
            local_roads_clipped = local_roads
        
        # Plot roads
        if not local_roads_clipped.empty:
            local_roads_clipped.plot(ax=ax, color="#8E8E8D", linewidth=1.2, zorder=1)
            
        # Plot buildings colored by floor height
        if not local_bld_clipped.empty:
            local_bld_clipped["color"] = local_bld_clipped["floors"].apply(get_bld_color)
            local_bld_clipped.plot(ax=ax, color=local_bld_clipped["color"], edgecolor="#1e293b", linewidth=0.5, zorder=2)
                
        # Draw grid cell boundary
        gpd.GeoSeries([geom]).plot(ax=ax, facecolor="none", edgecolor="#1e293b", linestyle="--", linewidth=1.5, zorder=3)
        
        # Style axes (small inner margin so the dashed cell outline is fully visible)
        padx = (bbox[2] - bbox[0]) * 0.03
        pady = (bbox[3] - bbox[1]) * 0.03
        ax.set_xlim(bbox[0] - padx, bbox[2] + padx)
        ax.set_ylim(bbox[1] - pady, bbox[3] + pady)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#cbd5e1")
            s.set_linewidth(0.8)
        
        if row_idx == 0:
            ax.set_title(density_labels[col_idx], fontsize=11, fontweight="bold", color="#1e293b", pad=6)
            
        if col_idx == 0:
            ax.set_ylabel(label, fontsize=11, fontweight="bold", color="#1e293b", labelpad=8)
            
        # Add cell building count, FAR, Coverage, and LST annotation in the corner
        stats_label = f"LST: {lst_val:.1f}°C\nBld: {bld_count_val}\nFAR: {far_val:.2f}\nCov: {cov_val:.2f}"
        ax.text(0.95, 0.05, stats_label, 
                transform=ax.transAxes, ha="right", va="bottom", fontsize=7.0, fontweight="bold",
                color="#1e293b", bbox=dict(boxstyle="round,pad=0.2", fc="#ffffffcc", ec="#cbd5e1", alpha=0.9, lw=0.5), zorder=4)

        # Add scale bar in the bottom-left panel
        if row_idx == 6 and col_idx == 0:
            scale_x = minx + 15
            scale_y = miny + 15
            ax.plot([scale_x, scale_x + 100], [scale_y, scale_y], color="#1e293b", linewidth=3, zorder=4)
            ax.text(scale_x + 50, scale_y + 5, "100 m", ha="center", va="bottom", fontsize=8, fontweight="bold", zorder=4)

# Custom legend for building floors
legend_elements = [
    Rectangle((0, 0), 1, 1, facecolor="#EBCB9C", edgecolor="#1e293b", label="1-2 Floors (Low-rise)"),
    Rectangle((0, 0), 1, 1, facecolor="#A0CBBF", edgecolor="#1e293b", label="3-4 Floors (Mid-rise)"),
    Rectangle((0, 0), 1, 1, facecolor="#DDB5B5", edgecolor="#1e293b", label="5-8 Floors (High-rise)"),
    Rectangle((0, 0), 1, 1, facecolor="#E9B420", edgecolor="#1e293b", label="9+ Floors (Tower)"),
    Rectangle((0, 0), 1, 1, facecolor="none", edgecolor="#1e293b", linestyle="--", label="250m Analysis Cell")
]
fig.legend(handles=legend_elements, loc="lower center", ncol=5, fontsize=10, framealpha=0.95, facecolor="#ffffff", edgecolor="#cbd5e1")

fig.suptitle("Systematic urban-fabric comparison — building morphology & street networks",
             fontsize=13.5, fontweight="bold", color="#0f172a", y=0.99)
fig.text(0.5375, 0.962,
         "250 m × 250 m grid cells across the seven fabric strata  ·  N = 35 panels  ·  all panels share scale and extent",
         ha="center", va="center", fontsize=9.5, color="#475569")
plt.subplots_adjust(bottom=0.05, top=0.93, left=0.085, right=0.99, hspace=0.06, wspace=0.025)
fig.savefig(OUT_FIG, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
print(f"Successfully generated Figure 6 (tissue comparisons): {OUT_FIG}")
