# WORK ORDER — ICUS2026 Manuscript Revision (rev2)

> **Role split:** This file was written by the LEAD (brain) agent. You are the WORKER agent.
> Execute the tasks in this order, then write a comprehensive `.md` report that **exactly
> follows the report contract in Section 8**. The lead agent will audit your report;
> incomplete or unverified work will be rejected.

---

## HANDOFF STATE (2026-07-19) — READ BEFORE ANYTHING ELSE

A first worker agent was stopped mid-run after making partial progress. **Do not redo or
duplicate the items below; verify them and continue from this state.** Everything else in
this order is written as if starting from scratch; where a statement below contradicts the
body text (e.g. "the manuscript contains no equations"), this section wins.

Already completed (verified by the LEAD):
1. **Backup exists:** `paper/manuscript/_backup_src_20260719_021355.tar.gz` (pre-edit
   state of the whole `src/` tree). Do NOT create a second backup; this one is the
   rollback baseline.
2. **Task 1, partial:** `methodology.tex` already contains three numbered equations with
   prose integration: `eq:xattr` (M1) and `eq:servicearea` (M2) in the cross-attribution
   subsection, and `eq:orient` (optional O1) in the indicators subsection. Still missing:
   M3 (`eq:shap`), M4 (`eq:pareto`), M5 (`eq:entropy`), M6 (`eq:topsis`), M7 (`eq:moran`),
   M8 (`eq:gini`). Do not re-insert or re-label the three existing ones.
3. **refs.bib:** `lundberg2020LocalExplanations` (DOI `10.1038/s42256-019-0138-9`) and
   `boeing2019UrbanSpatial` (DOI `10.1007/s41109-019-0189-1`) were added and have been
   **DOI-verified against Crossref by the LEAD** (titles match exactly). No further
   verification needed for these two; the rule still applies to any other new citation.
4. **Task 5.1, partial:** the scope-boundary paragraph (pluvial = screening overlay, not a
   need axis) was added to the proxies subsection of `methodology.tex`. Still missing: the
   stale axis list "(heat, pluvial, coastal, access deficit, social vulnerability)" at
   ~line 217 of `methodology.tex` must be corrected to the real five axes; the abstract,
   introduction and limitations must be reconciled as specified in Task 5.1.
5. **Task 2, trace amount:** one "reported honestly" was already changed to "reported
   conservatively" in `methodology.tex`. The full dash/tell purge remains to be done.

Untouched by the first worker: `results.tex`, `discussion.tex`, `conclusions.tex`,
`introduction.tex`, `background.tex`, `study_area.tex`, `titleAbstract.tex`,
`declarations.tex`, `appendix.tex`, `title_page.tex`, all figure scripts and PNGs.
No report was written.

---

## 0. Environment, sources and ground rules

**Working directory (source of truth):**
`C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience\paper\manuscript\src\`

| What | Path |
|---|---|
| Main document | `src/main.tex` (`\input`s the section files from `src/sections/*.tex`) |
| Title + abstract | `src/sections/titleAbstract.tex` |
| Separate title page | `src/title_page.tex` (compiled separately) |
| Declarations (author contributions) | `src/sections/declarations.tex` |
| Preamble | `src/mypreamble.sty` (`amsmath` is **already loaded**; no extra package needed for equations) |
| Bibliography | `src/refs.bib` (apalike/natbib) |
| Figure PNGs | `outputs/figures/` (graphicspath points there) |
| Figure data (with geometry) | `outputs/figure_gpkgs/figure_XX_*.gpkg` + `figure_gpkg_manifest.csv` |
| Figure generation scripts | `scripts/make_*.py`, `scripts/generate_all_figures.py`, shared style: `scripts/_manuscript_style.py` |
| Analysis pipeline (produces numbers) | `scripts/pilot_01..14_*.py`, canonical numbers: `scripts/report_canonical_numbers.py` |
| Output tables | `outputs/tables/*.csv` |

**Rules (violation = rejection):**

1. **Do not touch the analysis numbers.** All canonical values are frozen: Table 2 / Table 3
   values, the R2 scores, ARI = 0.38, Gini = 0.26, the Moran's I values, the 223-cell
   frontier, N = 3,777, and so on. When regenerating figures, verify these numbers did not
   change (compare against `scripts/report_canonical_numbers.py`).
2. **No invented references.** Any new citation must be verified against Crossref
   (`https://api.crossref.org/works/<doi>`) before it enters `refs.bib`. Title, authors,
   year and journal must match the Crossref record exactly. (This is an established project
   rule; see the reports under `references/verification/`.)
3. **No invented ORCID iDs or academic titles.** For unknown fields of the third author,
   insert `%TODO%` markers and list them in the report under "Questions for the user".
4. **Back up first:** before any edit, archive `paper/manuscript/src` as
   `paper/manuscript/_backup_src_YYYYMMDD_HHMMSS.tar.gz` (this habit already exists in the
   project, e.g. `outputs/_backup_figures_20260702_021838.tar.gz`).
5. The manuscript language is English. The text currently mixes "optimisation/optimise"
   with "optimization/optimize". **Standardise on one family** (recommendation: the "-ize"
   family) at the spelling level only, without touching terminology.
6. After each task, recompile and leave no errors or undefined references in the log
   (Section 7).

---

## Critical pre-findings (from the LEAD's reconnaissance — internalise these first)

### A. The PDF is STALE relative to the sources
`src/main.pdf` was compiled on 2026-07-01 01:02; the `sections/*.tex` files were edited
AFTER that (up to 02 July). Two figures present in the old PDF, `scale_stability` (old
Fig 7) and `spatial_inequality` (old Fig 11), were removed from the sources and their
panels merged into `cluster_synthesis` (Fig 6b,d) and `geostats_map` (Fig 10c,d). As a
result, the figure numbers the user quotes from the PDF differ from the current source
numbering. **Mapping table (labels are authoritative):**

| Label | File | Old PDF number (what the user saw) | After rebuilding current sources |
|---|---|---|---|
| `fig:priority-synthesis` | `priority_synthesis.png` | **Figure 12** | Figure 10 |
| `fig:flow-sankey` | `flow_sankey.png` | **Figure 13** | Figure 11 |
| `fig:topsis-robustness` | `topsis_robustness.png` | **Figure 14** | Figure 12 |

The user's requests about "Figure 12 / 13 / 14" refer to these three labels. First step:
do a clean rebuild to establish the current numbering baseline.

### B. Internal contradiction: is the fifth axis "pluvial" or "cooling deficit"?
- `methodology.tex`, the "optimize" subsection (around line 183), lists the axes as
  **"heat, pluvial, coastal, access deficit, social vulnerability"**.
- `results.tex` (res-priority subsection), the Fig 12 caption, and `appendix.tex`
  `tab:params` ("Need axes") all say: **"heat, cooling deficit, access deficit, coastal
  exposure, social vulnerability"**.
- The introduction and abstract claim "three hazards: extreme heat, pluvial flooding,
  coastal exposure", yet a pluvial axis NEVER enters the optimiser.

This is a consistency error and one of the concrete sources of the "shallow methods paper"
impression. The fix is defined in Task 5.1.

### C. Supplementary figure numbering is broken
In `appendix.tex`, figures whose captions are hand-labelled "Supplementary Figure S5/S6/S7"
(`supp_m1_heat_leverage`, `supp_vulnerability_robustness`, `supp_shap_stability`) appear in
document order BEFORE S1–S4; moreover all of them take numbers from the main counter
(Figure 15–18...). Fixed in Task 6.4.

---

## TASK 1 — Equations (highest priority)

The manuscript currently contains **not a single numbered equation**; the user requires the
key equations to be present. `amsmath` is loaded; use
`\begin{equation}...\end{equation}` + `\label{eq:...}` and **reference every equation at
least once in the prose** as `Equation~\eqref{...}` or `(Eq.~\ref{...})` (`\eqref` comes
with amsmath).

The 8 equations below are **mandatory**; placement is specified for each. The LaTeX blocks
are ready; adapt notation to the surrounding text without changing meaning. The equations
must be consistent with the actual parameters in `tab:params` (18 bins, k=8 neighbours,
2,000 Dirichlet draws, 6-block CV, ...).

**M1. The cross-attribution operator** — the paper's "methodological core".
Place in `methodology.tex`, subsection `\ref{sec:methods-xattr}`, replacing/alongside the
sentence "Formally, the cross-attribution rule...":

```latex
\begin{equation}\label{eq:xattr}
\bar{x}_{c}(g) \;=\; \frac{\sum_{t \in T(g)} a_{t \cap g}\, x_{c}(t)}
                        {\sum_{t \in T(g)} a_{t \cap g}},
\end{equation}
```
where $T(g)$ = the tessellation cells intersecting grid cell $g$, $a_{t\cap g}$ = the
intersection area, and $x_c(t)$ = the value of character $c$ on tessellation cell $t$.
State in the text that the area-weighted median/IQR analogues are produced with the same
operator.

**M2. Network service-area definition.** Same subsection, next to the 400/800 m definition:

```latex
\begin{equation}\label{eq:servicearea}
S_{r}(g) \;=\; \{\, e \in E \;:\; d_{\mathrm{net}}(v_{g}, e) \le r \,\},
\qquad r \in \{400, 800\}\,\mathrm{m},
\end{equation}
```
$v_g$ = the node nearest the cell, $d_{\mathrm{net}}$ = edge-length-weighted shortest-path
(Dijkstra) distance, $E$ = the set of street segments.

**M3. SHAP (Shapley) attribution.** Place in `methodology.tex`, subsection
`\ref{sec:methods-explain}`:

```latex
\begin{equation}\label{eq:shap}
\phi_{j} \;=\; \sum_{S \subseteq F \setminus \{j\}}
\frac{|S|!\,\bigl(|F|-|S|-1\bigr)!}{|F|!}\,
\Bigl[ f_{x}\bigl(S \cup \{j\}\bigr) - f_{x}(S) \Bigr],
\end{equation}
```
$F$ = the feature set, $f_x(S)$ = the conditional expected model output. Citation: for
TreeSHAP use Lundberg et al. 2020, *Nature Machine Intelligence*
(DOI `10.1038/s42256-019-0138-9`) — **verify on Crossref first**, then add to `refs.bib`
(the bib currently has NO methodological SHAP citation; this is a gap).

**M4. Pareto dominance definition.** Place in `methodology.tex`, subsection
`\ref{sec:methods-optimize}`:

```latex
\begin{equation}\label{eq:pareto}
i \succ j \;\iff\; n_{k}(i) \ge n_{k}(j)\;\; \forall k \in \{1,\dots,5\}
\;\;\wedge\;\; \exists\, k :\; n_{k}(i) > n_{k}(j),
\end{equation}
```
$n_k(\cdot)$ = the need axes coded so that larger values mean higher need; the
non-dominated set = the priority frontier.

**M5. Entropy weights.** Same subsection (before TOPSIS):

```latex
\begin{equation}\label{eq:entropy}
e_{k} \;=\; -\frac{1}{\ln m} \sum_{i=1}^{m} p_{ik} \ln p_{ik},
\qquad
w_{k} \;=\; \frac{1 - e_{k}}{\sum_{l} \bigl(1 - e_{l}\bigr)},
\qquad
p_{ik} \;=\; \frac{r_{ik}}{\sum_{i} r_{ik}},
\end{equation}
```

**M6. TOPSIS closeness coefficient.** Immediately after:

```latex
\begin{equation}\label{eq:topsis}
C_{i} \;=\; \frac{D_{i}^{-}}{D_{i}^{+} + D_{i}^{-}},
\qquad
D_{i}^{\pm} \;=\; \Bigl( \sum_{k} \bigl( w_{k} r_{ik} - v_{k}^{\pm} \bigr)^{2} \Bigr)^{1/2},
\end{equation}
```
$v_k^{+}/v_k^{-}$ = the ideal/anti-ideal points; $r_{ik}$ = the vector-normalised decision
matrix. (Hwang \& Yoon 1981 is already in the bib: `hwang1981MultipleAttribute`.)

**M7. Global Moran's I.** Place in `methodology.tex`, subsection `\ref{sec:methods-spatial}`:

```latex
\begin{equation}\label{eq:moran}
I \;=\; \frac{n}{\sum_{i}\sum_{j} w_{ij}}\;
\frac{\sum_{i}\sum_{j} w_{ij}\, z_{i} z_{j}}{\sum_{i} z_{i}^{2}},
\end{equation}
```
$w_{ij}$ = row-standardised k-nearest-neighbour weights ($k=8$), $z_i$ = deviation from the
mean. Optionally give local Moran $I_i$ and Getis-Ord $G_i^{*}$ in one extra equation
(optional item O2).

**M8. Gini coefficient (equity axis).** Same subsection:

```latex
\begin{equation}\label{eq:gini}
G \;=\; 1 - \sum_{k=1}^{n} \bigl( X_{k} - X_{k-1} \bigr)\bigl( Y_{k} + Y_{k-1} \bigr),
\end{equation}
```
$X_k$ = cumulative share of cells, $Y_k$ = cumulative share of the exposure $\times$
vulnerability burden (trapezoidal Lorenz-curve approximation; consistent with panel (d) of
`fig:geomap`).

**Optional (add if space allows; justify inclusion/exclusion in the report):**
- O1: Orientation entropy $H_{o} = -\sum_{i=1}^{18} p_i \ln p_i / \ln 18$ (length-weighted,
  18 bins; cite Boeing 2019, *Applied Network Science*, DOI `10.1007/s41109-019-0189-1` —
  verify then add).
- O2: The standard form of Getis-Ord $G_i^{*}$.
- O3: Silhouette $s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}$ and/or the ARI (cluster-number
  selection + scale stability).
- O4: Direction-coded z-standardisation $z_{ij} = s_j (x_{ij}-\mu_j)/\sigma_j$ (after
  winsorising to [1, 99]).

Do not inflate the equation count: the 8 mandatory ones plus at most 2–3 optional. No need
to write the XGBoost objective (it is handled by citation); the SHAP equation is mandatory
because the mechanism claims rest on it.

---

## TASK 2 — Purge of em-dashes / en-dashes and AI-writing tells

Current inventory (counted by the LEAD): `---` (em-dash) **90 occurrences**, word--word
en-dash **31 occurrences**. Distribution: results 22, discussion 15, background 12,
study_area 10, appendix 8, conclusions 8, methodology 7, introduction 4, titleAbstract 4.

**Rules:**
1. `---` (em-dash) must **disappear entirely** from running prose. Do NOT mechanically
   substitute commas; recast each sentence naturally: colon, parentheses, a separate
   sentence, "that is", "namely", etc. Preserve meaning and emphasis.
2. Word--word en-dash compounds (`fabric--resilience`, `catchment--radius`,
   `exposure--vulnerability`, `morphology--temperature`, `explain $\rightarrow$ optimize`,
   etc.): convert to a plain hyphen (`fabric-resilience`) or reword ("the exposure and
   vulnerability burden"). Collapse the "explain $\rightarrow$ optimize" pattern to a single
   form throughout: recommendation **"explain-then-optimize"** (already used in places).
3. Numeric ranges: in prose, "2014--2024" becomes "2014 to 2024" / "between 2014 and 2024";
   the "400/800\,m" form may stay. **In table cells and refs.bib page ranges, `--` may
   remain** (standard typography; the user's target is AI-tells in prose).
4. The title also contains an en-dash (`Fabric--Resilience`); resolved together with Task 4.
5. Scan for and reduce other AI-writing tells (report before/after counts):
   - Excessive `\emph{}` emphasis (very frequent; cut by at least half, keep only for
     genuine term definitions).
   - The repeated "honest/honestly/candid" family (appears 4+ times): keep one instance,
     vary the rest ("conservative", "cautious", "we do not over-read", ...).
   - Pile-ups of "notably", "crucially", "importantly"; repeated triadic parallel
     constructions.
6. Post-purge verification (grep commands in Section 7) must show zero `---`.

---

## TASK 3 — Third author: Hilmi Evren Erdin (position 3)

Update three files:

1. **`sections/titleAbstract.tex`** — add in third position inside `\author{}`:
   ```latex
   \and Hilmi Evren Erdin\thanks{%TODO-TITLE%, Department of City and Regional
   Planning, Dokuz Eyl\"ul University, \.{I}zmir, T\"urkiye. ORCID %TODO-ORCID%.}
   ```
2. **`title_page.tex`** — add the `\textsuperscript{3}` line, the affiliation block entry,
   the ORCID line, and the **CRediT** entry. Suggested CRediT (subject to user approval;
   flag in the report):
   `Hilmi Evren Erdin: Supervision, Conceptualization, Writing - Review & Editing.`
3. **`sections/declarations.tex`** — add to the "Author contributions" paragraph with the
   same contribution set.

**No fabrication:** leave the ORCID and the academic title (Assoc. Prof. / Prof.) as
`%TODO%` and list them in the report under "Questions for the user". The Department of City
and Regional Planning at Dokuz Eylül University is a reasonable affiliation assumption, but
flag it for confirmation as well.

---

## TASK 4 — Title shortening

Current title (2 lines, 18 words, and it contains an en-dash):
> *Grid-Based Urban Morphometrics for Climate Resilience: Explainable, Pareto-Aware
> Fabric--Resilience Priorities for the İzmir Functional Urban Region*

User request: short and visually clean; "optimization" or "Pareto" may appear. Rules:
target 12 words or fewer, at most one colon, no dash of any kind.

**Candidate list (pick one; justify your choice in 2–3 sentences in the report):**
1. **Explain, then Optimize: Urban Fabric and Climate Adaptation Priorities in İzmir**
   *(LEAD's recommendation — captures the two-stage method and the city in one breath)*
2. Explainable Morphometrics and Pareto Optimization for Climate Adaptation in İzmir
3. Pareto-Aware Climate Adaptation Priorities for Urban Fabric in İzmir
4. Urban Form, Heat and Equity: Multi-Objective Adaptation Priorities for İzmir
5. From Urban Fabric to Adaptation Priorities: An Explainable Multi-Objective Workflow

Update: `titleAbstract.tex` `\title{}`, the title block of `title_page.tex`, and (if any)
headers/PDF metadata. Revisit the keyword list so it does not duplicate words now in the
title (good practice: keywords complement rather than repeat the title).

---

## TASK 5 — Deepening: break the "shallow methods paper" impression

Concrete, bounded upgrades (those requiring no new analysis first):

**5.1 (MANDATORY) Resolve the axis contradiction.** The inconsistency of pre-finding B:
align the list "(heat, pluvial, coastal, access deficit, social vulnerability)" in
`methodology.tex` with the real pipeline: **heat, cooling deficit, access deficit, coastal
exposure, social vulnerability** (see `tab:params`, "Need axes"). Then honestly reconcile
the "three hazards (heat, pluvial, coastal)" narrative in the abstract + introduction +
the proxies subsection: state EXPLICITLY that pluvial exposure is produced as a screening
layer but does not enter the priority axes, and is deferred to future work together with
hydrodynamic validation (add a limitation item). First check whether a pluvial axis
actually exists in `scripts/pilot_11_priority.py`; if it exists and its output is in
`outputs/tables/adaptation_priority.csv`, consider restoring the axis to the text as an
alternative resolution. Report which option you chose, with evidence.

**5.2 (MANDATORY) Research-question-to-answer mapping.** The introduction defines four
research questions, but neither the results nor the conclusions answer them one by one.
Restructure `conclusions.tex` (or the start of the discussion) to close RQ1–RQ4 in order,
each with a one-sentence verdict ("RQ1: yes, the seven strata are sharply differentiated
(Table 2)..." style).

**5.3 (MANDATORY) Policy translation table.** Add a small table to the discussion's policy
subsection: rows = the 7 fabric strata; columns = dominant SHAP mechanism (from panel (b)
of `fig:shap`), priority rank (Table 3), recommended intervention package (roof/yard
greening, albedo, shading, evacuation access, ...). Data from
`outputs/tables/shap_per_stratum_mechanism.csv` + `adaptation_priority.csv`; no new
analysis, just a translation of existing findings into decision language. This table turns
the "method paper" perception into a "decision-support paper" perception.

**5.4 (MANDATORY) Quantitative scenario sentence.** Add at least one numerical
counterfactual statement derived from the SHAP dependence plots
(`fig:explainable-heat-interactions`); e.g. the stratum-level range of the green-cover SHAP
effect is already computed (−0.81 °C in peripheral expansion; +0.40 °C footprint effect in
industrial). Carry these into the discussion in "attributable contrast" language: "moving a
coarse-grain cell's green-cover fraction from its stratum median to the peripheral median
is associated with...". DO NOT produce new numbers; read only from the existing SHAP
outputs (`outputs/tables/shap_*.csv`).

**5.5 (Optional; propose, but state the cost in the report before implementing):**
- A one-paragraph justification or mini-sensitivity note for the exclusion thresholds
  (built fraction 0.10, slope 15%).
- A conceptual comparison paragraph against LCZ (Local Climate Zones): why this is not LCZ,
  what it adds over LCZ (implied in the intro; one explicit paragraph in the discussion
  would be better).
- One sentence quantifying the Landsat 100 m LST vs 250 m cell scale-commensurability
  uncertainty (referencing the PSF panel of S1).

---

## TASK 6 — Figure surgery

Shared rules: new/revised figures must use the style of `scripts/_manuscript_style.py` and
the cartographic language of `raw_morphology_maps` (scale bar, north arrow, coastline,
EPSG:32635). Add production code under `scripts/` as new/revised `make_*.py` and hook it
into `generate_all_figures.py`. Figure data is ready in `outputs/figure_gpkgs/`.

**6.1 Fig `fig:priority-synthesis` (the user's Figure 12) — SPATIALISE.**
Current: (a) fabric-level scatter, (b) cell-level Pareto scatter. Problem: you cannot see
WHERE the 223 frontier cells are, although spatial targeting is the text's main message.
To do: extend to three panels or replace (b):
- (a) fabric-level scatter (keep; may shrink),
- (b) cell-level Pareto scatter (keep),
- **(c) NEW MAP:** all 3,777 cells; dominated cells in light grey, the 223 frontier cells
  filled in their stratum colour + dark outline; coastline; an inset zoom around the bay.
  Data: `figure_12_priority_synthesis.gpkg` (geometry + dominance flag; verify field names
  against `figure_gpkg_manifest.csv`) or the output of `pilot_13_cell_pareto.py`.
Update the caption and the res-priority text in `results.tex` for the new panel (add one
spatial reading sentence such as "frontier cells concentrate along the bay-front..." —
verify the claim from the gpkg before writing it).

**6.2 Fig `fig:flow-sankey` (the user's Figure 13) — REMOVE.**
- Delete the figure environment from `results.tex` and the sentence that anchors it ("The
  transition flow from a-priori fabric strata ... Figure~\ref{fig:flow-sankey},
  illustrating how..."); leave the paragraph flowing smoothly.
- Verify by grep that no `\ref{fig:flow-sankey}` remains.
- Remove `make_fig09_flow_sankey.py` from `generate_all_figures.py` (do not delete the
  file; just drop it from the orchestrator); `flow_sankey.png` may stay on disk.
- The stratum-to-cluster transition information already lives in `tab:cluster-priority` +
  `cluster_vs_stratum.csv`; no information is lost — state this in the report.

**6.3 Fig `fig:topsis-robustness` (the user's Figure 14) — SEMI-SPATIALISE.**
Current: (a) Monte-Carlo rank boxplots (valuable, KEEP), (b) parallel-coordinates plot
(abstract, weak). To do: replace (b) with this map:
- Cell-level entropy-weighted TOPSIS closeness $C_i$ map (continuous colour ramp) with the
  223 frontier cells overlaid as outlines. This builds a visual bridge to Fig 12(c).
  Data: `figure_14_topsis_robustness.gpkg` (if absent, `pilot_11_priority.py` produces the
  cell scores; `cell_priority_top20.csv` for cross-checking).
- Move the entropy-weight box content of the parallel-coordinates panel into the caption
  (no information loss). If you judge the alternative (moving parallel coordinates to the
  supplementary) better, justify it in the report.

**6.4 Supplementary figure order and de-duplication.**
1. **Repair the numbering:** appendix figures take main-counter numbers "Figure 15–18"
   while captions hand-say "S1..S7", and document order is S5,S6,S7,S1,S2,S3,S4. Fix: add
   this block at the top of the appendix and delete ALL hand-written "Supplementary Figure
   S#:" prefixes from captions:
   ```latex
   \renewcommand{\thefigure}{S\arabic{figure}}
   \setcounter{figure}{0}
   \renewcommand{\thetable}{S\arabic{table}}
   \setcounter{table}{0}
   ```
   (Decide whether tables also move to the S-series by checking main-text
   cross-references; `tab:cluster-priority`, `tab:heat-leverage`, `tab:vuln-robust`,
   `tab:params` live in the appendix.) S-numbers then follow document order automatically
   and consistently.
2. **De-duplication (apply at least these two; propose more if you spot them):**
   - `supp_topsis_sensitivity` (S4) panel (c) "strata $C_i$ distributions" largely repeats
     the information of main Fig `fig:topsis-robustness`(a) rank distributions: drop the
     panel or reduce S4 to three panels with a one-sentence caption note.
   - The CV-performance inset inside main Fig `fig:shap` repeats S3
     (`supp_xgb_diagnostics`) verbatim: simplify the inset (a single $R^2$ line) or defer
     to S3.
   - `supp_data_quality` (S1) panel (d), the demographic correlation, is described in one
     sentence in the text; keeping it is defensible — give your opinion in the report
     before touching it.
3. After the figure changes, update the manifest of `export_figure_gpkgs.py` and
   `figure_gpkg_export_report.md` (the number mapping will change).

---

## TASK 7 — Verification and build

After each major task and at the end:

```powershell
cd C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience\paper\manuscript\src
latexmk -pdf -interaction=nonstopmode main.tex   # fallback: pdflatex x2 + bibtex + pdflatex x2
latexmk -pdf -interaction=nonstopmode title_page.tex
```

Checks (include the outputs in the report):
1. `main.log`: `Undefined references`, `Citation ... undefined`, `multiply defined` = ZERO.
2. Em-dash audit: `grep -c -- '---' sections/*.tex` → all zero.
   En-dash audit: `grep -oE '[a-zA-Z]--[a-zA-Z]' sections/*.tex` → empty.
3. `grep -n 'flow-sankey' sections/*.tex main.tex` → empty.
4. `%TODO` markers exist only in the Erdin ORCID/title fields.
5. Run `scripts/check_citations.py` → clean.
6. If figures were regenerated, show via `scripts/report_canonical_numbers.py` that the
   canonical numbers did not change.
7. Visually inspect the new PDF page by page: equation overflows (overfull hbox), figure
   placement, S-numbering, title line breaks.

---

## TASK 8 — Report contract (return to the LEAD)

Write the report to: `docs/revision/WORKER_REPORT_rev2.md`. Mandatory sections:

```markdown
# WORKER REPORT — rev2
## 1. Executive summary (max 10 lines: what was done, what was not, why)
## 2. Task status table
   | Task | Status (DONE/PARTIAL/NOT DONE) | Evidence (file:line / grep output / page no.) |
## 3. Equations added (number, label, host subsection, in-text reference sentence)
## 4. Em-dash/en-dash audit (before/after grep counts, per file)
## 5. Chosen title + rationale + files updated
## 6. Author change (additions made + TODO fields)
## 7. Figure changes (per figure: old state → new state, production script, PNG path,
     caption text; preview paths for the new Fig12(c) and Fig14(b) maps)
## 8. Deepening changes (5.1–5.4 one by one; evidence for the axis-contradiction fix)
## 9. Consistency sweep: ADDITIONAL problems YOU found (beyond the LEAD's list)
## 10. Build evidence (latexmk summary, log warning count, PDF page count, figure count)
## 11. Questions for the user (Erdin ORCID/title/CRediT approval, title approval, etc.)
## 12. Full list of modified files + path of the backup archive
```

**Priority order (under time pressure, follow this order):**
1. Backup + rebuild baseline
2. TASK 1 (equations) and 5.1 (axis contradiction)
3. TASK 3 (author) + TASK 4 (title)
4. TASK 2 (dash purge)
5. TASK 6.2 (delete sankey) → 6.1 → 6.3 → 6.4
6. TASKS 5.2–5.4
7. TASK 7 verification + TASK 8 report

**Definition of done:** the 7 verification checks above are evidenced, the report follows
the contract, the PDF compiles cleanly, the canonical numbers are unchanged, and TODOs
remain only in fields that require user approval.
