# Pilot progress & resume guide — ICUS 2026 İzmir grid paper

_Last updated: 2026-06-20._ **Single source of truth for resuming work.** The
empirical pilot AND a full first manuscript draft are complete; what remains is
finishing/refinement (Section 8). Read Section 0 first.

---

## 0. Resume here (next session)
State (v7, 2026-06-24): **UPGRADED from the N=700 pilot to a FULL CENSUS of all
3,777 urban cells**, with **network-distance service areas** (400/800 m, Dijkstra on
the BBB road graph) replacing radial buffers, and a refined waterfront stratum rule
(`dist_core_km<=15` so it no longer over-captures remote peninsulas). Full pipeline
re-run (`pilot_03`→`pilot_14`); **all headline numbers re-derived** (Section 4) and the
manuscript + every figure re-synced. LaTeX compiles to **55 pp, 0 undefined**;
`check_citations.py` clean (97 cite = 97 bib). Cover letter + highlights drafted
(`paper/`). Congress abstract reconciled to the census (TR 706 / EN 750 words). New
helper: `scripts/report_canonical_numbers.py` (re-derives every headline number from
the CSVs). Remaining = author tasks (Section 8). Nothing is mid-run; everything local.

Quick sanity check after opening:
```
.venv/Scripts/python.exe -c "import ee; ee.Initialize(project='ee-geophilo'); print('ok')"
# latexmk now WORKS (Strawberry Perl installed). Build from anywhere with -cd:
latexmk -cd -pdf paper/manuscript/src/main.tex          # -> 54 pp, 0 undefined
# fallback: cd paper/manuscript/src; pdflatex main; bibtex main; pdflatex main; pdflatex main
```

---

## 1. Environment (project-local; never depend on other projects)
- venv: `.venv/` (`uv venv --python 3.12`). Run all scripts with `.venv/Scripts/python.exe`.
- deps: `requirements.txt` → `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`.
- GEE: `ee.Initialize(project="ee-geophilo")` (creds in `~/.config/earthengine`).
- LaTeX: MiKTeX 25.4 + **Strawberry Perl 5.42.2** (portable, `C:\Users\YE\Strawberry`,
  `perl\bin` on USER PATH) → **`latexmk` 4.88 works**. Build: `latexmk -cd -pdf <main>.tex`.
  Global cfg `C:\Users\YE\.latexmkrc`; full system doc in `C:\Users\YE\PyCharmMiscProject\AGENTS.md`.
- `bbtmk_papers/` = **read-only** source to copy open data from; never modified.

## 2. Data (all local, EPSG:32635 unless noted). Provenance: `data/01_raw/PROVENANCE.md`
| Layer | Path |
|---|---|
| Study boundary | `data/00_external/boundaries/izmir_study_boundary.gpkg` |
| Districts / neighbourhoods | `…/boundaries/ilce.shp` (30); `mahalle.shp` (1317, **EPSG:5253**, name-only) |
| Buildings (official BBB) | `data/01_raw/buildings/izmir_buildings_bbb.gpkg` (901,609; `ZEMINUSTUK`=floors) |
| Roads (official BBB) | `data/01_raw/roads/izmir_roads_bbb.gpkg` (207,741) |
| ESA WorldCover 2021 | `data/01_raw/worldcover/izmir_worldcover2021_10m.tif` |
| Summer LST JJA 2014–2024 | `data/01_raw/lst_jja/lst_jja_mean_*_100m.tif` (°C, nodata −9999) |
| DEM + slope (GLO-30) | `data/01_raw/dem/izmir_{dem,slope}_glo30_30m.tif` |
| Coastline | `data/01_raw/coastline/izmir_coastline_osm.gpkg` |
| Population / vulnerability | `data/01_raw/population/izmir_population_data.xlsx` (raw ADNKS) and `mahalle_population_controls_2024.gpkg` (pre-joined, with `elderly_65_plus_share`, `age_dependency_proxy`) |

## 3. Pipeline (scripts/, run in order) and outputs
| Step | Script | Output(s) |
|---|---|---|
| acquire | `download_coastline.py`, `download_worldcover.py`, `download_dem.py`, `convert_bbb_layers.py` | `data/01_raw/*` |
| 1 grid + exclusion | `pilot_01_build_grid.py` | `data/02_interim/grid_250m_{full,urban}.gpkg` (16,496 → **3,777 urban**) |
| 2 enrich | `pilot_02_enrich.py` | `grid_250m_urban_enriched.gpkg` (dist_coast, dist_core) |
| 3 strata (provisional) | `pilot_03_strata.py` | `grid_250m_urban_strata.gpkg`; `outputs/figures/strata_map_provisional.png` |
| 4 sample | `pilot_04_sample.py` | `grid_250m_sample.gpkg` (**100×7 = 700**) |
| 5 indicators | `pilot_05_indicators.py` | `data/03_processed/cell_indicators.csv` (700×29; BBB buildings/roads) |
| 6 attach LST | `pilot_06_lst.py` | `data/02_interim/lst_jja_mean_2014_2024_100m.tif`; `lst_summer` col |
| 7 PCA + Ward | `pilot_07_cluster.py` | `cell_clusters.csv`; `outputs/tables/cluster_*.csv`; dendrogram |
| 8 scale stability | `pilot_08_scale_stability.py` | `outputs/tables/scale_stability.csv` |
| 9 SHAP explain | `pilot_09_shap.py` | `outputs/{figures,tables}/shap_*` |
| 10a vulnerability | `pilot_10_vulnerability.py` | `svi` col in `cell_indicators.csv` |
| 10b GeoStats | `pilot_12_geostats.py` | `cell_geostats.csv`; `outputs/tables/geostats_summary.csv` |
| 11 priority | `pilot_11_priority.py` | `outputs/tables/adaptation_priority.csv`; `priority_pareto.png` |
| 13 cell Pareto | `pilot_13_cell_pareto.py` | `data/03_processed/cell_priority.csv`; `outputs/tables/cell_pareto_summary.csv`, `cell_priority_top20.csv`; `cell_pareto.png` |
| 14 geo map | `pilot_14_geomap.py` | `outputs/figures/geostats_map.png` (Gi* + LISA adaptation-need map) |

NB: `cell_indicators.csv` accumulates columns across steps 5→6→10a (rerun 5 first if rebuilding).

## 4. Real results (FULL CENSUS N=3,777, network service areas — screening; do not embellish)
_v7 (2026-06-24): re-derived from the processed CSVs via `scripts/report_canonical_numbers.py`.
These SUPERSEDE the v6 pilot numbers (N=700, radial buffers, k=3, ARI 0.505) and match the manuscript._
- **Form** sharply separates strata: historic_core FAR 1.69 / 4.13 floors; waterfront tallest
  (5.08 floors — bay high-rise); industrial lowest orientation entropy 0.67; peripheral FAR 0.07.
- **LST**: industrial hottest 45.5 °C, waterfront coolest 41.7 °C (range 3.8 °C).
- **Typology**: PCA(7,91%)+Ward → **k=4** super-types (silhouette 0.224; sizes 1265 / 1062 / 1327 /
  123 = compact core / coarse-grain large-footprint / low-density peripheral / sparse fringe).
  **Scale stability: ARI 0.38** (250 m k=4 vs 500 m k=3; *fair* — the finest mode is scale-sensitive).
- **SHAP**: morphology-only spatial-block R²≈**0.09** (RMSE 1.98 °C — now POSITIVE); +coastal/topo
  context R²≈0.27 (RMSE 1.78 °C). **Distance-to-coast dominates** summer LST; leading *morphological*
  terms = green-cover (peripheral −0.81 °C) and mean footprint area (industrial +0.40 °C).
  Linear baselines: Ridge morph +0.04 / full −0.15; Elastic-Net +0.04 / −0.12 (can't exploit context).
- **Vulnerability**: SVI highest waterfront (elderly 19.0%), lowest industrial (10.5%).
  **0 fallback** — over the census every cell falls within a populated mahalle (the v6 "66 fallback" is gone).
- **Priority (5 axes, TOPSIS)**: **waterfront = clear #1** (entropy 0.75; MC rank 1.6 [1–3]) though
  coolest → equity inversion (cleaner than the pilot). All 7 non-dominated at fabric level.
- **Cell-level Pareto**: **223/3,777 cells (5.9%) non-dominated**. Frontier rate highest in
  waterfront (33%), lowest apartment_block (1.8%). Entropy-TOPSIS collapses onto access_deficit →
  report frontier membership/composition, not a unique cell order.
- **Spatial**: Moran's I LST 0.71 / SVI 0.83 / need 0.72 (p=.001); LISA HH in industrial (203) /
  waterfront (183) / apartment (138); Gi* 843 hot / 819 cold; equity-burden Gini 0.27.

## 5. Manuscript draft (`paper/manuscript/src/`, compiles 33 pp, 0 undefined)
Drafted from real numbers: Title/Abstract (reports findings), §1 Intro, §2 Background,
§3 Study area + **Table 1** (data inventory), §Methods (v3 chain), **§6 Results** (5
subsections + `tab:fabric-profiles`, `tab:priority`), §7 Discussion, §8 Conclusions.
Bibliography `refs.bib` = 94 Crossref-verified entries (v3 anchors + classics). Target
journal: *Sustainable Cities and Society*. Verifier: `references/scripts/verify_v3_anchors.py`.

**Figures embedded (2026-06-15):** `\graphicspath` fixed to `../../../outputs/figures/`;
6 figures wired in with captions + `\ref`s (COMPILED order) — Fig 1 strata map
(study_area); Fig 2 dendrogram, Fig 3 SHAP importance, **Fig 4 Gi*/LISA need map**
(`pilot_14_geomap.py`), **Fig 5 fabric Pareto**, **Fig 6 cell-level Pareto** (all
Results). [Cross-refs use `\ref`, so numbering is automatic & correct in the PDF.] **Appendix filled** (`sections/appendix.tex`):
algorithm-parameter longtable (Table 4, params verified against the scripts) +
reproducibility checklist. `declarations.tex` already complete (CRediT / funding /
competing interests / AI-use).

**QC consistency pass (2026-06-15):** reconciled abstract/intro/methods/Table 1 with what
the pilot actually computed — removed **MGWR** (never run) and **spatial-Gini** (decomposition
was an artefact), keeping Moran/LISA/Gi* + a burden Gini; MGWR reframed as deferred to the full
study. Recompiles 33 pp, 0 undefined.

## 6. Key decisions & caveats (read before resuming)
- **Strata are PROVISIONAL** (rule-based, `pilot_03`); earmarked for refinement with
  planning docs + urban-design input (H. Topçu). Waterfront rule over-captures remote
  peninsulas. Clustering tests/refines them (keep a-priori-then-test logic).
- **Buildings/roads** = official İzmir BBB (replaced sparse OSM; floors → real FAR).
- **Shared open data** with sibling SAM3/PFI study (LST, boundary, mahalle, population) —
  disclosed in Methods §repro; no text reuse, no overlapping findings.
- Exclusion (step 1): f_built≥0.10, f_water≤0.50, slope_mean≤15%. Sampling: seed 42, 100/stratum.
- SVI matched 581/700 cells (119 filled neutral 0). Mahalle.shp has names only (no code) →
  used the sibling's pre-joined population layer instead.
- All results modest/screening-level — the contribution is the integrated method + the
  equity inversion, not predictive accuracy.

## 7. Memory
Project memory: `…/memory/icus2026-izmir-morphometrics-paper.md` (v4 + pilot notes) mirrors this.

## 8. Remaining work (prioritised — pick up here)
**DONE 2026-06-15 (this session):** (1) figures embedded — `\graphicspath` fixed,
**6 figures** with captions + `\ref`s (incl. Fig 4 Gi*/LISA need map, `pilot_14`); (3)
cell-level Pareto (`pilot_13`; 178/700 selective frontier; into §6.5 + Fig 5 + discussion
limit (v)); (4) appendix parameter table + reproducibility checklist (`declarations.tex` was
already complete); (QC) reconciled abstract/intro/methods/Table 1 — dropped unused **MGWR** &
artefactual **spatial-Gini**, kept Moran/LISA/Gi* + burden Gini. Manuscript → 33 pp, 0 undefined.

**DONE 2026-06-20 (session 1):** (1) Split the monolithic `make_supp_figs.py` into 4 modular scripts (`make_supp_fig_s1.py` to `make_supp_fig_s4.py`) in `scripts/`; (2) Revised all manuscript and supplementary figures to conform strictly to the Figure Style Guide color palette (Gold, Muted Slate, Sadi Colors), typography (Arial), backgrounds (`#f8fafc`), and 180 DPI resolution; (3) Cleaned the repository by removing the old monolithic file; (4) Orchestrated and verified all figures by running `scripts/generate_all_figures.py`; (5) Upgraded Figure 6 (`tissue_comparisons.png`) to overlay the measured summer LST on all 35 panels and adjusted scale bar layout; (6) Audited all figure and table in-text citations, verifying that every citation occurs immediately before the respective environment declaration (`Order: OK` across the entire document); (7) Resolved flowchart (`fig:flowchart`) citation and moved the environment block; (8) Linked all supplementary figures (S1–S4) to their relevant sections in the main text and appendix; (9) Recompiled the LaTeX manuscript `main.pdf` successfully (51 pages) with all figures integrated.

**DONE 2026-06-20 (session 2 - peer-review revisions):** (1) Completely cleaned up and reverted all modifications from the peer-review-system; (2) Reconciled Adjusted Rand Index (ARI) to 0.505 consistently across all sections, including the abstract; (3) Computed and reported the Ridge ($R^2 \approx -0.10$ / $-0.38$) and Elastic-Net ($R^2 \approx -0.08$ / $-0.07$) spatial-block CV metrics alongside XGBoost in results.tex; (4) Added detailed guidance in results.tex on how planners should navigate TOPSIS rank sensitivities; (5) Documented the nearest-neighbour SVI fallback methodology and explained why it prevents spatial autocorrelation bias; (6) Corrected Landsat resolution description (100m native vs resampled 30m vs zonal 250m) in study_area.tex; (7) Clarified pedestrian reaches are network walking distances using segment routing via OSMnx and QGIS; (8) Standardized all dotted capital I spellings of İzmir (\.{I}zmir) across the manuscript; (9) Updated captions for Figures 6 and 8, Table 2, and EPSG:32635 parameters; (10) Redesigned all 4 supplementary figures (S1--S4) as detailed, 4-panel diagnostic dashboards, adding advanced diagnostics (bivariate geographic/demographic distributions, PCA loadings heatmap, clusters in PC space, XGBoost spatial residuals maps, observed vs predicted LST, raw TOPSIS closeness distributions, and peripheral expansion rank sensitivity); (11) Updated the appendix text to comprehensively describe all 16 diagnostic panels; (12) Verified clean compilation of the final 54-page PDF.

**DONE 2026-06-22 (integrity + consistency reconciliation pass):** (1) Re-derived **every**
headline number from the processed CSVs and reconciled the manuscript to them: fixed Table 2
(TOPSIS entropy 0.79→0.73 and the rest; re-ordered rows by entropy-TOPSIS; ranks synced to the
re-run `pilot_11`), fixed prose "TOPSIS 0.79"→0.73, and "SVI lowest in apartment blocks"→
industrial/logistics (elderly 10.0%). Table 1, cluster sizes (257/173/270), Gi* (161/188),
LISA HH (56/45/25), Moran (0.52/0.72/0.65), Gini (0.30), cell-Pareto (150/700=21.4%; waterfront
54% / apartment 1%), SHAP R² (−0.07 / 0.26) all independently re-verified = match. (2) **Integrity
fix:** methodology claimed 400/800 m catchments were *network-distance routing* "rather than
Euclidean buffers" — but `pilot_05` uses a circular `centroid.buffer()`. Rewrote methodology,
the cross-attribution rule, the appendix param row, and the response-to-reviewers Comment 8 to
state honestly that the pilot uses **radial (Euclidean) buffers**, with network service areas as
a planned refinement. (3) Softened "strata defined from planning documents" → rule-based proxies
(consistent with the provisional/limitations framing) in methodology + study_area. (4) Trimmed
"XGBoost/LightGBM/CatBoost"→XGBoost and "pixel/tessellation scale"→grid-cell scale; dropped
unused "ECOSTRESS"; fixed road count 207,741→**207,734** (data_inventory) to match appendix/data.
(5) **Reference integrity:** all 97 cite keys = 97 bib entries (0 undefined/unused). Crossref-verified
the 9 entries not in the prior reports; caught + fixed **two fabricated-metadata refs** the
peer-review pass had added — `cooper2018sDNA` (was 2018/SoftwareX 7/160–165, no DOI → real paper is
2020/SoftwareX 12/100525, renamed `cooper2020sDNA`) and `lindberg2018UMEP` (was Theor.&Appl.Climatol.
134/953–972, no DOI → real journal Env.Model.&Softw. 99/70–87, doi added). `tesspy_zenodo` confirmed OK.
(6) Recompiled: **54 pp, 0 undefined citations/refs, 0 overfull hboxes**. Helper scripts:
`scripts/check_citations.py`, `scripts/verify_unchecked_refs.py`.

**DONE 2026-06-23 (figure-integrity audit + congress-abstract reconciliation):** (1) Audited every
figure that embeds a statistic. Found + fixed **two figures that recomputed the wrong quantity**:
`make_fig11_topsis_robustness.py` (entropy-weight text box was hardcoded "Access 80% / Social 3%" →
now computes the real weights live: **Social 47% / Coastal 26% / Access 24% / Cooling 3% / Heat 0%**;
manuscript caption corrected too), and `make_fig08_spatial_inequality.py` (Moran panel used
`topsis_entropy` → **need** score; Lorenz/Gini used `heat*social_vul` → authoritative **burden**
column; figure now shows **Moran I=0.65, Gini=0.30**, matching the text). Regenerated both PNGs and
recompiled (54 pp). Verified the rest are correct/live: flowchart (91%, ARI 0.505, exclusion), cluster
silhouette **0.222**, scale-stability ARI 0.505, SHAP R² 0.26, geostats_map (Gi*/LISA from CSV),
cell-Pareto "150/700 (21.4%)", graphical abstract. (2) Reconciled the **congress abstract** (source
`scripts/build_icus2026_submission_ready_pdf.py` + `abstracts/icus2026_abstract_q1_revised.md` + regenerated
PDF + `icus2026_cmt_submission_guide.txt`): dropped **"spatial Gini"** → "Gini of the exposure–vulnerability
burden" (journal dropped spatial-Gini as artefact), softened "planning documents"→rule-based proxies,
fixed the `işsel`→`işlevsel` typo (the .md had drifted from the script), removed ECOSTRESS/MGWR-as-current
from notes. Word counts TR 693 / EN 735. Headline numbers (3,777; 700; ARI 0.505; equity inversion) already
matched. (Pre-pilot `docs/manuscript/icus2026_q1_manuscript_skeleton.md` left as a historical artefact.)

**DONE 2026-06-24 (v7 — full-census + network-areas upgrade):** strata refined (waterfront
`dist_core<=15` fix, validated on the map); switched to **FULL CENSUS** (3,777 cells; `pilot_04`
FULL_CENSUS mode); implemented **network-distance service areas** in `pilot_05` (scipy Dijkstra on
the BBB road graph) replacing radial buffers; re-ran `pilot_03`→`pilot_14`; re-derived every number
(`report_canonical_numbers.py`) and re-synced the manuscript + all figures (figure scripts made
k-robust; `make_fig05` now reads the silhouette curves from CSV instead of hardcoding); added
Ridge/Elastic-Net baselines to `pilot_09`; added the **AI-use declaration**; drafted
`paper/cover_letter.md` + `paper/highlights.txt`; reconciled the congress abstract/PDF/CMT to the
census (TR 706 / EN 750). Compiles **55 pp, 0 undefined**; `check_citations.py` 97=97.

**DONE 2026-06-24 (v7.1 — desk-reject professionalization pass, user-flagged):** removed every
internal-implementation leak from the manuscript body that would invite desk-rejection: (a) deleted the
**sibling-project cross-reference** (SAM3/GNNWR "parallel İzmir study") from methodology §4.10, the
data-inventory footnote, declarations and the appendix repro checklist — the shared-open-data disclosure
now lives ONLY in the editor cover letter, which is the correct venue; (b) rewrote all **internal file/script
paths** (`scripts/pilot_01–14`, `logs/`, `requirements.txt`, `data/01_raw/PROVENANCE.md`, `outputs/`) to
professional language ("the analysis code is openly released in a version-controlled repository"; "logged with
the released code"); (c) softened a **phantom validation claim** ("is checked against a cadastral sub-area" →
"can be validated against … where available"); (d) **removed the project-tracking "Status (Ready/Derive)"
column** from Table 1 (now Layer/Source/Resolution/Licence/Role) and fixed the stale "sampling (42)" repro item
(full census, no sampling). Plugin citations kept (author's own open software; competing interest declared).
grep confirms ZERO `scripts/`/`pilot_NN`/`logs/`/`SAM3`/`sibling` leaks in `src/*.tex` (only the invisible
`\graphicspath`). Recompiled **55 pp, 0 undefined**; `check_citations.py` 97=97.

**STILL OPEN (need author / planning input):**
1. **Strata refinement with planning documents + H. Topçu** — the waterfront over-capture is fixed,
   but the 7 rule-based strata are still provisional; planning-doc input would let `pilot_03` be
   frozen (then rerun `pilot_03`→`pilot_14`). The census already shows them consolidating into 4 modes.
2. **<20% similarity check** + author verify & rewrite in own voice (congress AI-ethics) — applies to
   BOTH the journal manuscript and the congress abstract; the author must read and own the prose.
3. Optional robustness (honestly deferred to future work): seasonal/diurnal LST split (needs new GEE
   winter/night scenes); pixel-scale SHAP; MGWR for local non-stationarity.
4. Author specifics: funding line (now "None declared"), acknowledgements, plugin **Zenodo DOIs**.
