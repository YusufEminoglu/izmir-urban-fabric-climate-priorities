# WORK ORDER — ICUS2026 Manuscript Revision (rev3)

> **Role split:** Written by the LEAD agent after auditing rev2. You are the WORKER agent.
> rev2 is complete and audited (`docs/revision/LIDER_DENETIM_rev2.md`). rev3 is a
> **text-and-style revision driven by direct author feedback**. Execute every task, then
> report per Section 10. The LEAD will audit against the files.

---

## 0. Scope, environment and hard rules

Working directory: `C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience\paper\manuscript\src\`
(`main.tex` + `sections/*.tex` + `title_page.tex` + `refs.bib` + `mypreamble.sty`).

**This round is text/bibliography/front-matter only.**

1. **DO NOT regenerate any figure and DO NOT run any `pilot_*.py` or
   `generate_all_figures.py`.** Rev2 audit found that rerunning the SHAP script refits the
   model and drifts frozen values; everything was restored from the 2 July archives. All
   PNGs, GPKGs and `outputs/tables/*.csv` are now canonical. Hands off.
2. All canonical numbers remain frozen (N=3,777; ARI=0.38; Gini=0.26; R2 0.09/0.27; the
   223-cell frontier; every table value; the SHAP values −0.81, +0.40, −1.84, +0.32,
   −0.29, −0.20, 1.21 now in the text).
3. No em-dashes or word-to-word en-dashes may re-enter the prose; do not reintroduce the
   purged AI-tells; keep the "-ize" spelling family.
4. New citations only with Crossref-verified DOI (Task 8 specifies the one to add).
5. Back up before editing: `paper/manuscript/_backup_src_rev3_YYYYMMDD_HHMMSS.tar.gz`.
6. Rebuild `main.tex` and `title_page.tex` after the changes; zero undefined references,
   zero overfull boxes, `scripts/check_citations.py` clean (0 undefined, 0 unused).

**The author's core criticism, which governs every task below:** the manuscript reads as
fragmented and formulaic; too many headings, labelled abstract blocks, "Equation (n)"
announcements, and footnote-symbol scaffolding. The goal of rev3 is **organic, flowing,
economical academic prose**. When in doubt, merge, shorten, and let sentences do the work
that labels currently do.

---

## TASK 1 — Author block: letters, not symbols; Erdin is Prof. Dr.

The author has confirmed: **Hilmi Evren Erdin is Prof. Dr.** (Professor). His ORCID is
still unknown.

1. Replace the `\thanks{}` footnote-symbol notation in `sections/titleAbstract.tex` with
   **superscript-letter affiliation notation (a, b, c style)**. Recommended: load
   `authblk` in `mypreamble.sty` and write:
   - Yusuf Eminoğlu (a, corresponding), Halil Topçu (b), Hilmi Evren Erdin (a) — note
     Eminoğlu and Erdin share affiliation (a): Department of City and Regional Planning,
     Dokuz Eylül University, İzmir, Türkiye; (b) İzmir Demokrasi University, Graduate
     School of Natural and Applied Sciences, Urban Design Program, İzmir, Türkiye.
   - Corresponding-author email as a single asterisked line or a note under the
     affiliations; **no footnote symbols (daggers, double asterisks) in the byline.**
2. The byline itself carries only names + letters. Personal detail (Research Assistant
   and PhD Candidate; Master's Student; **Professor** for Erdin; ORCIDs; email) lives on
   `title_page.tex`, which must also switch from numeric superscripts 1/2/3 to the same
   letter notation for consistency.
3. Fill Erdin's `%TODO-TITLE%` with Professor. Keep a single `%TODO-ORCID%` comment (a
   LaTeX comment, invisible in the PDF — the rendered page must NOT show a dangling
   "ORCID ." fragment) until the user supplies the iD; list it as the one open question.
4. CRediT stays as approved: Erdin: Supervision, Conceptualization, Writing - Review \&
   Editing.

## TASK 2 — New title (author rejected the rev2 title)

The author did not like "Explain, then Optimize: Urban Fabric and Climate Adaptation
Priorities in İzmir". Replace it with the DEFAULT below unless the user annotates
otherwise before you run; keep it plain, classic, no dash, at most one colon:

- **DEFAULT: Urban Fabric and Climate Adaptation Priorities in İzmir**
- Alt 1: Morphometric Screening of Climate Adaptation Priorities in İzmir
- Alt 2: Linking Urban Morphometrics to Climate Adaptation Priorities in İzmir
- Alt 3: Explainable Multi-Objective Screening of Urban Climate Adaptation in İzmir
- Alt 4: Urban Form and Equitable Climate Adaptation in the İzmir Urban Region

Update `titleAbstract.tex` and `title_page.tex`; re-check that keywords complement the
final title.

## TASK 3 — Plain abstract

Rewrite the abstract as **one continuous, unlabelled paragraph** (target 200–250 words).
Delete the bold "Context. / Objective. / Methods. / Findings." scaffolding entirely and
let the same content flow as ordinary prose in that natural order. Keep all numbers
exactly as they are; keep the keyword line.

## TASK 4 — Section architecture: fewer, shorter headings

The author finds the manuscript over-partitioned ("çok parçalı, çok başlıklı, derli toplu
değil"). Two rules:

**4a. Headings are short noun phrases, never sentence-like.** Target 1–4 words. Examples
of the required conversions (apply the same spirit everywhere, including any heading that
still carries a dash-replacement or an "the X stage" appendage):
- "Grid construction, exclusion and the full-census analysis set" → "Analysis grid"
- "The grid cell and the cross-attribution rule" → "Cross-attribution"
- "Morphometric and network indicators" → "Indicators"
- "Climate-resilience proxies and hazards" → "Hazard proxies"
- "Explainable heat model (the explain stage)" → "Explainable heat model"
- "Synthesis: standardisation, dimensionality reduction, clustering" → "Typology"
- "Scale (grid-resolution) stability" → "Scale stability"
- "Adaptation prioritisation (the optimize stage)" → "Prioritization"
- "Validation, limitation controls and reproducibility" → "Reproducibility"
- Results: "Morphometric differentiation of fabric" → "Fabric differentiation";
  "Fabric–resilience typology and its scale stability" → "Typology and scale stability";
  "Measured heat and its morphological mechanism" → "Heat mechanisms";
  "Trade-off-aware adaptation priorities" → "Adaptation priorities".
- Discussion: "Planning and policy translation" → "Policy translation".

**4b. Merge subsections so each section has few, substantial parts.** Guidance (use
judgement; report the final outline):
- Methodology currently has ~9 subsections → merge to **5 at most**, e.g.: Analysis grid;
  Cross-attribution and indicators; Explainable heat model; Typology and scale stability;
  Spatial statistics and prioritization; plus a short closing Reproducibility paragraph
  that may live unheaded at the end of the section.
- Discussion currently has 6 → merge to **4 at most** (fold Transferability and Future
  work into one closing subsection, e.g. "Outlook").
- Never leave a subsection of a single short paragraph; fold it into a neighbour.
- All `\ref{sec:...}` cross-references must be repaired after merging.

## TASK 5 — Organic equation integration (kill the "Equation (n)" announcements)

The author finds the pattern "X is given by Equation (5):" artificial. Keep all nine
equations and their labels, but weave each into the sentence grammar so the display is a
natural continuation of the prose. Pattern to eliminate (BEFORE) and target style (AFTER):

- BEFORE: "dominance is defined according to Equation~\eqref{eq:pareto}: \begin{equation}...\end{equation}"
- AFTER: "a cell $i$ dominates a cell $j$ when it is at least as needy on every axis and
  strictly needier on at least one,
  \begin{equation} ... \end{equation}
  and the cells that no other cell dominates form the priority frontier."

Rules: the sentence must read grammatically **through** the display (punctuate the
equation as part of the sentence, with a comma or nothing before it and the continuation
after it); the word "Equation" may appear only in genuine later cross-references (e.g.
"the operator in Eq.~\eqref{eq:xattr} also produces..."), not as a herald immediately
before its own display. Apply to all nine equations.

## TASK 6 — Global prose pass: "derli toplu"

One editorial pass over the whole manuscript for flow, applying the author's criticism:
- Merge choppy short paragraphs where they treat one idea.
- Remove residual scaffolding phrases ("This section reports...", "The following
  subsection describes...") where the structure is self-evident; keep at most one
  roadmap sentence at the end of the introduction.
- Keep terminology, claims and all numbers untouched. This is a style pass, not a
  content pass. Do not increase the word count; aim to reduce it slightly.

## TASK 7 — Single PlanX reference

The toolchain must be carried by **one citation only**: `eminoglu2026planxresilience`
(PlanX: Urban Resilience, Zenodo DOI 10.5281/zenodo.20753148 — already in the bib).

1. Remove every `\planxgeo` / `eminoglu2026planxgeostats` citation from the text
   (methodology, introduction contribution (iv), anywhere else grep finds it). The
   GeoStats functionality may still be *named* in prose ("the spatial statistics are run
   in the PlanX suite's GeoStats module") but without a separate citation.
2. Remove the now-unused `\planxgeo` macro from `mypreamble.sty` and the
   `eminoglu2026planxgeostats` entry from `refs.bib` (the citation checker must stay at
   0 unused).
3. In `declarations.tex`, keep the software-availability paragraph but restructure it so
   PlanX: Urban Resilience (with its Zenodo DOI) is the cited software; the GeoStats
   repository URL may remain as availability information only. Simplify the parenthetical
   pile-up while you are there.

## TASK 8 — New in-text citation (the author's Istanbul paper)

Add and cite: Eminoğlu, Y. and Çelik, H.M. (2026), "Diagnosing Urban Heat Vulnerability
through Multiscale Spatial Modelling: Evidence from Istanbul for Climate-Resilient
Cities", *Sustainable Cities and Society*, art. 107190, Elsevier.

1. **Verify on Crossref first** (mandatory): query
   `https://api.crossref.org/works?query.bibliographic=Diagnosing+Urban+Heat+Vulnerability+Multiscale+Istanbul&rows=3`
   and confirm title/authors/journal; take the DOI, volume and year exactly from the
   Crossref record (likely a 10.1016/j.scs... DOI). If Crossref cannot confirm it, do NOT
   add the entry; flag it in the report instead.
2. Bib key: `eminoglu2026Diagnosing` (house style); fields from Crossref, not from memory.
3. Cite it **organically, in 2 (max 3) load-bearing places**, not decoratively:
   - Introduction, the heat-vulnerability-indices passage (alongside
     `turner2025Guhvi`/`iqbal2025HeatStress`): as evidence that heat vulnerability is
     scale-dependent and multiscale spatial modelling changes the diagnosis.
   - Discussion, the future-work sentence on multiscale geographically weighted
     regression / local non-stationarity: as the companion Istanbul evidence base.
   - Optionally in Background where vulnerability mapping literature is set up.
   No citation in the abstract.

## TASK 9 — Verification

```powershell
cd C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience\paper\manuscript\src
latexmk -pdf -interaction=nonstopmode main.tex
latexmk -pdf -interaction=nonstopmode title_page.tex
```
- Logs: 0 undefined, 0 multiply defined, 0 overfull.
- `grep -c -- '---' sections/*.tex` all zero; `grep -oE '[a-zA-Z]--[a-zA-Z]' sections/*.tex` empty.
- `grep -n 'Context\.\|Objective\.\|Methods\.\|Findings\.' sections/titleAbstract.tex` empty.
- `grep -n 'planxgeo' sections/*.tex mypreamble.sty refs.bib main.tex` empty.
- `grep -n 'given by Equation\|according to Equation\|in Equation~\\eqref{eq:[a-z]*}:'` style
  audit: no herald pattern immediately before a display.
- `scripts/check_citations.py`: 0 undefined, 0 unused; the new Istanbul entry cited.
- Confirm no file under `outputs/` changed (figures/tables untouched this round).
- Page-by-page visual check of the new PDF (byline letters, plain abstract, heading
  lengths, equation flow).

## TASK 10 — Report contract

Write `docs/revision/WORKER_REPORT_rev3.md`:

```markdown
# WORKER REPORT — rev3
## 1. Executive summary (max 8 lines)
## 2. Task status table (Task | DONE/PARTIAL/NOT DONE | evidence file:line / grep)
## 3. Final section outline (every section + subsection title, before → after)
## 4. Equation integration: the nine rewritten lead-in sentences, quoted
## 5. Author block: final byline + affiliation lines as compiled
## 6. Title applied (+ note if the user annotated an alternate)
## 7. PlanX unification evidence (greps) + declarations wording
## 8. Istanbul citation: Crossref-verified DOI + the 2–3 host sentences, quoted
## 9. Build evidence (log counts, page count) + confirmation outputs/ untouched
## 10. Open questions (Erdin ORCID; anything ambiguous you resolved and how)
```

**Definition of done:** every Task 9 check evidenced; report follows the contract; PDF
compiles clean; `outputs/` untouched; the only open TODO is Erdin's ORCID.
