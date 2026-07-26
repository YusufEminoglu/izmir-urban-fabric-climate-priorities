# SCS submission checklist — Grid-Based Urban Morphometrics (İzmir, full census)

_Target: Sustainable Cities and Society (Elsevier). State as of 2026-06-24 (v7)._

## Ready (in repo)
- [x] Manuscript PDF — `paper/manuscript/src/main.pdf` (55 pp, **0 undefined citations/refs**, full census N=3,777, network service areas, k=4 typology).
- [x] Reference integrity — `check_citations.py`: 97 cite keys = 97 bib entries, 0 undefined / 0 unused. All Crossref-verified.
- [x] All figures regenerated from authoritative CSVs (`generate_all_figures.py`); figure scripts are k-robust; `make_fig05` reads silhouette curves from CSV (no hardcoded stats).
- [x] Highlights — `paper/highlights.txt` (5 bullets, each ≤ 85 chars).
- [x] Cover letter — `paper/cover_letter.md` (includes the SAM3/PFI sibling-study disclosure).
- [x] Graphical abstract — `outputs/figures/graphical_abstract.png`.
- [x] CRediT author contributions, competing-interest (plugin developer), **generative-AI declaration**, data/code availability — `sections/declarations.tex`.
- [x] Data & parameter inventory (Table 1 + appendix parameter table) synced to the census/network run.
- [x] Canonical numbers reproducible — `scripts/report_canonical_numbers.py` re-derives every headline value from the processed CSVs.

## Author tasks before upload (cannot/should not be automated)
- [ ] **Read, verify and own the full prose** (congress AI-ethics + good practice). AI assisted drafting; the author is responsible for the content.
- [ ] **<20% similarity check** (Turnitin/iThenticate) on the manuscript and the congress abstract.
- [ ] Freeze the **7 fabric strata** with planning documents + H. Topçu (waterfront over-capture already fixed); if changed, rerun `pilot_03`→`pilot_14` and re-sync.
- [ ] Mint **Zenodo DOIs** for the two PlanX plugins and add `doi=` to the `@misc` refs.
- [ ] Funding statement (currently "None declared") + acknowledgements.
- [ ] Provide the related SAM3/PFI manuscript to the editor if requested (disclosed in the cover letter).
- [ ] Suggested reviewers / preferred-exclusions list (journal form).

## Optional strengthening (future work, honestly deferred in the text)
- Seasonal/diurnal LST split (needs new GEE winter/night scenes).
- Pixel-scale SHAP; MGWR for local non-stationarity.

## Build
`latexmk -cd -pdf paper/manuscript/src/main.tex` (Strawberry Perl + MiKTeX). Congress PDF + CMT guide:
`.venv/Scripts/python.exe scripts/build_icus2026_submission_ready_pdf.py` then `..._cmt_submission_guide.py`.
