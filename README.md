# Open-Source Urban Analytics for Climate-Resilience Screening

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![QGIS 3.34+](https://img.shields.io/badge/QGIS-3.34%2B-green.svg)](https://qgis.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20753131.svg)](https://doi.org/10.5281/zenodo.20753131)

This repository provides the open-source code, spatial analytical pipeline, and processed data for the metropolitan-scale climate-resilience screening framework applied to the İzmir functional urban region.

---

## 📌 Research Overview

Urban climate adaptation requires balancing multiple competing physical and social vulnerabilities across heterogenous urban fabrics. This repository contains the reproducible two-stage **explain-then-optimize** analytics pipeline:

1. **Unsupervised Morphometric Typology & Explainable ML:**
   - Evaluates 13 physical urban form indicators (coverage, FAR, street network centrality, green fraction, slope) and 2 regional context metrics (coastal distance, core distance) across 3,777 contiguous 250 m cells.
   - Fits XGBoost + TreeSHAP models to disentangle nonlinear heat-morphology interactions and coastal cooling buffers.

2. **Multi-Objective Spatial Prioritization (Pareto & TOPSIS):**
   - Screens target areas across five vulnerability/exposure axes (heat, cooling deficit, access deficit, coastal exposure, and social vulnerability).
   - Combines a 5D Pareto dominance filter with entropy-weighted TOPSIS and 2,000-run Monte Carlo robustness testing to establish robust priority tiers.

---

## 📁 Repository Structure

```
explainable-urban-resilience-screening/
├── CITATION.cff            # Citation File Format metadata
├── LICENSE                 # MIT Open-Source License
├── README.md               # Repository documentation
├── requirements.txt        # Python package environment
├── data/
│   └── 03_processed/       # Processed cell-level indicators (3,777 cells)
│       └── cell_indicators.csv
├── outputs/
│   ├── figures/            # High-resolution manuscript figures (fig01 to fig11, fig_s01 to fig_s07)
│   └── tables/             # Exported statistical summary tables (table01 to table08)
└── scripts/                # Reproducible Python processing pipeline
    ├── pilot_01_build_grid.py        # Analysis grid construction (250m)
    ├── pilot_02_enrich.py            # Indicator extraction & spatial joins
    ├── pilot_03_strata.py            # Planning strata definition
    ├── pilot_05_indicators.py        # Cell-level indicator synthesis
    ├── pilot_06_lst.py               # Summer LST satellite processing
    ├── pilot_07_cluster.py           # Hierarchical morphometric clustering
    ├── pilot_08_scale_stability.py   # Multi-scale MAUP sensitivity (250m vs 500m)
    ├── pilot_09_shap.py              # TreeSHAP global feature attribution & heatmap
    ├── pilot_10_vulnerability.py     # Social vulnerability operationalization
    ├── pilot_11_priority.py         # TOPSIS ranking & Monte Carlo sensitivity
    ├── pilot_13_cell_pareto.py       # 5D Pareto frontier extraction & mapping
    ├── make_elite_morphology_maps.py # High-resolution spatial mapping
    ├── make_elite_statistical_collage.py # Nonlinear interaction diagnostics
    └── generate_all_figures.py       # Master figure generation pipeline
```

---

## ⚙️ Installation & Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YusufEminoglu/explainable-urban-resilience-screening.git
cd explainable-urban-resilience-screening
```

### 2. Environment Setup
Create a Python 3.10+ virtual environment and install dependencies:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 Quickstart & Reproduction

To reproduce all figures and statistical tables from the raw indicators:

```bash
# Run complete figure generation pipeline
python scripts/generate_all_figures.py
```

Individual pipeline stages can be executed standalone:
```bash
# Run hierarchical clustering diagnostic (Figure 6)
python scripts/pilot_07_cluster.py

# Run TreeSHAP attribution & heatmap (Figure 7)
python scripts/pilot_09_shap.py

# Run non-linear SHAP interaction plots (Figure 8)
python scripts/make_elite_statistical_collage.py

# Run Pareto frontier mapping (Figure 10)
python scripts/pilot_13_cell_pareto.py

# Run TOPSIS Monte Carlo robustness (Figure 11)
python scripts/make_fig11_topsis_robustness.py
```

---

## 📊 Data Availability & Sources

All analytical steps rely on open-source, publicly accessible datasets:
- **Urban Form & Street Networks:** OpenStreetMap (OSM) via `OSMnx` & official IMM municipal layers.
- **Land Cover & Canopy:** ESA WorldCover 2021 (10m resolution).
- **Surface Temperature (LST):** Landsat 8/9 Collection 2 Tier 1 via Google Earth Engine (Multi-year summer mean 2014–2024).
- **Topography:** Copernicus GLO-30 DEM.
- **Demographics:** TurkStat ADNKS population register.

---

## 📖 Citation

If you find this codebase or methodology useful in your research, please cite:

```bibtex
@misc{eminoglu2026planx,
  author       = {Eminoglu, Yusuf},
  title        = {{PlanX}},
  year         = {2026},
  month        = {6},
  version      = {v4.10},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20753131},
  url          = {https://doi.org/10.5281/zenodo.20753131}
}
```

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
