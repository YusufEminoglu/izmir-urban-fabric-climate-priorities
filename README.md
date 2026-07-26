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
│   ├── figures/            # High-resolution manuscript figures (figure1.png to figure11.png, figure_s1 to figure_s7)
│   └── tables/             # Exported statistical summary tables (table1.csv to table8.csv)
└── scripts/                # Reproducible Python processing pipeline
    ├── 01_spatial_grid_processing.py      # Spatial grid construction & indicator synthesis
    ├── 02_morphometric_typology.py        # Unsupervised morphometric clustering (Figure 6 & Table 1)
    ├── 03_explainable_heat_attribution.py # TreeSHAP feature attribution & interactions (Figures 7, 8 & Tables 2, 3)
    ├── 04_spatial_autocorrelation.py      # Spatial autocorrelation & LISA diagnostics (Figure 9 & Table 6)
    ├── 05_pareto_topsis_prioritization.py # Pareto screening & TOPSIS Monte Carlo robustness (Figures 10, 11 & Tables 4, 5, 8)
    └── run_reproduction.py                # Master reproduction entry point
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

To reproduce all manuscript figures (`figure1.png`–`figure11.png`) and summary tables (`table1.csv`–`table8.csv`):

```bash
# Run complete reproduction pipeline
python scripts/run_reproduction.py
```

Individual pipeline stages can be executed standalone:
```bash
# Stage 1: Spatial grid synthesis
python scripts/01_spatial_grid_processing.py

# Stage 2: Morphometric typology & clustering (Figure 6, Table 1)
python scripts/02_morphometric_typology.py

# Stage 3: TreeSHAP heat attribution & interactions (Figures 7, 8, Tables 2, 3)
python scripts/03_explainable_heat_attribution.py

# Stage 4: Spatial autocorrelation & inequality (Figure 9, Table 6)
python scripts/04_spatial_autocorrelation.py

# Stage 5: Pareto & TOPSIS Monte-Carlo prioritization (Figures 10, 11, Tables 4, 5, 8)
python scripts/05_pareto_topsis_prioritization.py
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
