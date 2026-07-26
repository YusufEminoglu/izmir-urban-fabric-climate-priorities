# WORKER REPORT — rev2

## 1. Executive summary (max 10 lines: what was done, what was not, why)

The revision is complete against mandatory Tasks 1–7, preserving the existing backup and frozen canonical results.
Six missing equations were added and referenced; the three handoff equations were verified and not duplicated.
The five-axis/pluvial scope contradiction was resolved from pipeline evidence, and the abstract, introduction and limitations now agree.
Hilmi Evren Erdin was added in author position 3, with source TODOs for title and ORCID; the recommended short title was adopted.
All 90 archived em-dashes and 31 letter-to-letter en-dashes were removed from prose; emphasis fell from 59 to 17 instances.
The Sankey was removed, both requested map panels were produced, and supplementary figures now use automatic S-numbering.
RQ1–RQ4 answers, a seven-stratum policy table and a quantitative SHAP contrast were added.
Both PDFs compile without LaTeX/natbib/reference/overfull warnings; citation checks and canonical-number checks pass.
Optional Task 5.5 was not implemented because it was outside the mandatory scope; proposed costs are recorded below.

## 2. Task status table

| Task | Status (DONE/PARTIAL/NOT DONE) | Evidence (file:line / grep output / page no.) |
|---|---|---|
| 1, mandatory equations | DONE | `paper/manuscript/src/sections/methodology.tex:163,222,230,249,262,271`; rendered on PDF pp. 17–20. Existing M1/M2/O1 remain at lines 72, 83 and 106. |
| 2, dash/tell purge | DONE | Section 4 below; final `---` count = 0 in every section, `[A-Za-z]--[A-Za-z]` is empty, `\emph{}` 59→17, targeted tell words 8→0. |
| 3, third author | DONE | `sections/titleAbstract.tex:10`, `title_page.tex:21,35,43`, `sections/declarations.tex:6`; TODO audit returns only four Erdin-field markers. |
| 4, short title | DONE | `sections/titleAbstract.tex:1`; `title_page.tex:14`; main PDF p. 1 and title-page PDF p. 1. |
| 5.1, axis contradiction | DONE | Pipeline: `scripts/pilot_11_priority.py:37`; text: `methodology.tex:241`, `titleAbstract.tex:42`, `introduction.tex:51`, `discussion.tex:128`. |
| 5.2, RQ answers | DONE | `sections/conclusions.tex:15–27`; PDF p. 38. |
| 5.3, policy translation | DONE | `sections/discussion.tex:71–99`, label at line 85; PDF p. 35. |
| 5.4, quantitative SHAP scenario | DONE | `sections/discussion.tex:71–79`; uses frozen `outputs/tables/shap_per_stratum_mechanism.csv` values. |
| 5.5, optional extensions | NOT DONE | No optional threshold/LCZ/PSF paragraph was added. Estimated cost: roughly one paragraph each plus citation verification for LCZ and a careful non-causal uncertainty statement for PSF; omitted to avoid expanding the mandatory revision. |
| 6.1, priority map | DONE | `scripts/pilot_13_cell_pareto.py:256–329`; PNG `outputs/figures/priority_synthesis.png`; caption `results.tex:261`; PDF p. 32. |
| 6.2, remove Sankey | DONE | `rg 'flow-sankey' sections main.tex` is empty; orchestrator has no `make_fig09_flow_sankey.py`; current figure sequence proceeds directly from `results.tex:262` to the TOPSIS figure. |
| 6.3, TOPSIS map | DONE | `scripts/make_fig11_topsis_robustness.py:132–199`; PNG `outputs/figures/topsis_robustness.png`; caption `results.tex:268`; PDF p. 33. |
| 6.4, supplementary repair | DONE | Automatic counters and unique Hyperref anchors at `appendix.tex:2–8`; reduced S7 caption at `appendix.tex:288`; PDF pp. 56, 58, 60–64 show S1–S7 in document order. |
| 7, verification/build | DONE | Section 10 below; both PDFs built, 99/99 citation check, zero forbidden grep/log findings, 64-page visual render inspected. |
| 8, worker report | DONE | This file follows the twelve-section contract. |

## 3. Equations added (number, label, host subsection, in-text reference sentence)

| Eq. | Label | Host subsection | In-text reference sentence/evidence |
|---|---|---|---|
| M3 | `eq:shap` | Explainable heat model | `methodology.tex:161–164`: “the TreeSHAP attribution is … in Equation …”; definition at line 164. |
| M4 | `eq:pareto` | Adaptation prioritisation | `methodology.tex:247–250`: dominance is defined “according to Equation …”; definition at line 250. |
| M5 | `eq:entropy` | Adaptation prioritisation | `methodology.tex:260–263`: entropy weights are calculated “using Equation …”; definition at line 263. |
| M6 | `eq:topsis` | Adaptation prioritisation | `methodology.tex:269–272`: relative closeness is “given by Equation …”; definition at line 272. |
| M7 | `eq:moran` | Spatial statistics | `methodology.tex:222–223`: global autocorrelation is calculated with the equation; definition at line 223. |
| M8 | `eq:gini` | Spatial statistics | `methodology.tex:228–231`: equity is summarized by the Lorenz approximation; definition at line 231. |

The handoff equations `eq:xattr`, `eq:servicearea` and optional `eq:orient` were verified at `methodology.tex:73,84,107` and were not reinserted. O2–O4 were excluded to honor the order’s instruction not to inflate the equation count; O1 was already present and supplies the one useful optional definition.

## 4. Em-dash/en-dash audit (before/after grep counts, per file)

“Before” is the supplied rollback archive `paper/manuscript/_backup_src_20260719_021355.tar.gz`, the only pre-edit source baseline. The handoff source already had 81 em-dashes after partial work; the archive reproduces the LEAD’s stated 90/31 inventory.

| Section file | `---` before | `---` after | letter–`--`–letter before | after |
|---|---:|---:|---:|---:|
| appendix.tex | 8 | 0 | 0 | 0 |
| background.tex | 12 | 0 | 0 | 0 |
| conclusions.tex | 8 | 0 | 0 | 0 |
| declarations.tex | 0 | 0 | 0 | 0 |
| discussion.tex | 15 | 0 | 5 | 0 |
| introduction.tex | 4 | 0 | 1 | 0 |
| methodology.tex | 7 | 0 | 4 | 0 |
| results.tex | 22 | 0 | 14 | 0 |
| study_area.tex | 10 | 0 | 4 | 0 |
| titleAbstract.tex | 4 | 0 | 3 | 0 |
| tables/data_inventory.tex | 1 | 0 | 1 | 0 |
| **Total (all source prose)** | **91** | **0** | **32** | **0** |

The work order's 90/31 inventory covers the section files; the full source audit also found one placeholder and one compound label in `tables/data_inventory.tex`, both now recast. Final full-tree audits returned zero for both patterns. Numeric ranges retain standard LaTeX range markup only where it is semantically required. `\emph{}` fell from 59 to 17 (71% reduction). Whole-word `honest|honestly|candid|notably|crucially|importantly` fell from 8 to 0. Spelling was standardized to the `optimize/optimization/optimizer` family.

## 5. Chosen title + rationale + files updated

Chosen title: **Explain, then Optimize: Urban Fabric and Climate Adaptation Priorities in İzmir**.

This is candidate 1, the LEAD’s recommendation. It is ten words, contains no dash, names the two-stage logic without technical clutter, and retains the policy object and study city. Updated at `sections/titleAbstract.tex:1–2` and `title_page.tex:14–15`; the keyword list was revised at `titleAbstract.tex:64–66` to complement rather than repeat the title.

## 6. Author change (additions made + TODO fields)

Hilmi Evren Erdin is author 3 in `sections/titleAbstract.tex:10–13` and `title_page.tex:21`. The assumed Department of City and Regional Planning, Dokuz Eylül University affiliation appears at `title_page.tex:27–28`. The proposed CRediT line is at `title_page.tex:43`, and the matching declaration is at `sections/declarations.tex:6–7`.

No ORCID or academic title was invented. `%TODO-TITLE%` and `%TODO-ORCID%` occur only at `titleAbstract.tex:10,12` and `title_page.tex:27,35`; the rendered title page therefore leaves these unknown fields blank.

## 7. Figure changes (per figure: old state → new state, production script, PNG path, caption text; preview paths for the new Fig12(c) and Fig14(b) maps)

### `fig:priority-synthesis` (current Figure 10; user’s Figure 12)

- Old → new: two non-spatial scatter panels → retained panels (a,b) plus panel (c), a 3,777-cell EPSG:32635 map with 223 stratum-colored frontier cells, grey dominated cells, coastline, north arrow, 5 km scale bar and bay inset.
- Production: `scripts/pilot_13_cell_pareto.py:256–329`, hooked at `scripts/generate_all_figures.py:17`.
- PNG/preview: `outputs/figures/priority_synthesis.png`.
- Caption (`sections/results.tex:261`): “Multi-objective adaptation priority synthesis … (c) Spatial distribution of all cells … with the 223 non-dominated frontier cells … and a bay-front inset.”
- Spatial reading (`results.tex:185–192`): frontier median coast distance is 0.62 km versus 4.19 km for dominated cells, supporting the bay-front/coastal-industrial concentration statement.

### `fig:flow-sankey` (user’s Figure 13)

- Old → new: alluvial figure and anchoring prose → removed entirely. `make_fig09_flow_sankey.py` remains on disk, as ordered, but was removed from `generate_all_figures.py`.
- No information loss: the stratum/cluster transition data remain in `outputs/tables/cluster_vs_stratum.csv` and appendix `tab:cluster-priority`; the legacy PNG/GPKG may remain as an unreferenced artifact.
- Evidence: final `rg 'flow-sankey' sections/*.tex main.tex` returned empty; regenerated manifest contains no flow entry.

### `fig:topsis-robustness` (current Figure 11; user’s Figure 14)

- Old → new: retained Monte-Carlo rank boxplots in (a); replaced abstract parallel coordinates in (b) with the cell-level entropy-weighted closeness map and 223 frontier outlines.
- Production: `scripts/make_fig11_topsis_robustness.py:132–199`, hooked at `scripts/generate_all_figures.py:18`.
- PNG/preview: `outputs/figures/topsis_robustness.png`.
- Caption (`sections/results.tex:268`): “Adaptation priority ranking sensitivity and spatial targeting … (b) Cell-level entropy-weighted TOPSIS closeness $C_i$ …”; it also carries the removed box’s entropy weights (50.3%, 23.8%, 22.9%, 2.9%, 0.0%).

### Supplementary figures

- Old → new numbering: hand-written, out-of-order S labels/main counters → automatic S1–S7 using `appendix.tex:2–8`, including unique `\theHfigure`/`\theHtable` anchors.
- Old S4 four panels → current S7 three panels; redundant strata closeness distributions removed. Production: `scripts/make_supp_fig_s4.py`; PNG: `outputs/figures/supp_topsis_sensitivity.png`; caption `appendix.tex:288`.
- Main SHAP duplicate diagnostic: full two-model/RMSE box → one line, “Spatial-block CV: full-model R² = 0.27,” at `scripts/pilot_09_shap.py:195–198`; full diagnostics remain in current S6.
- `supp_data_quality` panel (d) was retained. It is defensible because it audits the two demographic inputs and is not visually duplicated elsewhere.
- GeoPackage mapping/export report updated: `outputs/figure_gpkgs/figure_gpkg_export_report.md:23–28`; exporter produced 16 GPKGs and omitted the removed Sankey.

## 8. Deepening changes (5.1–5.4 one by one; evidence for the axis-contradiction fix)

### 5.1 Axis contradiction

`scripts/pilot_11_priority.py:37` defines `AX = [heat, cooling_deficit, access_deficit, coastal_expo, social_vul]`; `outputs/tables/adaptation_priority.csv` contains those five derived columns and no pluvial optimizer axis. I therefore chose the order’s primary resolution: pluvial susceptibility remains a released screening overlay, not a ranked need axis. The real five axes now appear in `methodology.tex:241–242` and `titleAbstract.tex:42–45`; the screening boundary appears in `introduction.tex:51–53`, the existing proxies paragraph, and the explicit limitation at `discussion.tex:127–130`.

### 5.2 RQ-to-answer mapping

`conclusions.tex:15–27` closes RQ1 through RQ4 in order: differentiation yes with consolidation; partial scale stability (ARI 0.38); fabric-specific mechanisms; no stratum-level dominance but a 223-cell frontier and waterfront mean-rank priority.

### 5.3 Policy translation

`discussion.tex:81–99` adds all seven strata with dominant signed SHAP mechanism, frozen Monte-Carlo mean rank, and a decision package. Source numbers are `outputs/tables/shap_per_stratum_mechanism.csv` and `outputs/tables/adaptation_priority.csv`; no new analysis or citation was introduced.

### 5.4 Quantitative SHAP statement

`discussion.tex:71–79` reports peripheral green-cover SHAP = −0.83 °C, industrial large-footprint SHAP = +0.41 °C and their 1.24 °C attributable contrast. The wording explicitly says these are fitted model associations, not causal intervention effects.

## 9. Consistency sweep: ADDITIONAL problems YOU found (beyond the LEAD's list)

1. Resetting visible appendix counters initially created duplicate Hyperref destinations even though printed S labels were correct. Added `\theHfigure` and `\theHtable` at `appendix.tex:3,6`; final log has zero duplicate destinations.
2. The SHAP production script could overwrite frozen tables with nondeterministic refits. The first trial was caught by `report_canonical_numbers.py`; canonical tables were restored, and `scripts/pilot_09_shap.py:94–110` now requires and reads the frozen CSVs rather than rewriting them. The final canonical report again prints `dist_coast_km=0.625321`, `f_green=0.369751`, and `bld_mean_area=0.291768`.
3. The GeoPackage export mapping still reflected obsolete standalone scale/inequality figures and the removed Sankey. `scripts/export_figure_gpkgs.py:690–883` now maps merged panels, Figures 7–11 and S4–S7 correctly and includes cell/map context layers for Figures 10 and 11.

## 10. Build evidence (latexmk summary, log warning count, PDF page count, figure count)

- Commands: `latexmk -pdf -interaction=nonstopmode main.tex` and the same for `title_page.tex`; both ended “All targets … up-to-date.”
- `main.log`/`title_page.log`: 0 `Undefined references`, 0 undefined citations, 0 multiply-defined labels, 0 duplicate destinations, 0 `Overfull \hbox`, and 0 LaTeX/natbib warning lines.
- Citation script: `cite keys used: 99`, `bib entries: 99`, `UNDEFINED: 0`, `UNUSED: 0`.
- PDFs: `main.pdf` = 64 A4 pages, 17,898,639 bytes; `title_page.pdf` = 1 A4 page, 55,258 bytes.
- Figures: 18 figure environments total = 11 main figures + 7 automatically numbered supplementary figures.
- Canonical check: N = 3,777; ARI = 0.381 (reported 0.38); burden Gini = 0.265 (reported 0.26); frontier = 223/3,777; manuscript Table 2/3 values unchanged.
- Visual QA: Poppler rendered all 64 pages at 72 dpi to `tmp/pdfs/rev2_visual_qa/page-*.png`; four contact sheets and the title page were inspected. Equations fit, Figures 10/11 are legible, S1–S7 are sequential, and no clipping/overlap/broken glyph was found.

## 11. Questions for the user (Erdin ORCID/title/CRediT approval, title approval, etc.)

1. Please supply Hilmi Evren Erdin’s ORCID iD.
2. Please confirm his academic title for the affiliation line.
3. Please confirm the assumed Department of City and Regional Planning, Dokuz Eylül University affiliation.
4. Please approve or revise the proposed CRediT roles: Supervision, Conceptualization, Writing - Review & Editing.
5. Please approve the chosen title, “Explain, then Optimize: Urban Fabric and Climate Adaptation Priorities in İzmir.”

## 12. Full list of modified files + path of the backup archive

Backup used and not duplicated: `paper/manuscript/_backup_src_20260719_021355.tar.gz`.

Manuscript/source and report:

- `paper/manuscript/src/sections/{appendix,background,conclusions,declarations,discussion,introduction,methodology,results,study_area,titleAbstract}.tex`
- `paper/manuscript/src/tables/data_inventory.tex`
- `paper/manuscript/src/title_page.tex`
- `paper/manuscript/src/refs.bib` (handoff’s two verified entries; not re-added)
- `docs/revision/WORKER_REPORT_rev2.md`

Production scripts:

- `scripts/pilot_13_cell_pareto.py`
- `scripts/make_fig11_topsis_robustness.py`
- `scripts/make_supp_fig_s4.py`
- `scripts/pilot_09_shap.py`
- `scripts/generate_all_figures.py`
- `scripts/export_figure_gpkgs.py`

Regenerated figures/tables:

- `outputs/figures/{priority_synthesis,topsis_robustness,supp_topsis_sensitivity,shap_synthesis}.png`
- `outputs/tables/{cell_pareto_summary,cell_priority_top20,shap_global_importance,shap_per_stratum_mechanism}.csv`
- `data/03_processed/cell_priority.csv`

GeoPackage export and metadata:

- `outputs/figure_gpkgs/figure_gpkg_manifest.csv`
- `outputs/figure_gpkgs/figure_gpkg_export_report.md`
- `outputs/figure_gpkgs/figure_{01_study_area_map,03_tissue_comparisons,04_fabric_comparison,05_raw_morphology_maps,06_cluster_synthesis,07_scale_stability,08_shap_synthesis,09_explainable_heat_interactions,10_geostats_map,11_spatial_inequality,12_priority_synthesis,14_topsis_robustness,15_supp_s1_data_quality,16_supp_s2_pca_diagnostics,17_supp_s3_xgb_diagnostics,18_supp_s4_topsis_sensitivity}.gpkg`

Compiled deliverables:

- `paper/manuscript/src/main.pdf`
- `paper/manuscript/src/title_page.pdf`
- Standard latexmk auxiliary/log files in `paper/manuscript/src/` were refreshed by the clean build.
