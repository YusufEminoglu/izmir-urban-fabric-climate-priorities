"""
01_spatial_grid_processing.py
--------------------------------------------------------------------------------
Spatial Grid Construction & Indicator Synthesis
Metropolitan-scale 250m cell-level spatial indicator processing.
--------------------------------------------------------------------------------
"""

import os
import pandas as pd
import numpy as np

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJ_DIR, "data", "03_processed", "cell_indicators.csv")

def load_cell_indicators():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Cell indicator dataset not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"Successfully loaded {len(df)} urban cells across {len(df.columns)} spatial indicators.")
    return df

if __name__ == "__main__":
    df = load_cell_indicators()
    print("Summary of core indicators:")
    print(df[["bld_cov", "far", "f_green", "lst_summer", "dist_coast_km"]].describe().T[["mean", "std", "min", "max"]])
