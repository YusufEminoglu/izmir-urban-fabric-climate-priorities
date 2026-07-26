"""Pilot step 6 - attach measured summer land-surface temperature to sampled cells.

Builds a multi-year (2014-2024) JJA mean LST surface (nodata -9999 masked) and
extracts the per-cell mean. Adds column `lst_summer` to the indicator table.
Outputs:
  data/02_interim/lst_jja_mean_2014_2024_100m.tif
  data/03_processed/cell_indicators.csv   (with lst_summer)
"""
import os
import glob
import numpy as np
import rasterio
import pandas as pd
import geopandas as gpd
from exactextract import exact_extract

PROJ = r"C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience"
LST_DIR = os.path.join(PROJ, "data", "01_raw", "lst_jja")
SAMPLE = os.path.join(PROJ, "data", "02_interim", "grid_250m_sample.gpkg")
MEAN_TIF = os.path.join(PROJ, "data", "02_interim", "lst_jja_mean_2014_2024_100m.tif")
IND = os.path.join(PROJ, "data", "03_processed", "cell_indicators.csv")

tifs = sorted(glob.glob(os.path.join(LST_DIR, "lst_jja_mean_*_100m.tif")))
print(f"averaging {len(tifs)} JJA scenes ...")
stack = []
with rasterio.open(tifs[0]) as r0:
    prof = r0.profile
for t in tifs:
    with rasterio.open(t) as r:
        a = r.read(1).astype("float32")
        a[a <= -9990] = np.nan
        stack.append(a)
mean_lst = np.nanmean(np.stack(stack), axis=0)
mean_lst = np.where(np.isnan(mean_lst), -9999.0, mean_lst).astype("float32")
prof.update(dtype="float32", nodata=-9999.0, compress="deflate")
with rasterio.open(MEAN_TIF, "w", **prof) as dst:
    dst.write(mean_lst, 1)
valid = mean_lst[mean_lst != -9999.0]
print(f"  mean-LST surface: min {valid.min():.1f} / med {np.median(valid):.1f} / max {valid.max():.1f} degC")

sample = gpd.read_file(SAMPLE).to_crs(32635)
ex = exact_extract(MEAN_TIF, sample, ["mean"], output="pandas", include_cols=["sample_id"])
lst = ex.set_index("sample_id")["mean"].replace(-9999.0, np.nan)

df = pd.read_csv(IND)
df["lst_summer"] = df["sample_id"].map(lst)
df.to_csv(IND, index=False)
print(f"attached lst_summer to {IND} | non-null {df['lst_summer'].notna().sum()}/{len(df)}")
print(df.groupby("stratum_name")["lst_summer"].mean().round(2).to_string())
