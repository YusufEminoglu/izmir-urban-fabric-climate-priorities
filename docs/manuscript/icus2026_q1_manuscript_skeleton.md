# Q1 Manuscript Skeleton — Street-Scale Urban Morphometrics for Climate Resilience (İzmir Gulf)

**Stage 2 deliverable.** This is the journal-track scaffold seeded by the ICUS 2026 abstract. Sections
1–2 and parts of 3 and 7 are written as near-final prose (they are literature-driven and can be drafted
now). Sections 4–6 are structured scaffolds with `[TO FILL]` markers for empirical content. Citations
use author–year; full list in §References. Calibrated for a balanced method + resilience framing
(*Sustainable Cities and Society* / *Computers, Environment and Urban Systems* / *Landscape and Urban
Planning*). Quartiles and any `[verify]` citations: see the literature positioning dossier.

> **AI-ethics:** this is a scaffold for the authors to verify, rewrite and own. Confirm all empirical
> claims against actual outputs before submission; run a similarity check.

---

## Working title (options)

1. *Grid-Based Urban Morphometrics for Climate Resilience: Explainable, Pareto-Aware Fabric–Resilience Priorities for the İzmir Functional Urban Region*
2. *From Urban Fabric to Adaptation Priority: A Reproducible, Grid-Based Morphometric Workflow for a Coastal Metropolis*
3. *Coupling Morphometrics, Multi-Hazard Exposure and Social Vulnerability on a Sampled Urban Grid: An Open-Source Workflow for the İzmir Region*

## Highlights (Q1 style, ≤85 chars each)

- A grid-based workflow couples urban morphometrics with multi-hazard climate exposure.
- A 250 m grid cell makes form, movement and hazard commensurable in one unit.
- Seven a-priori fabric strata are grid-sampled across the İzmir functional urban region.
- SHAP attributes measured heat to morphology; Pareto + TOPSIS give trade-off-aware priorities.
- All parameters, layers and logs are released for transfer to other coastal metropolises.

## Graphical abstract

`[FIGURE 0]` Four-stage pipeline: (a) stratified grid-cell sampling over the functional region → (b) the
250 m grid cell (tessellation + network cross-attribution; 400/800 m reaches) → (c) morphometric +
resilience indicators (+ GeoStats Lab spatial statistics) → (d) explain (SHAP on measured land-surface
temperature) → optimize (Pareto frontier + TOPSIS), with a named dominant mechanism and a
trade-off-frontier position per profile.

---

## 1. Introduction

Cities concentrate the risks of a warming climate, and the form of the city is increasingly understood
not as a passive backdrop to those risks but as one of their controls. Recent work shows that urban
morphology governs land-surface temperature through both marginal and interaction effects, so that the
thermal behaviour of a neighbourhood cannot be read off its density alone (Wang, Zhou & Yu, 2025); that
heat exposure and the social capacity to cope with it are spatially uneven and frequently decoupled
across urban forms (Turner et al., 2025; Iqbal et al., 2025); and that heat and pluvial flooding act as
compound, interacting hazards rather than independent ones (Imroz et al., 2025). If form shapes risk,
then adaptation that ignores form will misallocate effort.

In parallel, the measurement of urban form has matured rapidly. Urban morphometrics has moved from
case-study description to a reproducible, unsupervised science capable of classifying built fabric at
national and even global scale, using consistent spatial units and open libraries (Fleischmann et al.,
2020, 2022; Araldi & Fusco, 2024; Debray et al., 2025), with interpretable and deep-learning variants
proliferating (Vartholomaios, 2025; Fang et al., 2024; Wang, Huang & Biljecki, 2024). The street network
side is similarly consolidated around reproducible open tooling (Boeing, 2017, 2025). The field can now
say, rigorously and at scale, *what kind of fabric* a place is.

Yet these two trajectories rarely meet at the scale where adaptation is actually designed, financed and
lived: the street and the walkable neighbourhood. Climate-resilience assessment remains dominated by
administrative units, coarse grids and Local Climate Zone tiles. Heat-vulnerability indices, even
excellent open and transferable ones, are typically resolved at the neighbourhood or census scale and
are not mechanistically tied to morphology (Turner et al., 2025); morphometric typologies, conversely,
remain largely descriptive and are seldom connected to hazard outcomes or to adaptation decisions
(Araldi & Fusco, 2024; Debray et al., 2025). The consequence is a practical blind spot: two areas of
similar density and land use can be assigned the same risk class while producing materially different
heat, accessibility and vulnerability outcomes — a divergence the recent empirical literature
documents directly (Wang, Zhou & Yu, 2025; Iqbal et al., 2025) but that coarse-unit assessment cannot
see.

This study addresses that blind spot with an open-source, auditable, QGIS-based typomorphological
workflow for the İzmir Gulf, a coastal metropolitan region with demonstrated and recent exposure to
extreme heat, pluvial flooding and coastal hazard (Cangüzel & Coşkun Hepcan, 2024). The workflow
couples street-scale morphometrics with multi-hazard exposure and social vulnerability to produce
transparent, fabric-specific adaptation priorities. Its methodological core is not the individual tools
but a **catchment–radius cross-attribution rule** that renders movement potential, built-form intensity
and hazard exposure commensurable within a single analytical unit, so that the three are integrated
rather than reported as parallel, unlinked layers. The workflow is deliberately distinguished from
form-only typologies (which stop at description) and from administrative resilience indices (which miss
the street scale at which form is produced and experienced).

**Contributions.** (i) A conceptual disambiguation of *urban fabric* into three registers — fabric as
type, as measurement, and as mechanism — that turns an intuition into a testable proposition. (ii) An
integration unit (the sampled 250 m grid cell: tessellation-cell morphometrics and network metrics
cross-attributed, with 400/800 m accessibility reaches) that makes morphometric, network and hazard
information commensurable. (iii) A two-stage
*explain → optimize* synthesis: an explainable gradient-boosting model with SHAP attributes a measured
outcome (land-surface temperature) to morphological mechanisms, and multi-objective (Pareto) optimisation
with TOPSIS and entropy/Monte-Carlo weight robustness turns those mechanisms into trade-off-aware
adaptation priorities, each profile naming its dominant driver and its position on the adaptation
frontier. (iv) A fully open, parameter-logged, transferable
implementation across the İzmir functional urban region, with the spatial-statistics layer
(Moran/LISA, Getis-Ord, spatial Gini, MGWR) run in GeoStats Lab.

**Research questions.** RQ1: Do fabric types across the İzmir functional urban region differ
systematically in their morphometric, accessibility and hazard-exposure profiles? RQ2: Are the resulting
fabric–resilience classifications stable across grid resolutions (250 m vs 500 m)? RQ3: Which morphological
mechanism dominates *measured* heat in each fabric type, as revealed by SHAP attribution of a
gradient-boosting land-surface-temperature model? RQ4: When adaptation priority is framed as a
multi-objective (Pareto) problem, which fabrics are dominated (clear intervention candidates) versus on
the trade-off frontier, and how robust is the TOPSIS ranking to entropy and Monte-Carlo weight
perturbation?

---

## 2. Background and related work

### 2.1 Reproducible urban morphometrics and fabric typology
Trace the consolidation: morphological tessellation as a consistent plot proxy (Fleischmann et al.,
2020); the numerical-taxonomy logic of contextual characters and unsupervised classification
(Fleischmann et al., 2022); scaling to nationwide street-based taxonomies (Araldi & Fusco, 2024) and
global unsupervised fabric typologies (Debray et al., 2025); interpretable multi-indicator pipelines
(Vartholomaios, 2025) and deep-learning classifiers (Fang et al., 2024; Wang, Huang & Biljecki, 2024).
**Gap framing:** these are predominantly descriptive and form-only.

### 2.2 Urban form as a control on climate hazard
Morphology → LST with marginal/interaction effects (Wang, Zhou & Yu, 2025); compound heat–flood
interactions (Imroz et al., 2025); green–blue NbS cooling quantified across types and scales (Wei et
al., 2025). Explainable ML (XGBoost/GBRT/CatBoost + SHAP) is now the standard lens on morphology→LST
(Wang et al., 2025; Liu et al., 2026; Li et al., 2026); we adopt it at street/cell scale and feed its
SHAP mechanism attributions into the typology. **Gap framing:** typically grid/LCZ scale, single-hazard,
decoupled from accessibility, equity, and from any downstream decision step.

### 2.3 Accessibility, walkability and the street network
Reproducible network analytics (Boeing, 2017, 2025); urban form → proximity/accessibility evidence and
the 15-minute-city assessment turn (Wang, Tsoi & Loo, 2025); Space-Syntax configurational reasoning
(Hillier & Hanson, 1984 `[verify]`). **Gap framing:** accessibility usually treated apart from hazard.

### 2.4 Social vulnerability, heat and climate justice
Open transferable heat-vulnerability indices (Turner et al., 2025); decoupling of exposure and
demographic vulnerability across forms (Iqbal et al., 2025); integrating vulnerability into adaptation
as a justice imperative (Neumann et al., 2026); SoVI lineage (Cutter et al., 2003 `[verify]`).

### 2.5 From MCDA to multi-objective (Pareto) prioritisation
Position TOPSIS (Hwang & Yoon, 1981 `[verify]`) and entropy weighting as transparent, auditable
alternatives to opaque composite indices. Go further: multi-objective (Pareto) optimisation is
established for urban heat and green-infrastructure trade-offs (Zhang et al., 2024; Zhu et al., 2025) but
has not been used for *fabric-level* adaptation priority. Pareto dominance separates unambiguous
intervention candidates from trade-off fabrics; pair it with TOPSIS ranking and Monte-Carlo/RDM weight
robustness (Lempert lineage `[verify]`).

### 2.6 Synthesis of the gap
No existing workflow binds reproducible morphometrics, multi-hazard exposure and social vulnerability on
a sampled metropolitan grid in one commensurable unit and converts them into explainable, Pareto-aware
adaptation priorities. That is the space this paper occupies. `[1–2 sentence explicit statement.]`

---

## 3. Study area: the İzmir functional urban region

- Coastal Mediterranean metropolis (functional urban region, ~11 districts); documented multi-hazard
  exposure — extreme heat, pluvial flooding, coastal/sea-level processes, and seismic context (the 2020
  Aegean earthquake motivates evacuation/assembly-area relevance) (Cangüzel & Coşkun Hepcan, 2024).
  `[add municipal climate-action context]`
- Justify the 250 m analysis grid and the seven a-priori fabric strata as a representative cross-section
  of the region's form. `[map: FIGURE 1 — grid, strata + sampled cells]`
- `[TO FILL: brief physical/climatic profile with sources; CRS = EPSG:32635]`

---

## 4. Data and materials

`[TABLE 1 — input data inventory]` columns: layer · source · date/version · resolution/scale · licence ·
use in workflow.

| Layer | Source | Notes |
|---|---|---|
| Street network, building footprints | OpenStreetMap; municipal open data where available | provenance + extraction date `[TO FILL]` |
| Imperviousness, land cover | Copernicus / ESA WorldCover | product + year `[TO FILL]` |
| Land-surface temperature (heat outcome) | Landsat 8/9 Collection 2 L2 ST; ECOSTRESS; summer scenes | measured dependent variable for the SHAP explain stage `[TO FILL: dates/scenes]` |
| Green–blue infrastructure, coastline, assembly areas, essential services | open institutional datasets | `[TO FILL]` |
| Social vulnerability inputs | TÜİK / ADNKS (age structure, dependency ratio, accessible socioeconomic indicators) | aggregation unit + year `[TO FILL]` |
| Analysis grid | 250 m fishnet (INSPIRE/GHSL-aligned), EPSG:32635; 500 m for stability test | reproducible unit; matches Landsat LST resolution |
| Software | QGIS `[freeze version]`; PlanX Urban Resilience v1.25.0; PlanX GeoStats Lab v0.9.17; PlanX main v2.5.0; OSMnx; momepy; GeoPandas; NetworkX; SHAP/XGBoost | freeze versions for reproducibility |

Measurement-honesty statements: impervious exposure from satellite land cover (not building-density
proxy); footprint intensity reported explicitly where floor counts are unavailable.

---

## 5. Methods

`[FIGURE 2 — full workflow diagram]`

### 5.1 Grid construction, exclusion and stratified sampling
Build a 250 m analysis grid (INSPIRE/GHSL-aligned, EPSG:32635) over the İzmir functional urban region.
Exclude non-urban, industrial, port, airport and steep-slope (>15%) cells. Assign remaining cells to
seven a-priori fabric strata (historic core, grid residential, apartment-block, waterfront
transformation, hillside/incremental, industrial-logistics, peripheral expansion), then draw a
stratified, spatially balanced sample per stratum (target N per stratum; minimum-distance inhibition).
Strata are defined from planning documents, land use, historical morphology and remote sensing *before*
clustering; clustering tests/refines the classification, avoiding circularity. `[state exclusion
thresholds + per-stratum N]`

### 5.2 The grid cell and the cross-attribution rule (core contribution)
The analytical unit is the sampled 250 m grid cell. Building footprints → morphological tessellation
cells (Fleischmann et al., 2020); road-centre lines cleaned and planarised → segment graph. Cross-
attribution: tessellation-cell morphometrics and network metrics → grid cell via area-weighted median,
IQR and density; 400 m and 800 m pedestrian reaches around each cell carry accessibility and movement
potential. Observation = grid cell. `[formalise the attribution operators; pseudocode/Algorithm 1]`

### 5.3 Morphometric and network indicators
- Network (OSMnx/NetworkX + QGIS): connectivity, node density, meshedness, orientation entropy,
  circuity; angular integration/choice after Space-Syntax-compatible segment-map conversion.
- Morphometric (momepy/GeoPandas): ground coverage, openness, compactness, frontage continuity, block
  permeability, cell heterogeneity, open-space fragmentation. `[TABLE 2 — indicator · formula/definition
  · library function · direction (+/–)]` — name the tool for each (answers reproducibility critique).

### 5.4 Climate-resilience proxies and hazards
Hazards: extreme heat, pluvial flooding, coastal exposure. Proxies: shade/solar-exposure potential,
green–blue cooling access (rationale: Wei et al., 2025), assembly-area and daily-service access,
impervious-exposure × social-vulnerability overlap (rationale: Turner et al., 2025; Neumann et al.,
2026). `[map each proxy to its hazard — hazard-appropriateness table]`

### 5.4b Explainable heat model — the "explain" stage (SHAP)
At fine (pixel/tessellation) scale, pooled across all sampled cells (large N), train a gradient-boosting
model (XGBoost / LightGBM / CatBoost) to predict measured land-surface temperature from morphometric and configurational
drivers; report cross-validated R²/RMSE with spatial-block cross-validation. Use **SHAP** for global
importance, dependence/interaction plots and per-fabric local attribution, yielding the *dominant heat
mechanism* of each fabric. Add a geographically weighted regression (GWR/MGWR) check for spatial
non-stationarity and a ridge/elastic-net baseline (indicators are collinear, p≈30). Template: Wang et
al. (2025); Liu et al. (2026); Li et al. (2026). `[Algorithm 2; FIGURE — SHAP summary + per-fabric
attribution]`

### 5.5 Synthesis: standardisation, dimensionality reduction, clustering
Direction-code + z-standardise; PCA for collinearity; Ward hierarchical clustering → fabric–resilience
profiles; cluster number by silhouette + dendrogram consistency. `[report variance retained, linkage
diagnostics]`

### 5.6 Scale (grid-resolution) stability
Compare 250 m vs 500 m grid classifications with Adjusted Rand Index + rank correlation; optionally vary
the 400/800 m accessibility reach. `[report ARI; which indicators are scale-sensitive]`

### 5.6b Spatial statistics (GeoStats Lab)
Run in PlanX GeoStats Lab: global Moran's I and LISA on fabric clusters, model residuals and priority
scores; Getis-Ord Gi* hot spots of adaptation priority; a **spatial Gini** of impervious-exposure ×
social-vulnerability (equity axis); MGWR as the spatial non-stationarity check; and Monte-Carlo
attribute-randomisation sensitivity. `[report Moran's I, Gi* clusters, spatial Gini]`

### 5.7 Adaptation prioritisation — the "optimize" stage (Pareto + TOPSIS + robustness)
Frame priority as multi-objective across hazard axes (heat, pluvial, coastal, access deficit, social
vulnerability): compute the **Pareto-optimal frontier** to separate dominated fabrics (unambiguous
intervention candidates) from non-dominated trade-off fabrics. Provide a TOPSIS ranking for decision use;
report robustness under equal-weight, entropy-weight and **Monte-Carlo weight perturbation**
(rank-stability distributions, Kendall's τ). Method pedigree: Zhang et al. (2024); Zhu et al. (2025).
`[FIGURE — 2D/3D Pareto front; rank-robustness plot]`

### 5.8 Validation, limitations controls, reproducibility
Tessellation-as-plot-proxy caveat + one cadastral/plan sub-area sensitivity check; screening-model
framing (not hydrodynamic/microsimulation); parameter logs, exported layers, QGIS project released.
**Related work / shared open data:** this study and a parallel İzmir project (pedestrian thermal-friction
/ PFI; SAM3 + GNNWR) share public open data (OpenStreetMap, Copernicus/ESA, Landsat/ECOSTRESS LST, TÜİK)
but differ in unit (250 m grid vs GSV nodes/H3 hex), dependent variable, method and question; disclose
the shared data and cite the sibling study, reuse no text, and report no overlapping findings.
`[reproducibility checklist]`

---

## 6. Results `[scaffold — pilot]`

- 6.1 Fabric–resilience typology: `[FIGURE 3 dendrogram; FIGURE 4 profile maps; TABLE 3 cluster means]`.
- 6.2 Indicator profiles per type: `[radar/heatmap; which mechanisms separate which fabrics]`.
- 6.2b Heat mechanism (SHAP explain stage): `[model skill R²/RMSE; SHAP global importance + per-fabric
  dominant heat driver; GWR non-stationarity]`.
- 6.3 Scale stability: `[ARI value; agreement matrix]`.
- 6.4 Adaptation priorities (optimize stage): `[Pareto frontier of fabrics — dominated vs trade-off;
  TOPSIS ranking; FIGURE 5 priority map; Monte-Carlo rank-robustness]`.
- 6.5 Dominant-mechanism attribution: `[per-profile dominant driver: network redundancy / block
  permeability / shade / open-space continuity / service access / socially differentiated exposure]`.
- 6.6 Cadastral sensitivity sub-area: `[proxy-validity result]`.

> Keep the abstract's promise honest: report the pilot subset actually computed; mark anything not yet
> run as future work rather than implying completion.

---

## 7. Discussion

- 7.1 **Mechanisms over labels:** what the three-register view buys analytically; which mechanism drives
  which fabric's risk, read against Wang, Zhou & Yu (2025) and Iqbal et al. (2025).
- 7.2 **Positioning:** the increment over descriptive typologies (Araldi & Fusco, 2024; Debray et al.,
  2025), over grid/LCZ-scale SHAP-LST studies (Wang et al., 2025; Li et al., 2026), and over coarse
  vulnerability indices (Turner et al., 2025); plus the first Pareto framing of fabric-level adaptation
  priority.
- 7.3 **Planning/policy translation:** how priorities inform NbS siting (Wei et al., 2025), accessibility
  and assembly-area provision, and equitable adaptation (Neumann et al., 2026); İzmir governance hook.
- 7.4 **Limitations:** footprint-only proxy, screening (non-hydrodynamic) hazard treatment, OSM
  completeness, vulnerability data granularity, N = 42 pilot.
- 7.5 **Transferability:** open data + logged parameters → other coastal metropolises.

---

## 8. Conclusion
Restate the gap, the integration unit, and the explainable-priority output; one sentence on transfer.

## Reproducibility statement
Frozen software versions; data sources + dates; parameter tables; released QGIS project, layers, logs,
and code. Open repository link `[TO FILL]`.

## CRediT author contributions / Funding / Acknowledgements / Conflicts
`[TO FILL]` — for journal version only (the ICUS abstract body stays blind).

---

## References (manuscript core — verified unless flagged `[verify]`)

- Araldi, A., & Fusco, G. (2024). Multi-Level Street-Based Analysis of the Urban Fabric: Developments for a Nationwide Taxonomy. *Geographical Analysis, 57*(2), 270–301. https://doi.org/10.1111/gean.12416
- Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems, 65*, 126–139. https://doi.org/10.1016/j.compenvurbsys.2017.05.004
- Boeing, G. (2025). Modeling and Analyzing Urban Networks and Amenities With OSMnx. *Geographical Analysis, 57*(4), 567–577. https://doi.org/10.1111/gean.70009
- Cangüzel, A., & Coşkun Hepcan, Ç. (2024). Climate change vulnerability assessment of Karşıyaka, İzmir. *Natural Hazards, 120*, 14869–14888. https://doi.org/10.1007/s11069-024-06798-5
- Cutter, S. L., Boruff, B. J., & Shirley, W. L. (2003). Social vulnerability to environmental hazards. *Social Science Quarterly, 84*(2), 242–261. `[verify]`
- Debray, H., Gassilloud, M., Lemoine-Rodríguez, R., Wurm, M., Zhu, X., & Taubenböck, H. (2025). Universal patterns of intra-urban morphology: Defining a global typology of the urban fabric using unsupervised clustering. *International Journal of Applied Earth Observation and Geoinformation, 141*, 104610. https://doi.org/10.1016/j.jag.2025.104610
- Fang, Z., Jin, Y., Zheng, S., Zhao, L., & Yang, T. (2024). UrbanClassifier: A deep learning-based model for automated typology and temporal analysis of urban fabric across multiple spatial scales and viewpoints. *Computers, Environment and Urban Systems, 111*, 102132. https://doi.org/10.1016/j.compenvurbsys.2024.102132
- Fleischmann, M. (2019). momepy: Urban Morphology Measuring Toolkit. *Journal of Open Source Software, 4*(43), 1807. https://doi.org/10.21105/joss.01807
- Fleischmann, M., Feliciotti, A., Romice, O., & Porta, S. (2020). Morphological tessellation as a way of partitioning space: Improving consistency in urban morphology at the plot scale. *Computers, Environment and Urban Systems, 80*, 101441. https://doi.org/10.1016/j.compenvurbsys.2019.101441
- Fleischmann, M., Feliciotti, A., Romice, O., & Porta, S. (2022). Methodological foundation of a numerical taxonomy of urban form. *Environment and Planning B: Urban Analytics and City Science, 49*(4), 1283–1299. https://doi.org/10.1177/23998083211059835
- Hillier, B., & Hanson, J. (1984). *The Social Logic of Space.* Cambridge University Press. `[verify]`
- Hwang, C.-L., & Yoon, K. (1981). *Multiple Attribute Decision Making: Methods and Applications.* Springer. `[verify]`
- Imroz, M., Akhtar, M. P., Sharma, M. K., & Alshehri, F. (2025). Integrated assessment of urban flooding and heat island interactions: A systematic review of geospatial technologies, machine learning approaches, and microclimate dynamics. *Journal of Environmental Management, 395*, 127984. https://doi.org/10.1016/j.jenvman.2025.127984
- Iqbal, N., Ravan, M., Mitraka, Z., Birkmann, J., Grimmond, S., Hertwig, D., Chrysoulakis, N., Somarakis, G., Wendnagel-Beck, A., & Panagiotakis, E. (2025). How does perceived heat stress differ between urban forms and human vulnerability profiles? Case study Berlin. *Natural Hazards and Earth System Sciences, 25*, 2481–2502. https://doi.org/10.5194/nhess-25-2481-2025
- Li, H., Yang, J., Xin, J., Yu, W., Ren, J., Yu, H., Xiao, X., & Xia, J. (2026). Investigating the effect of urban form on land surface temperature at block and grid scales based on XGBoost-SHAP. *Environmental Modelling & Software, 195*, 106738. https://doi.org/10.1016/j.envsoft.2025.106738
- Liu, X., Wang, S., & Tang, G. (2026). Understanding nonlinear and spatially heterogeneous effects of urban residential morphology on land surface temperature: Integrating SOM, XGBoost-SHAP, and GWR models. *Sustainable Cities and Society, 136*, 107100. https://doi.org/10.1016/j.scs.2025.107100
- Neumann, S., Berta, J. M. L., Elliot, T., & Bodum, L. (2026). Towards urban climate justice: Integrating social vulnerability in climate adaptation planning. *Environmental Development, 57*, 101365. https://doi.org/10.1016/j.envdev.2025.101365
- Stewart, I. D., & Oke, T. R. (2012). Local Climate Zones for urban temperature studies. *Bulletin of the American Meteorological Society, 93*(12), 1879–1900. `[verify]`
- Turner, R., Higgs, C., Sun, C., … Boeing, G., … Lowe, M. (2025). Development and validation of the Global Urban Heat Vulnerability Index (GUHVI). *Urban Climate, 64*, 102716. https://doi.org/10.1016/j.uclim.2025.102716
- Vartholomaios, A. (2025). Detection and clustering of urban form types with machine learning: insights into Thessaloniki's urban planning and evolution. *Computational Urban Science, 5*(1). https://doi.org/10.1007/s43762-025-00206-9
- Wang, H., Tsoi, K. H., & Loo, B. P. Y. (2025). An assessment framework for 15-minute Cities: Progress worldwide and the impact of urban form. *Transportation Research Part A: Policy and Practice, 199*, 104583. https://doi.org/10.1016/j.tra.2025.104583
- Wang, J., Huang, W., & Biljecki, F. (2024). Learning visual features from figure-ground maps for urban morphology discovery. *Computers, Environment and Urban Systems, 109*, 102076. https://doi.org/10.1016/j.compenvurbsys.2024.102076
- Wang, Z., Zhou, R., & Yu, Y. (2025). The impact of urban morphology on land surface temperature under seasonal and diurnal variations: Marginal and interaction effects. *Building and Environment, 272*, 112673. https://doi.org/10.1016/j.buildenv.2025.112673
- Wang, Z., Zhou, R., Rui, J., & Yu, Y. (2025). Revealing the impact of urban spatial morphology on land surface temperature in plain and plateau cities using explainable machine learning. *Sustainable Cities and Society, 118*, 106046. https://doi.org/10.1016/j.scs.2024.106046
- Wei, H., Bai, X., Lu, Q., Wu, J., Su, F., Hong, T., Hu, Q., Wang, W., Quan, S. J., Luo, Z., & Han, Y. (2025). Urban cooling and energy-saving effects of nature-based solutions across types and scales. *Nature Cities, 2*(12), 1194–1204. https://doi.org/10.1038/s44284-025-00349-0
- Zhang, Y., Teoh, B. K., & Zhang, L. (2024). Multi-objective optimization for energy-efficient building design considering urban heat island effects. *Applied Energy, 376*, 124117. https://doi.org/10.1016/j.apenergy.2024.124117
- Zhu, Y., Shen, X., Rui, S., Sun, X., Wang, J., Zhang, L., & Guan, Y. (2025). Utilizing multi-objective optimization in improved green infrastructure for enhanced pollution reduction and carbon mitigation in sponge cities. *Resources, Conservation and Recycling, 217*, 108179. https://doi.org/10.1016/j.resconrec.2025.108179
