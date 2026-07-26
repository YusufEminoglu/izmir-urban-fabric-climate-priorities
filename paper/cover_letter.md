# Cover letter — Sustainable Cities and Society

Dear Editors,

We submit our original research article, **"Grid-Based Urban Morphometrics for
Climate Resilience: Explainable, Pareto-Aware Fabric–Resilience Priorities for the
İzmir Functional Urban Region,"** for consideration in *Sustainable Cities and
Society*.

**The gap.** Reproducible urban morphometrics can now say *what kind of fabric* a
place is at metropolitan scale, and climate-resilience assessment can say *where
risk is* — but the two rarely meet at the street and neighbourhood scale where
adaptation is actually designed, financed and lived. Resilience is still resolved
over administrative units, coarse grids and Local Climate Zone tiles that cannot see
the form at which heat, accessibility and vulnerability are produced.

**What we do.** We close that gap with an open-source, parameter-logged, auditable
QGIS workflow that binds street-scale morphometrics, multi-hazard exposure and social
vulnerability in one commensurable unit — a 250 m grid cell carrying tessellation-cell
morphometrics, **network-distance service-area** reaches and measured land-surface
temperature — and converts them, through an *explain → optimize* sequence
(explainable gradient boosting + SHAP, then multi-objective Pareto optimisation with
TOPSIS and Monte-Carlo weight robustness), into transparent, fabric-specific
adaptation priorities. The analysis is run as a **full census of all 3,777 urban
cells** of the İzmir functional urban region (not a sample).

**Why it matters for this journal.** Two results speak directly to sustainable,
equitable urban adaptation. First, an **equity inversion**: coupling heat with
access, coastal exposure and social vulnerability ranks the *coolest* fabric — the
waterfront — as the *highest* adaptation priority, exactly the case a heat-only
reading misses. Second, an honest corrective: at metropolitan scale urban form is a
**secondary, though genuine,** control on summer land-surface temperature behind the
coastal gradient (cross-validated R² ≈ 0.09 for morphology alone, ≈ 0.27 with coastal
and topographic context), a caution against importing inland-derived morphology–heat
coefficients into maritime cities. The workflow is fully reproducible and transferable
to other coastal metropolitan regions, with frozen software versions, logged
parameters and released code.

**Integrity disclosures.**
- *Related İzmir study (shared open data).* The land-surface-temperature, boundary,
  neighbourhood and population layers are common open inputs also assembled for a
  parallel İzmir study by the corresponding author (pedestrian thermal friction;
  SAM3 + GNNWR). That study uses a different analytical unit, dependent variable,
  method and research question; the present work shares only public open data and
  reuses no text and reports no overlapping findings. We disclose this proactively
  and are happy to provide the related manuscript to the editor.
- *Software / competing interest.* The analysis uses two open QGIS plugins developed
  by the corresponding author (PlanX: Urban Resilience; PlanX GeoStats Lab); they are
  cited as software and the competing interest is declared.
- *Generative AI.* AI tools assisted code development and language editing; all design,
  analysis and interpretation are the authors', every result is computed by the
  released code from open data, and the authors take full responsibility.

The manuscript is original, not under consideration elsewhere, and all authors approve
the submission. We have no conflicts beyond the software disclosure above.

Thank you for your consideration.

Sincerely,
Yusuf Eminoğlu (corresponding author), on behalf of the authors
Department of City and Regional Planning, Dokuz Eylül University, İzmir, Türkiye
yusuf.eminoglu@deu.edu.tr · ORCID 0009-0005-6000-2934
