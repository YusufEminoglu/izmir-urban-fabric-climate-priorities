# ICUS 2026 — Literature Positioning Dossier (2024–June 2026 Q1 base)

**Purpose.** The CMT abstract body must stay blind and reference-free, so this companion document
carries the literature grounding the abstract implies. It (1) states the Q1-level gap in current
terms, (2) positions the study against the 2024–2026 state of the art, (3) maps each load-bearing
abstract claim to supporting work, and (4) provides an annotated, DOI-checked bibliography that
seeds the journal manuscript.

**Provenance / honesty note.** Every entry in §5.1 and §5.2 was verified against the Crossref API
(title, authors, journal, year, volume, DOI). The classic anchors in §5.3 are given from disciplinary
knowledge and are flagged **[verify]** — confirm them in the journal/DOI before they enter a
submitted reference list. Quartiles are indicative (Scopus/JCR categories shift year to year);
confirm the current quartile for the author's target list.

---

## 1. Why the current abstract sat below Q1, and what the literature lets us fix

The pre-revision abstract was methodologically literate but **disconnected from the live debate** in
its own field. It described a workflow; it did not argue a position against what the 2024–2026
literature already does. Four moves close that gap, each anchored in recent Q1 work:

1. **Name the real tension.** Urban morphometrics has, in the last two years, become a *scalable,
   unsupervised, reproducible* typology science: nationwide street-based taxonomies (Araldi & Fusco,
   2024, *Geographical Analysis*), global urban-fabric typologies from unsupervised clustering
   (Debray et al., 2025, *Int. J. Applied Earth Obs. Geoinf.*), interpretable multi-scale clustering
   pipelines (Vartholomaios, 2025, *Computational Urban Science*), and deep-learning fabric
   classifiers (Fang et al., 2024; Wang, Huang & Biljecki, 2024, both *CEUS*). In parallel, the
   climate-urban literature shows form is a **first-order control** on heat and hazard: morphology
   drives land-surface temperature through marginal and interaction effects (Wang, Zhou & Yu, 2025,
   *Building and Environment*), heat vulnerability is unevenly distributed by form and demography
   (Turner et al., 2025, *Urban Climate*; Iqbal et al., 2025, *NHESS*), and flooding and heat
   co-produce risk (Imroz et al., 2025, *J. Environmental Management*). **These two literatures rarely
   meet at the street/walkable-neighbourhood scale where adaptation is designed.** That is the gap.

2. **Motivate the hook empirically.** The abstract's claim that *equally dense areas differ in heat,
   access and vulnerability* is no longer rhetorical: Wang, Zhou & Yu (2025) show density alone
   underdetermines LST once configuration and interactions are modelled, and Iqbal et al. (2025) show
   heat exposure and human vulnerability decouple across urban forms in Berlin (inner-city heat vs.
   outer-zone elderly concentration). The hook now cites a mechanism, not an intuition.

3. **Argue the contribution against prior art.** Recent morphometric typologies are predominantly
   *descriptive* (form in, types out); resilience indices are predominantly *administrative/coarse*
   (GUHVI at neighbourhood scale, LCZ tiles). The increment here is the **catchment-radius
   cross-attribution rule** that renders movement potential, built-form intensity and hazard exposure
   commensurable in one unit, plus hazard-specific MCDA (TOPSIS) that converts a descriptive typology
   into *auditable adaptation priorities*. That is a framework-integration contribution, positioned
   precisely where the 2024–2026 work stops.

4. **Add a headline method unit ("explain → optimize").** Two moves lift the synthesis from
   conventional (z-score → PCA → Ward → TOPSIS) to distinctive. *Explain:* an explainable
   gradient-boosting model attributes a **measured** outcome — satellite land-surface temperature — to
   morphometric drivers, with **SHAP** naming the dominant mechanism per fabric. XGBoost/GBRT/CatBoost +
   SHAP has become the standard way to read morphology→LST (Wang, Zhou & Yu, 2025; Wang et al., 2025;
   Liu et al., 2026; Li et al., 2026); our increment is street/cell scale, pooled across the 42 samples,
   with SHAP mechanisms feeding the typology and the priority. *Optimize:* adaptation priority is
   reframed as a **multi-objective (Pareto)** problem — a trade-off frontier separating dominated fabrics
   (clear intervention candidates) from frontier fabrics — with TOPSIS ranking and entropy/Monte-Carlo
   weight robustness (method pedigree: Zhang et al., 2024; Zhu et al., 2025). No existing fabric-typology
   study frames fabric-level adaptation priority as a Pareto problem; that transfer is the novelty.

---

## 2. State of the art vs. this study's increment

| Recent Q1 strand (2024–2026) | Representative work | What it establishes | What it does **not** do | This study's increment |
|---|---|---|---|---|
| Scalable unsupervised fabric typology | Araldi & Fusco 2024; Debray et al. 2025; Vartholomaios 2025 | Form can be classified reproducibly at national/global scale | Stays descriptive; no climate-hazard coupling; coarse or plot-only units | Couples typology to multi-hazard exposure + vulnerability at street scale |
| Deep-learning fabric classification | Fang et al. 2024 (UrbanClassifier); Wang, Huang & Biljecki 2024 | High-accuracy, multi-scale fabric recognition | Black-box; not auditable; not tied to adaptation decisions | Glass-box, parameter-logged, decision-linked (explainable profiles) |
| Morphology → heat | Wang, Zhou & Yu 2025; (LCZ literature) | Form controls LST via marginal/interaction effects | Grid/LCZ scale; single hazard; no accessibility or equity | Street scale; multi-hazard; integrates shade, cooling access, equity |
| Heat vulnerability indices | Turner et al. 2025 (GUHVI); Iqbal et al. 2025 | Open, transferable neighbourhood heat-vulnerability mapping | Vulnerability ≠ morphometrics; not fabric-mechanistic | Binds vulnerability to morphological mechanism in same unit |
| Flood–heat interaction | Imroz et al. 2025 | Compound hazard framing is needed | Review-level; no operational street-scale unit | Operational unit handling heat + pluvial + coastal together |
| Accessibility / 15-min city | Wang, Tsoi & Loo 2025 | Urban form shapes proximity/walkability outcomes | Accessibility treated apart from hazard/vulnerability | Accessibility is one axis of a hazard-coupled priority |
| Reproducible open tooling | Boeing 2025 (OSMnx); Fleischmann 2019/2020/2022 (momepy) | Mature open libraries for networks and morphometrics | Libraries are components, not an integrated resilience workflow | Integration layer + auditable QGIS pipeline over these libraries |
| İzmir Gulf climate risk | Cangüzel & Coşkun Hepcan 2024 (Karşıyaka) | İzmir Gulf is demonstrably climate-exposed and policy-relevant | Administrative-unit vulnerability; not street-scale morphometric | Provides the street-scale morphometric layer that case lacks |
| Explainable ML for form→heat (SHAP) | Wang, Zhou & Yu 2025; Wang et al. 2025; Liu et al. 2026; Li et al. 2026 | XGBoost/GBRT/CatBoost + SHAP attribute LST to morphology and name mechanisms | Grid/block/LCZ scale; not linked to a typology or a decision step | Runs at street/cell scale; SHAP mechanisms feed the typology and the priority |
| Multi-objective / Pareto optimisation | Zhang et al. 2024; Zhu et al. 2025 | Pareto fronts expose adaptation trade-offs and support decisions | Applied to GI / building design, not to fabric-level priority | Frames fabric-level adaptation priority as a Pareto problem (+ TOPSIS, weight uncertainty) |

**One-line positioning (for the introduction):** *We take the reproducible morphometric typology that
the field has just industrialised (Araldi & Fusco 2024; Debray et al. 2025) and the form–hazard
evidence it rarely connects to (Wang et al. 2025; Turner et al. 2025), and bind them in a single
street-scale unit that yields auditable, hazard-specific adaptation priorities for the İzmir Gulf.*

---

## 3. Claim-by-claim citation map

Use this when expanding the abstract into the manuscript, or if a reviewer asks for grounding.

| # | Abstract claim | Supporting literature |
|---|---|---|
| 1 | Morphometrics is now reproducible/unsupervised at national–global scale | Fleischmann et al. 2022; Araldi & Fusco 2024; Debray et al. 2025; Vartholomaios 2025 |
| 2 | Urban form is a first-order control on LST/heat | Wang, Zhou & Yu 2025; Iqbal et al. 2025 |
| 3 | Heat exposure and social vulnerability are spatially uneven and decoupled | Turner et al. 2025; Iqbal et al. 2025; Neumann et al. 2026 |
| 4 | Heat and pluvial flooding co-produce compound urban risk | Imroz et al. 2025 |
| 5 | Resilience is still assessed at administrative/coarse/LCZ scale (the gap) | Turner et al. 2025; Neumann et al. 2026; Cangüzel & Coşkun Hepcan 2024 |
| 6 | "Equally dense areas differ in heat/access/vulnerability" | Wang, Zhou & Yu 2025; Iqbal et al. 2025 |
| 7 | Street networks/accessibility shape adaptation-relevant outcomes | Boeing 2025; Wang, Tsoi & Loo 2025 |
| 8 | Morphological tessellation is a defensible plot proxy | Fleischmann et al. 2020; Fleischmann 2019 |
| 9 | Reproducible/open tooling for networks + morphometrics exists and is citable | Boeing 2017, 2025; Fleischmann 2019 |
| 10 | Green–blue infrastructure delivers measurable cooling (resilience proxy rationale) | Wei et al. 2025 |
| 11 | İzmir Gulf is a climate-exposed, policy-relevant case | Cangüzel & Coşkun Hepcan 2024 |
| 12 | Unsupervised clustering + dimensionality reduction is standard for fabric typology | Debray et al. 2025; Vartholomaios 2025; Fleischmann et al. 2022 |
| 13 | Climate justice requires integrating social vulnerability into adaptation | Neumann et al. 2026; Turner et al. 2025 |
| 14 | Explainable ML (SHAP) attributes measured LST to morphological mechanisms | Wang, Zhou & Yu 2025; Wang et al. 2025; Liu et al. 2026; Li et al. 2026 |
| 15 | Multi-objective / Pareto framing exposes adaptation trade-offs; ranking robust under weight uncertainty | Zhang et al. 2024; Zhu et al. 2025 |

---

## 4. Target journals (balanced method + resilience framing)

| Tier | Journal | Why it fits | Quartile (confirm) |
|---|---|---|---|
| Primary | *Sustainable Cities and Society* | Resilience + method + decision support; high visibility | Q1 |
| Primary | *Computers, Environment and Urban Systems* | Home of reproducible urban morphometrics/analytics | Q1 |
| Primary | *Landscape and Urban Planning* | Form–environment coupling with planning translation | Q1 |
| Alt | *Urban Climate* | If heat/hazard is foregrounded over method | Q1 |
| Alt | *Environment and Planning B: Urban Analytics and City Science* | If the integration unit/typology is foregrounded | Q1 |
| Alt | *Cities* | Policy-facing version with İzmir governance angle | Q1 |

---

## 5. Annotated bibliography

### 5.1 Verified 2024–2026 anchors (Crossref-checked)

1. **Araldi, A., & Fusco, G. (2024).** Multi-Level Street-Based Analysis of the Urban Fabric:
   Developments for a Nationwide Taxonomy. *Geographical Analysis, 57*(2), 270–301.
   doi:10.1111/gean.12416. — *Closest prior art on street-based fabric taxonomy; cite as the method
   our street unit extends toward hazard coupling.* [Q1]
2. **Debray, H., Gassilloud, M., Lemoine-Rodríguez, R., Wurm, M., Zhu, X., & Taubenböck, H. (2025).**
   Universal patterns of intra-urban morphology: Defining a global typology of the urban fabric using
   unsupervised clustering. *International Journal of Applied Earth Observation and Geoinformation,
   141*, 104610. doi:10.1016/j.jag.2025.104610. — *Shows unsupervised fabric typology is now global;
   our increment is climate coupling at street scale.* [Q1]
3. **Vartholomaios, A. (2025).** Detection and clustering of urban form types with machine learning:
   insights into Thessaloniki's urban planning and evolution. *Computational Urban Science, 5*(1).
   doi:10.1007/s43762-025-00206-9. — *Interpretable 17-indicator UMAP+BIRCH typology; direct methodo-
   logical sibling for our PCA+Ward choice rationale.* [Q1/Q2 — confirm]
4. **Fang, Z., Jin, Y., Zheng, S., Zhao, L., & Yang, T. (2024).** UrbanClassifier: A deep learning-
   based model for automated typology and temporal analysis of urban fabric across multiple spatial
   scales and viewpoints. *Computers, Environment and Urban Systems, 111*, 102132.
   doi:10.1016/j.compenvurbsys.2024.102132. — *DL fabric typology; contrast with our explainable,
   auditable approach.* [Q1]
5. **Wang, J., Huang, W., & Biljecki, F. (2024).** Learning visual features from figure-ground maps
   for urban morphology discovery. *Computers, Environment and Urban Systems, 109*, 102076.
   doi:10.1016/j.compenvurbsys.2024.102076. — *Unsupervised visual morphology discovery; situates our
   indicator-based, interpretable alternative.* [Q1]
6. **Wang, Z., Zhou, R., & Yu, Y. (2025).** The impact of urban morphology on land surface temperature
   under seasonal and diurnal variations: Marginal and interaction effects. *Building and Environment,
   272*, 112673. doi:10.1016/j.buildenv.2025.112673. — *Core evidence that form (not density alone)
   drives heat via interactions; anchors the "same density, different heat" hook.* [Q1]
7. **Turner, R., Higgs, C., Sun, C., … Boeing, G., … Lowe, M. (2025).** Development and validation of
   the Global Urban Heat Vulnerability Index (GUHVI). *Urban Climate, 64*, 102716.
   doi:10.1016/j.uclim.2025.102716. — *Open, transferable exposure–sensitivity–adaptive-capacity heat
   vulnerability; our work binds such vulnerability to morphological mechanism.* [Q1]
8. **Iqbal, N., Ravan, M., Mitraka, Z., Birkmann, J., Grimmond, S., Hertwig, D., Chrysoulakis, N.,
   Somarakis, G., Wendnagel-Beck, A., & Panagiotakis, E. (2025).** How does perceived heat stress
   differ between urban forms and human vulnerability profiles? Case study Berlin. *Natural Hazards
   and Earth System Sciences, 25*, 2481–2502. doi:10.5194/nhess-25-2481-2025. — *Directly supports the
   decoupling of heat exposure and demographic vulnerability across urban forms.* [Q1/Q2 — confirm]
9. **Imroz, M., Akhtar, M. P., Sharma, M. K., & Alshehri, F. (2025).** Integrated assessment of urban
   flooding and heat island interactions: A systematic review of geospatial technologies, machine
   learning approaches, and microclimate dynamics. *Journal of Environmental Management, 395*, 127984.
   doi:10.1016/j.jenvman.2025.127984. — *Justifies treating heat + pluvial as compound, not separate.*
   [Q1]
10. **Neumann, S., Berta, J. M. L., Elliot, T., & Bodum, L. (2026).** Towards urban climate justice:
    Integrating social vulnerability in climate adaptation planning. *Environmental Development, 57*,
    101365. doi:10.1016/j.envdev.2025.101365. — *Equity rationale for the impervious-exposure ×
    vulnerability overlap layer.* [Q1/Q2 — confirm]
11. **Wang, H., Tsoi, K. H., & Loo, B. P. Y. (2025).** An assessment framework for 15-minute Cities:
    Progress worldwide and the impact of urban form. *Transportation Research Part A: Policy and
    Practice, 199*, 104583. doi:10.1016/j.tra.2025.104583. — *Form → proximity/accessibility evidence
    for the accessibility axis.* [Q1]
12. **Wei, H., Bai, X., Lu, Q., … Han, Y. (2025).** Urban cooling and energy-saving effects of nature-
    based solutions across types and scales. *Nature Cities, 2*(12), 1194–1204.
    doi:10.1038/s44284-025-00349-0. — *Quantifies green–blue cooling, grounding the cooling-access
    proxy.* [Nature-family; no JCR quartile yet]
13. **Boeing, G. (2025).** Modeling and Analyzing Urban Networks and Amenities With OSMnx.
    *Geographical Analysis, 57*(4), 567–577. doi:10.1111/gean.70009. — *Current OSMnx (v2) citation for
    the network + amenity-access components.* [Q1]
14. **Cangüzel, A., & Coşkun Hepcan, Ç. (2024).** Climate change vulnerability assessment of Karşıyaka,
    İzmir. *Natural Hazards, 120*, 14869–14888. doi:10.1007/s11069-024-06798-5. — *İzmir Gulf-specific,
    recent; the administrative-scale assessment our street-scale layer complements.* [Q1/Q2 — confirm]

### 5.1b Method-unit anchors — "explain → optimize" (Crossref-checked, 2024–2026)

M1. **Wang, Z., Zhou, R., Rui, J., & Yu, Y. (2025).** Revealing the impact of urban spatial morphology
    on land surface temperature in plain and plateau cities using explainable machine learning.
    *Sustainable Cities and Society, 118*, 106046. doi:10.1016/j.scs.2024.106046. — *GBRT + SHAP for
    morphology→LST; core "explain"-stage precedent (same lead author as the Building and Environment
    anchor).* [Q1]
M2. **Liu, X., Wang, S., & Tang, G. (2026).** Understanding nonlinear and spatially heterogeneous
    effects of urban residential morphology on land surface temperature: Integrating SOM, XGBoost-SHAP,
    and GWR models. *Sustainable Cities and Society, 136*, 107100. doi:10.1016/j.scs.2025.107100. —
    *Combines clustering + XGBoost-SHAP + GWR; the template for our explain-stage with a
    spatial-non-stationarity check.* [Q1]
M3. **Li, H., Yang, J., Xin, J., Yu, W., Ren, J., Yu, H., Xiao, X., & Xia, J. (2026).** Investigating
    the effect of urban form on land surface temperature at block and grid scales based on XGBoost-SHAP.
    *Environmental Modelling & Software, 195*, 106738. doi:10.1016/j.envsoft.2025.106738. — *Block and
    grid scales = multi-scale, mirroring our 400/800 m scale design.* [Q1]
M4. **Zhang, Y., Teoh, B. K., & Zhang, L. (2024).** Multi-objective optimization for energy-efficient
    building design considering urban heat island effects. *Applied Energy, 376*, 124117.
    doi:10.1016/j.apenergy.2024.124117. — *Pareto/MOO + UHI; method pedigree for the "optimize" stage.*
    [Q1]
M5. **Zhu, Y., Shen, X., Rui, S., Sun, X., Wang, J., Zhang, L., & Guan, Y. (2025).** Utilizing
    multi-objective optimization in improved green infrastructure for enhanced pollution reduction and
    carbon mitigation in sponge cities. *Resources, Conservation and Recycling, 217*, 108179.
    doi:10.1016/j.resconrec.2025.108179. — *Pareto trade-off optimisation for urban climate
    infrastructure; transfer target for fabric-level priority.* [Q1]

*Uncertainty layer (cite by name, **[verify]**):* Robust Decision Making / Decision-Making under Deep
Uncertainty lineage (Lempert and colleagues) — conceptual basis for the Monte-Carlo weight-robustness
check on the TOPSIS ranking.

### 5.2 Verified foundational method backbone (Crossref-checked)

15. **Fleischmann, M. (2019).** momepy: Urban Morphology Measuring Toolkit. *Journal of Open Source
    Software, 4*(43), 1807. doi:10.21105/joss.01807. — *Cite for every momepy character.*
16. **Fleischmann, M., Feliciotti, A., Romice, O., & Porta, S. (2020).** Morphological tessellation as
    a way of partitioning space: Improving consistency in urban morphology at the plot scale.
    *Computers, Environment and Urban Systems, 80*, 101441. doi:10.1016/j.compenvurbsys.2019.101441.
    — *Cite for the tessellation-as-plot-proxy claim.* [Q1]
17. **Fleischmann, M., Feliciotti, A., Romice, O., & Porta, S. (2022).** Methodological foundation of a
    numerical taxonomy of urban form. *Environment and Planning B: Urban Analytics and City Science,
    49*(4), 1283–1299. doi:10.1177/23998083211059835. — *Cite for the unsupervised-typology logic and
    the contextual-character approach.* [Q1]
18. **Boeing, G. (2017).** OSMnx: New methods for acquiring, constructing, analyzing, and visualizing
    complex street networks. *Computers, Environment and Urban Systems, 65*, 126–139.
    doi:10.1016/j.compenvurbsys.2017.05.004. — *Original OSMnx citation.* [Q1]

### 5.3 Classic anchors to cite by name — confirm exact details **[verify]**

These are standard in the field and safe to use, but were not Crossref-checked here; confirm
year/volume/DOI before they enter a submitted reference list.

- **Hillier, B., & Hanson, J. (1984).** *The Social Logic of Space.* Cambridge University Press.
  *(Space Syntax foundation for angular integration/choice.)*
- **Stewart, I. D., & Oke, T. R. (2012).** Local Climate Zones for urban temperature studies.
  *Bulletin of the American Meteorological Society, 93*(12), 1879–1900. *(LCZ baseline the study
  argues past.)*
- **Cutter, S. L., Boruff, B. J., & Shirley, W. L. (2003).** Social vulnerability to environmental
  hazards. *Social Science Quarterly, 84*(2), 242–261. *(SoVI lineage for the vulnerability layer.)*
- **Hwang, C.-L., & Yoon, K. (1981).** *Multiple Attribute Decision Making.* Springer.
  *(TOPSIS origin.)*
- **Berghauser Pont, M., & Haupt, P. (2010).** *Spacematrix: Space, Density and Urban Form.*
  *(GSI/FSI/OSR density logic behind footprint-intensity reporting.)*
- **Conzen, M. R. G. (1960)** and **Caniggia, G., & Maffei, G. L. (1979/2001).** *(Typomorphology
  lineage for the a-priori strata.)*

---

## 6. Verification notes & caveats (read before submitting)

- **Word counts (script-verified):** Turkish 712, English 748 — both inside the 500–750 rule.
- **Spatial design (v3):** the unit is now a **sampled 250 m analysis grid** over the **İzmir
  functional urban region** (square grid, INSPIRE/GHSL-aligned), not street catchments. 250 m matches
  Landsat LST resolution and is reproducible; grid-resolution stability is tested 250 vs 500 m (ARI).
  The catchment–radius rule is retargeted to the grid; 400/800 m become per-cell accessibility reaches.
- **Method unit "explain → optimize":** SHAP-on-measured-LST + Pareto/TOPSIS with weight uncertainty.
  **Data dependency:** the explain stage needs an open land-surface-temperature product (Landsat 8/9 or
  ECOSTRESS summer scenes for İzmir). Modelling runs at fine scale pooled across sampled cells, so N is
  large enough for ML; the GWR/MGWR non-stationarity check lives in the manuscript (and in GeoStats Lab).
- **Blind-review consideration (now stronger):** the body names **two author-developed plugins** —
  "PlanX Urban Resilience" and "GeoStats Lab". Naming two niche own-plugins materially weakens
  double-blind anonymity. Recommended: in the blind CMT body, neutralise to "open-source QGIS
  resilience-screening and spatial-statistics plugins"; name PlanX Urban Resilience and GeoStats Lab
  only in the (non-blind) camera-ready/manuscript. **Author decision needed.**
- **Tense/claim calibration:** the body keeps the honest "testable pilot protocol" stance while making
  the standalone methodological contribution explicit — this answers the internal review's
  overstatement flag without underselling.
- **Quartiles** in §4–§5 are indicative; confirm against the author's institution's current
  Scopus/JCR list. *Nature Cities* (2024 launch) has no JCR quartile yet but is a top venue.
- **AI-ethics rule (congress):** this dossier and the abstract draft are scaffolding. The author must
  read, verify and rewrite to own the final prose, and run the similarity check (<20%) before CMT.
- **Shared open data & sibling-study disclosure (journal track):** this study and a parallel İzmir
  project (pedestrian thermal-friction / PFI; SAM3 + GNNWR) draw on the **same public open data**
  (OpenStreetMap, Copernicus/ESA, Landsat/ECOSTRESS LST, TÜİK). This is legitimate and common, but
  **do not conceal it** — concealment is the real integrity risk (duplicate-publication / salami-
  slicing). The two are genuinely distinct in **unit** (250 m grid vs GSV nodes/H3 hex), **dependent
  variable** (fabric-resilience priority vs PFI), **method** (momepy + Pareto/TOPSIS vs SAM3 + GNNWR)
  and **question**. In the journal manuscript, add one sentence disclosing the shared open-data
  environment and cite the sibling study as related work; reuse no text and report no overlapping
  findings. The blind CMT body names no other project, so nothing is required there.
- **Do not paste this dossier into CMT.** It is the journal-track support layer; the CMT body stays
  reference-free.
