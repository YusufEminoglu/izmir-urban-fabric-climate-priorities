# ICUS 2026 Project Guide

**Working title family:** Acik Kaynak QGIS Tabanli Kentsel Direnclilik Taramasi  
**Current venue:** 11. Kent Arastirmalari Kongresi, Ankara, 12-14 October 2026  
**Scrape date:** 13 June 2026  
**Abstract deadline:** 29 June 2026  
**Submission mode:** CMT, abstract-first  
**Working CRS:** to be decided after the case city is frozen; for Izmir, likely `EPSG:32635`.
**Current PlanX Urban Resilience version observed locally:** `1.25.0`
**Current PlanX main version observed locally:** `2.5.0`
**Student collaborator:** Halil Topcu, urban design master's student at Izmir Demokrasi University
**Author plan:** Yusuf Eminoğlu first author; Halil Topçu second author and planned congress presenter.

## 1. Strategic Publication Logic

ICUS 2026 is a good fit because the congress theme is climate-change-resilient cities, with subthemes covering urban vulnerability, spatial justice, local governance, urban policy, green infrastructure, risk, and data-informed decision-making.

The most defensible publication angle is:

1. **Congress abstract track:** concise, theme-aligned, 500-750 words, no figures/tables/references in the abstract text.
2. **Method demonstration track:** QGIS + PlanX Urban Resilience as an open-source, reproducible workflow, with transparent algorithm parameters and validation notes.
3. **Later journal track:** no full text will be submitted to the congress; the expanded article will be developed separately for a later journal submission.

## 1.1 Author and Presenter Metadata

| Role | Name | Email | ORCID | Affiliation |
|---|---|---|---|---|
| First author | Yusuf Eminoğlu | yusuf.eminoglu@deu.edu.tr | https://orcid.org/0009-0005-6000-2934 | Research Assistant and PhD Candidate, Department of City and Regional Planning, Dokuz Eylül University, İzmir, Türkiye |
| Second author / presenter | Halil Topçu | halil.topcu2001@hotmail.com | https://orcid.org/0009-0009-3366-179X | Master's Student, İzmir Demokrasi University, Graduate School of Natural and Applied Sciences, Urban Design Program |

## 2. Recommended Paper Framing

### Preferred framing

**Urban morphology and street-tissue analytics for climate-resilient urban design: an open-source QGIS workflow narrated through PlanX Urban Resilience.**

Why this is strong:

- It matches the congress theme directly.
- It foregrounds open science and local government usability.
- It lets the PlanX ecosystem become evidence of method reproducibility instead of the object of praise.
- It can connect street network configuration, built form, tissue samples, microclimate proxies, accessibility, and planning action.
- It gives Halil's urban design background a clear research object: urban tissue, street-space morphology, and sample-based design interpretation.

### Risky framing to avoid

Do not frame the abstract as only "we developed a plugin." Reviewers may see that as software promotion unless there is a clear urban research question, case study, or planning contribution.

## 3. Candidate Research Questions

1. How do different street-based urban tissues in the Izmir Gulf or Izmir functional urban region vary in morphology, accessibility, microclimate exposure proxies, and resilience capacity?
2. Can open-source QGIS workflows classify urban fabric samples through combined street-network, building-form, density, and resilience indicators?
3. Which tissue types produce higher adaptation priority when morphological compactness, network centrality, heat exposure, access, and vulnerability are evaluated together?

## 4. Candidate Case and Unit Choices

### Option A: Izmir case

Best fit if we want continuity with the BBTMK data environment and existing Izmir layers. This likely gives the fastest path to a serious abstract and later full paper.

Potential analysis unit:

- street-corridor buffers,
- 400 m / 800 m walkable catchments,
- 250 m or 500 m morphology grids,
- selected urban-tissue samples around Izmir Gulf,
- neighborhood / planning units for policy translation.

### Option A1: Izmir Gulf tissue transect

Recommended first choice. Sample contrasting tissues along the Gulf: historic core, planned grid, apartment block fabric, industrial/logistics edge, hillside informal or incremental tissue, waterfront redevelopment, and peripheral expansion. This gives a strong urban design narrative and a manageable analysis surface.

### Option A2: Izmir functional urban region

Stronger for regional urban analytics, but larger and more data demanding. Useful if the paper wants to compare center, corridor, peri-urban, and satellite settlement morphologies.

### Option B: Ankara case

This may align symbolically with the congress location, but data preparation would probably be slower unless clean layers are already available.

### Option C: Synthetic + real mini-case

Useful for demonstrating replicability, but academically weaker unless paired with a real policy-relevant geography.

## 5. PlanX-Centered Method Chain

Recommended chain for an abstract-level study:

1. Build street-based sample polygons and core open data inventory.
2. Run selected PlanX main modules:
   - Prepare Network
   - Space Syntax / Segment Angular Analysis
   - Network Centrality
   - Building Form Metrics
   - Morphological Tessellation
   - Spacematrix Density
   - Street Network Morphology
   - Multi-Amenity Access Score
   - Heat Island Risk Grid / Sky View Factor if DSM inputs are usable
3. Run selected PlanX Urban Resilience modules:
   - Urban Heat Comfort Risk
   - Social Vulnerability Index
   - Emergency Accessibility / Network Accessibility
   - Recovery Capacity Index
   - Multi-Hazard Composite Index
   - Equity-Adjusted Adaptation Priority
   - Hot-Spot / LISA cluster statistics, if the data supports it
4. Join indicators to samples or planning units.
5. Cluster/classify urban tissue types.
6. Produce adaptation-priority classes, dominant morphological drivers, and design/planning implications.
7. Validate outputs through parameter logs, sensitivity checks, and selected independent descriptive checks.

## 6. Evidence Standard

For acceptance, the abstract can describe the workflow and expected outputs, but the later full paper should include:

- exact plugin version and QGIS version,
- input data table with sources and dates,
- algorithm parameter table,
- uncertainty and screening-model limitations,
- sensitivity analysis for weights and thresholds,
- QGIS project and exported layers,
- reproducible logs in `logs/`.

## 7. Ethics and Writing Rule

The congress page includes a strict AI-content warning under plagiarism/ethics. Therefore:

- AI can help organize, critique, translate alternatives, and check compliance.
- The final abstract/full text must be rewritten, verified, and owned by the author.
- Do not submit unreviewed AI-generated prose.
- Preserve notes that distinguish planning support from final authorial text.
