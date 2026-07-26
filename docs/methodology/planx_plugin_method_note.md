# PlanX Urban Resilience Method Note

## Recommendation

Use `planx_urban_resilience` as the central analytical environment, but not as the only evidence layer. The academically strongest position is **PlanX-first, validation-backed**:

- PlanX provides the reproducible QGIS workflow.
- Open data and transparent parameters provide auditability.
- Independent checks and sensitivity tests keep the study from looking like a plugin advertisement.

Local plugin metadata currently reports version `1.25.0` and 43 Processing algorithms. Freeze the exact release before analysis starts and cite that frozen version in the method section.

## Why This Is a Good ICUS 2026 Fit

The plugin already covers the congress language: climate risk, social vulnerability, emergency accessibility, multi-hazard synthesis, recovery capacity, spatial statistics, scenarios, and reporting. It also supports the open-source argument because it runs inside QGIS and exposes tool parameters, logs, layers, and styles.

## Candidate Module Chain

| Step | PlanX module family | Possible output |
|---|---|---|
| 1 | Heat | 0-100 heat risk / comfort stress grid or unit score |
| 2 | Flood | pluvial susceptibility and exposed roads/buildings |
| 3 | Social | social vulnerability score by neighborhood/planning unit |
| 4 | Emergency / Network | access deficit, travel distance/time to shelters or services |
| 5 | Recovery | recovery capacity index |
| 6 | Join / Multi-hazard | joined risk fields and composite score |
| 7 | Equity-adjusted priority | intervention priority weighted by vulnerability |
| 8 | Hot-Spot / LISA | statistically interpretable clusters and outliers |
| 9 | Reporting / Symbology | reproducible QGIS atlas, HTML/Markdown brief, QML styles |

## Suggested Abstract-Level Claim

The study demonstrates how an open-source QGIS workflow can convert heterogeneous climate-risk and socio-spatial inputs into transparent adaptation-priority surfaces for local planning. PlanX Urban Resilience is used as the operational workflow engine, while outputs are checked through parameter documentation, sensitivity analysis, and selected spatial-statistical diagnostics.

## Validation Plan

For the abstract phase:

- report plugin version and QGIS version,
- state that outputs are screening indicators, not deterministic risk predictions,
- use a limited but coherent set of modules,
- include sensitivity testing as planned or initial validation.

For the full paper phase:

- compare selected PlanX outputs against independent descriptive layers,
- run weight sensitivity for composite and priority scores,
- report missing-data flags and data limitations,
- preserve Processing logs,
- export QGIS project and final layers,
- include a parameter table and reproducibility appendix.

## Caution

Avoid overclaiming. The plugin is a planning-support screening suite, not a hydrodynamic, microsimulation, or fully causal urban climate model. That limitation can be a strength if stated clearly: the contribution is fast, open, auditable prioritization for early-stage climate adaptation planning.
