# Open-Source Urban Analytics for Climate-Resilience Screening

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![QGIS 3.34+](https://img.shields.io/badge/QGIS-3.34%2B-green.svg)](https://qgis.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20753131.svg)](https://doi.org/10.5281/zenodo.20753131)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0005--6000--2934-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0005-6000-2934)

**Authors:** **Yusuf Eminoglu**¹✉, **Halil Topcu**², **Hilmi Evren Erdin**¹  
*¹ Department of City and Regional Planning, Dokuz Eylul University, İzmir, Türkiye*  
*² Graduate School of Natural and Applied Sciences, Urban Design Program, İzmir Demokrasi University, İzmir, Türkiye*  
✉ *Corresponding author:* [yusuf.eminoglu@deu.edu.tr](mailto:yusuf.eminoglu@deu.edu.tr)

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
izmir-urban-fabric-climate-priorities/
├── CITATION.cff            # Citation File Format metadata
├── LICENSE                 # MIT Open-Source License
├── README.md               # Repository documentation
├── requirements.txt        # Python package environment
├── data/
│   └── 03_processed/       # Processed cell-level indicators (3,777 cells)
│       └── cell_indicators.csv
├── outputs/
│   ├── figures/            # Manuscript figures (figure1.png-figure11.png, figure_s1.png-figure_s7.png)
│   └── tables/             # Exported statistical summary tables (table1.csv to table8.csv)
└── scripts/                # Reproducible Python processing pipeline
    ├── 01_spatial_grid_processing.py           # Spatial grid construction & indicator synthesis
    ├── 02_morphometric_typology.py             # Unsupervised morphometric clustering (Figure 6 & Table 1)
    ├── 03_explainable_heat_attribution.py      # TreeSHAP feature attribution & interactions (Figures 7, 8 & Tables 2, 3)
    ├── 04_spatial_autocorrelation.py           # Spatial autocorrelation & LISA diagnostics (Figure 9 & Table 6)
    ├── 05_pareto_topsis_prioritization.py      # Pareto screening & TOPSIS Monte Carlo robustness (Figures 10, 11 & Tables 4, 5, 8)
    ├── make_fig04_fabric_comparison.py         # Figure 4: fabric-strata statistical comparison
    ├── make_fig06_cluster_synthesis.py         # Figure 6: dendrogram, silhouette, PCA scatter
    ├── make_fig07_shap_synthesis.py            # Figure 7: SHAP global importance & per-stratum heatmap
    ├── make_fig08_explainable_heat_interactions.py # Figure 8: SHAP interaction diagnostics
    ├── make_fig10_priority_synthesis.py        # Figure 10: Pareto priority synthesis
    ├── make_fig11_topsis_robustness.py         # Figure 11: TOPSIS Monte Carlo robustness
    └── run_reproduction.py                     # Master reproduction entry point
```

**Reproducibility note.** Figures 1, 2, 3, 5, 9 and the seven supplementary figures
(`figure_s1.png`-`figure_s7.png`) are exported outputs of the analysis pipeline above
(study-area mapping, methodology diagram, tissue comparisons, raw indicator maps,
spatial-statistics maps, and supplementary diagnostics); their standalone plotting
scripts are still being cleaned up for release and are not yet included in
`scripts/`. All underlying numerical results for every figure are fully reproducible
from `01`-`05` and the processed data in `data/03_processed/`.

---

## ⚙️ Installation & Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YusufEminoglu/izmir-urban-fabric-climate-priorities.git
cd izmir-urban-fabric-climate-priorities
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
@misc{eminoglu2026resilience,
  author       = {Eminoglu, Yusuf and Topcu, Halil and Erdin, Hilmi Evren},
  title        = {{Open-Source Urban Analytics for Climate-Resilience Screening: A Two-Stage Explainable and Robust Prioritization of Urban Fabrics}},
  year         = {2026},
  month        = {6},
  version      = {v1.0.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20753131},
  url          = {https://doi.org/10.5281/zenodo.20753131}
}
```

---

## 👥 Authors & Affiliations

- **Yusuf Eminoglu** *(Corresponding Author)*  
  Department of City and Regional Planning, Dokuz Eylul University, İzmir, Türkiye  
  📧 **Email:** [yusuf.eminoglu@deu.edu.tr](mailto:yusuf.eminoglu@deu.edu.tr) | 🆔 **ORCID:** [0009-0005-6000-2934](https://orcid.org/0009-0005-6000-2934) | 🌐 **GitHub:** [@YusufEminoglu](https://github.com/YusufEminoglu)

- **Halil Topcu**  
  Graduate School of Natural and Applied Sciences, Urban Design Program, İzmir Demokrasi University, İzmir, Türkiye  
  🆔 **ORCID:** [0009-0009-3366-179X](https://orcid.org/0009-0009-3366-179X)

- **Hilmi Evren Erdin**  
  Department of City and Regional Planning, Dokuz Eylul University, İzmir, Türkiye  
  📧 **Email:** [evren.erdin@deu.edu.tr](mailto:evren.erdin@deu.edu.tr) | 🆔 **ORCID:** [0000-0002-3350-8930](https://orcid.org/0000-0002-3350-8930)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
