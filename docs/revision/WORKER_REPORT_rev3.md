# WORKER REPORT — rev3

## 1. Executive summary (max 8 lines)

- DONE: all ten rev3 tasks were completed; no figure or pilot script was run and no file under `outputs/` changed.
- The byline now uses affiliation letters a/b/c-style (actual markers a/b/a), Erdin is Professor, and only his invisible ORCID TODO remains.
- The default title and a single unlabelled 250-word abstract were applied.
- Every heading is a 1–4 word noun phrase; Methodology has five subsections and Discussion has four.
- All nine equations remain intact and now flow grammatically through their host sentences.
- PlanX is represented by one bibliography record; the Crossref-verified Istanbul article is cited twice.
- Both PDFs compile cleanly, all Task 9 greps pass, and all 63 manuscript pages plus the title page passed visual inspection.

## 2. Task status table (Task | DONE/PARTIAL/NOT DONE | evidence file:line / grep)

| Task | Status | Evidence |
|---|---|---|
| 1. Author block | DONE | Lettered authors and affiliations: `sections/titleAbstract.tex:3–9`; title-page a/b/a byline and affiliations: `title_page.tex:18–25`; Professor: `title_page.tex:31`; one invisible TODO: `title_page.tex:38`. Source grep found no `\thanks` and one TODO only. |
| 2. New title | DONE | Default title at `sections/titleAbstract.tex:1` and `title_page.tex:14`; no alternate was annotated. Complementary keywords remain at `titleAbstract.tex:47–49`. |
| 3. Plain abstract | DONE | One unlabelled paragraph at `sections/titleAbstract.tex:19–45`; audit count = 250 words, 1 paragraph, and 0 `Context./Objective./Methods./Findings.` tags. |
| 4. Section architecture | DONE | Final outline in Section 3; Methodology subsection count = 5, Discussion = 4, and every heading is 1–4 words. Final logs contain 0 undefined references and 0 invalid/duplicate destinations. |
| 5. Equation integration | DONE | Nine displays at `methodology.tex:69,80,101,157,217,224,242,255,264`; herald grep count = 0. Quoted lead-ins appear in Section 4. |
| 6. Global prose flow | DONE | Enumerated contribution scaffold replaced at `introduction.tex:65–82`; choppy Results opening merged at `results.tex:4–8`; figure scaffolds recast at `results.tex:23,137`; redundant supplementary-figure roadmap deleted after `appendix.tex:259`. Claims and canonical values were not changed. |
| 7. Single PlanX reference | DONE | `planxgeo|eminoglu2026planxgeostats` grep count = 0; sole record at `refs.bib:809–820`; direct uses at `methodology.tex:8–10` and `declarations.tex:10–15`. |
| 8. Istanbul paper | DONE | Crossref record confirmed DOI `10.1016/j.scs.2026.107190`, volume 138, year 2026, page/article 107190; entry at `refs.bib:825–835`; load-bearing citations at `introduction.tex:36–38` and `discussion.tex:160–163`. |
| 9. Verification | DONE | `main.pdf` and `title_page.pdf` build cleanly; Task 9 counts and output hash are in Section 9. |
| 10. Report | DONE | This file follows the required ten-section contract and records the sole open question in Section 10. |

Backup created before editing: `paper/manuscript/_backup_src_rev3_20260719_034131.tar.gz` (17,236,862 bytes; SHA-256 `8DF2B1436525A004A3F0C809D222EBC3626414DB85C326C769FB39406988993B`). No second rev3 backup was created.

## 3. Final section outline (every section + subsection title, before → after)

The “before” outline is from the backup above; the “after” outline is the compiled source.

| Section | Before | After |
|---|---|---|
| Introduction | Introduction; no subsections | Introduction; no subsections |
| Background | Background and related work | Background |
| Background subsection | Reproducible urban morphometrics and fabric typology | Urban morphometrics |
| Background subsection | Urban form as a control on climate hazard | Climate hazards |
| Background subsection | Accessibility, walkability and the street network | Street networks |
| Background subsection | Social vulnerability, heat and climate justice | Climate justice |
| Background subsection | From composite indices to multi-objective prioritisation | Prioritization |
| Study area | Study area | Study area |
| Study-area subsection | Data and materials | Data sources |
| Methodology | Methodology | Methodology |
| Methodology subsection | Grid construction, exclusion and the full-census analysis set | Analysis grid |
| Methodology subsection | The grid cell and the cross-attribution rule | Cross-attribution |
| Methodology subsection | Morphometric and network indicators | Merged into Cross-attribution |
| Methodology subsection | Climate-resilience proxies and hazards | Merged into Cross-attribution |
| Methodology subsection | Explainable heat model: the “explain” stage | Explainable heat model |
| Methodology subsection | Synthesis: standardisation, dimensionality reduction, clustering | Typology and scale stability |
| Methodology subsection | Scale (grid-resolution) stability | Merged into Typology and scale stability |
| Methodology subsection | Spatial statistics | Spatial prioritization |
| Methodology subsection | Adaptation prioritisation: the “optimize” stage | Merged into Spatial prioritization |
| Methodology subsection | Validation, limitation controls and reproducibility | Unheaded closing reproducibility paragraph |
| Results | Results | Results |
| Results subsection | Morphometric differentiation of fabric | Fabric differentiation |
| Results subsection | Fabric-resilience typology and its scale stability | Typology stability |
| Results subsection | Measured heat and its morphological mechanism | Heat mechanisms |
| Results subsection | Spatial structure and equity | Spatial equity |
| Results subsection | Trade-off-aware adaptation priorities | Adaptation priorities |
| Discussion | Discussion | Discussion |
| Discussion subsection | Mechanisms over labels + Positioning | Mechanisms |
| Discussion subsection | Planning and policy translation | Policy translation |
| Discussion subsection | Limitations | Limitations |
| Discussion subsection | Transferability + Future work | Outlook |
| Conclusions | Conclusions; no subsections | Conclusions; no subsections |
| Declarations | Declarations; paragraph heads only | Declarations; paragraph heads only |
| Appendix section | Data inventory and parameters | Data and parameters |
| Appendix subsection | Algorithm parameters | Parameters |
| Appendix subsection | Reproducibility checklist | Reproducibility |
| Appendix section | Supplementary analyses | Supplementary analyses |
| Appendix subsection | Aggregation dependence of the priority signal | Aggregation dependence |
| Appendix subsection | Modifiable versus fixed heat leverage | Heat leverage |
| Appendix subsection | Robustness of the priority signal to the vulnerability definition | Vulnerability robustness |
| Appendix subsection | Spatial stability of the SHAP heat attributions | SHAP stability |
| Appendix section | Supplementary figures | Supplementary figures |

The five Methodology headings are at `methodology.tex:22,45,139,178,202`; the four Discussion headings are at `discussion.tex:4,51,100,132`. Labels for merged material were retained at their host paragraphs, so existing cross-references resolve to the correct merged subsection.

## 4. Equation integration: the nine rewritten lead-in sentences, quoted

The bracketed `[display]` below marks the unchanged displayed equation and shows how the sentence continues through it.

1. `eq:xattr`, `methodology.tex:67–76`: “The cross-attribution rule maps each tessellation character $c$ onto grid cell $g$ through the area-weighted aggregation [display], where $T(g)$ is the set of tessellation cells intersecting grid cell $g$, $a_{t \cap g}$ is the area of the intersection between tessellation cell $t$ and grid cell $g$, and $x_c(t)$ is the value of character $c$ on tessellation cell $t$.”
2. `eq:servicearea`, `methodology.tex:77–87`: “Reach-based characters instead use the network service area [display], where $E$ is the set of street segments, $v_g$ is the graph node nearest to the centre of cell $g$, and $d_{\mathrm{net}}$ is the edge-length-weighted shortest-path (Dijkstra) distance along the street graph.”
3. `eq:orient`, `methodology.tex:99–107`: “Orientation entropy summarizes street-grid order as the normalized Shannon entropy of segment bearings [citation], [display], where $p_i$ is the length-weighted share of street segments falling in orientation bin $i$.”
4. `eq:shap`, `methodology.tex:154–163`: “For feature $j$, TreeSHAP defines the coalition-weighted marginal contribution [citation] as [display], where $F$ is the feature set and $f_x(S)$ is the conditional expected model output given coalition $S$.”
5. `eq:moran`, `methodology.tex:214–222`: “With row-standardized $k$-nearest-neighbour weights, global spatial autocorrelation is [display], where $w_{ij}$ is a row-standardized $k$-nearest-neighbour weight ($k=8$) and $z_i$ is the deviation of observation $i$ from the mean.”
6. `eq:gini`, `methodology.tex:222–229`: “The trapezoidal Lorenz-curve approximation summarizes equity as [display], where $X_k$ is the cumulative share of cells and $Y_k$ is the cumulative share of the impervious-exposure $\times$ social-vulnerability burden.”
7. `eq:pareto`, `methodology.tex:239–247`: “With all axes coded so that larger values mean greater need, cell $i$ dominates cell $j$ when [display], where $n_k(\cdot)$ denotes a need axis, and cells not dominated under this rule form the priority frontier.”
8. `eq:entropy`, `methodology.tex:252–263`: “For the vector-normalized decision matrix, criterion entropy and its corresponding weight are [display], and the same weighted matrix gives each cell's relative closeness to the ideal solution...”
9. `eq:topsis`, `methodology.tex:262–269`: “...the same weighted matrix gives each cell's relative closeness to the ideal solution, [display], where $v_k^{+}$ and $v_k^{-}$ are the ideal and anti-ideal points.”

The exact Task 9 herald grep (`given by Equation|according to Equation|in Equation~\eqref{eq:[a-z]*}:`) returned 0 lines; all nine labels remain present.

## 5. Author block: final byline + affiliation lines as compiled

Compiled main-manuscript byline:

> Yusuf Eminoğluᵃ, Halil Topçuᵇ, and Hilmi Evren Erdinᵃ

Compiled affiliations and correspondence note:

> ᵃ Department of City and Regional Planning, Dokuz Eylül University, İzmir, Türkiye  
> ᵇ Graduate School of Natural and Applied Sciences, Urban Design Program, İzmir Demokrasi University, İzmir, Türkiye  
> Corresponding author: yusuf.eminoglu@deu.edu.tr

The standalone title page repeats the a/b/a byline (`title_page.tex:18–20`), gives the two affiliation lines (`title_page.tex:24–25`), and places all personal details below them: Yusuf Eminoğlu is Research Assistant and PhD Candidate, Halil Topçu is Master's Student, and Hilmi Evren Erdin is Professor (`title_page.tex:29–31`). The correspondence note has no byline footnote symbol. `%TODO-ORCID% Hilmi Evren Erdin ORCID pending.` is a single source comment at `title_page.tex:38` and produces no visible “ORCID” fragment. CRediT remains unchanged at `title_page.tex:43–45`.

## 6. Title applied (+ note if the user annotated an alternate)

Applied the unannotated DEFAULT title:

> Urban Fabric and Climate Adaptation Priorities in İzmir

It appears at `sections/titleAbstract.tex:1` and `title_page.tex:14`. No alternate was annotated before execution. The keywords at `titleAbstract.tex:47–49` complement the title with methods and measures rather than repeating its main phrase.

## 7. PlanX unification evidence (greps) + declarations wording

- `rg 'planxgeo|eminoglu2026planxgeostats' sections mypreamble.sty refs.bib main.tex` → 0 lines.
- `eminoglu2026planxgeostats` and its BibTeX block were removed; no `\planxgeo` macro remains.
- The sole PlanX bibliography record is `eminoglu2026planxresilience` at `refs.bib:809–820`, DOI `10.5281/zenodo.20753148`.
- PlanX: Urban Resilience is cited directly at `methodology.tex:8–10` and `declarations.tex:10–12`; GeoStats is named as a module and its repository remains availability information only.

Final declarations wording (`declarations.tex:10–19`):

> “The analysis uses PlanX: Urban Resilience v1.25.0 [citation], archived on Zenodo at https://doi.org/10.5281/zenodo.20753148, with source code at https://github.com/YusufEminoglu/planx_urban_resilience. Source for the GeoStats module is available at https://github.com/YusufEminoglu/planx_geostats. The full analysis code and derived outputs are openly available in a version-controlled repository, and all inputs are open or openly licensed...”

The citation checker reports 99 cited keys, 99 bibliography entries, 0 undefined and 0 unused.

## 8. Istanbul citation: Crossref-verified DOI + the 2–3 host sentences, quoted

Crossref was queried before editing at the work-order endpoint and then by DOI. Its record confirms: Yusuf Eminoğlu and Hüseyin Murat Çelik; “Diagnosing urban heat vulnerability through multiscale spatial modelling: Evidence from Istanbul for climate-resilient cities”; *Sustainable Cities and Society*; volume 138; March 2026; page/article 107190; Elsevier BV; DOI `10.1016/j.scs.2026.107190`. The house-style entry is `eminoglu2026Diagnosing` at `refs.bib:825–835`.

Introduction host (`introduction.tex:34–39`):

> “Heat-vulnerability indices, even excellent open, transferable and multi-hazard ones, are typically resolved at the neighbourhood or census scale and are not mechanistically tied to morphology [citations]. Multiscale spatial modelling in Istanbul further shows that the diagnosis of heat vulnerability changes with analytical scale and spatial specification [citation].”

Discussion host (`discussion.tex:159–163`):

> “Third, multiscale geographically weighted regression (MGWR) will be introduced to capture local non-stationarity in the heat-morphology relationship, extending the multiscale Istanbul evidence base with spatially varying coefficients [citations].”

The key occurs exactly twice in manuscript prose and nowhere in the abstract.

## 9. Build evidence (log counts, page count) + confirmation outputs/ untouched

Build commands executed from `paper/manuscript/src`:

- `latexmk -pdf -interaction=nonstopmode main.tex`
- `latexmk -pdf -interaction=nonstopmode title_page.tex`

Final `main.log` + `title_page.log` counts: undefined references 0; undefined citations 0; multiply-defined labels 0; duplicate destinations 0; overfull boxes 0; LaTeX warnings 0; natbib warnings 0. `main.pdf` is 63 A4 pages and 17,929,024 bytes; `title_page.pdf` is 1 A4 page and 52,074 bytes.

Task 9 source checks:

- Every `sections/*.tex` file: `---` = 0 and `[A-Za-z]--[A-Za-z]` = 0.
- Abstract labels = 0; abstract = 250 words in one paragraph.
- PlanX GeoStats citation/macro/key hits = 0.
- Equation-herald hits = 0; equation displays = 9.
- TODO hits = 1, the Erdin ORCID source comment.
- Citation checker = 99/99, 0 undefined, 0 unused.

The PDF skill workflow rendered all 63 current manuscript pages at 96 dpi to `tmp/pdfs/rev3_visual_qa/page-*.png`, generated four contact sheets, and rendered the standalone title page at 144 dpi. Page-by-page inspection found no clipping, overlap, broken glyph, heading defect, affiliation-marker error, visible ORCID placeholder, or equation-flow problem.

Before editing, `outputs/` contained 60 files with aggregate content digest `04ad6b7deac174168533195c21962bb14c6451808d13e3ee068605101881da97`. The final audit reports the same 60 files and the same digest (`baseline_match=True`). No file under `outputs/` changed, and no `pilot_*.py`, figure, export, or generation script was run.

## 10. Open questions (Erdin ORCID; anything ambiguous you resolved and how)

1. **Open:** please supply Hilmi Evren Erdin's ORCID. It is the only remaining TODO and is invisible in both PDFs.
2. **Resolved:** no alternate title was annotated, so the Task 2 DEFAULT was applied.
3. **Resolved:** Crossref gives the second author's full name as Hüseyin Murat Çelik, so the bibliography uses that verified form rather than the abbreviated wording in the request.
4. **Resolved:** “single PlanX reference” was implemented as one PlanX bibliography record (`eminoglu2026planxresilience`); the GeoStats repository remains an uncited availability URL, as Task 7 permits.

No task is PARTIAL or NOT DONE.
