# ICUS 2026 PlanX Urban Resilience Paper

**Project phase:** abstract-first congress preparation  
**Venue:** 11. Kent Arastirmalari Kongresi / ICUS 2026  
**Main theme:** Iklim Degisikligine Direncli Kentler  
**Project root:** `C:\Users\YE\PyCharmMiscProject\icus2026_planx_urban_resilience`  
**Candidate method backbone:** QGIS + PlanX urban analytics ecosystem, narrated through PlanX Urban Resilience  
**Plugin path:** `C:\Users\YE\PyCharmMiscProject\qgis_plugins\planx_urban_resilience`
**Student collaborator:** Halil Topcu, urban design master's student at Izmir Demokrasi University

This folder is structured like the BBTMK workflow, but starts smaller because the immediate target is a 500-750 word abstract. If the abstract is accepted, the same folder can expand into the full-text, slide, QGIS, and reproducibility package workflow.

## Working Position

The strongest direction is not simply "a paper introducing a plugin." A stronger academic framing is:

> An open-source, QGIS-based urban morphology and street-tissue workflow for reading climate-related resilience capacity across contrasting urban fabrics, narrated through PlanX Urban Resilience on a real city case.

This keeps PlanX central while avoiding a purely promotional tone. The method should be transparent enough that reviewers see it as a planning-support and urban-design research workflow, not a black-box software demo.

## Folder Map

```text
icus2026_planx_urban_resilience/
|-- abstracts/                 # abstract outlines, drafts, CMT-ready checks
|-- data/                      # raw/interim/processed inputs and outputs
|-- docs/
|   |-- congress/              # scraped ICUS 2026 briefing
|   |-- methodology/           # PlanX and open-source method notes
|   |-- notes/                 # decisions, open questions
|   |-- submission/            # CMT and format checklist
|   `-- manuscript/            # later full-text track
|-- logs/                      # processing logs and validation notes
|-- outputs/
|   |-- figures/
|   `-- tables/
|-- qgis/
|   `-- styles/
|-- src/                       # optional reproducibility scripts
`-- project_guide.md
```

## Empirical pilot

The journal-track empirical analysis runs in a project-local Python environment
(`.venv`, Python 3.12) over a 250 m grid of the İzmir functional urban region.
**Resume guide and full pipeline status:** [`docs/PILOT_PROGRESS.md`](docs/PILOT_PROGRESS.md).
Data provenance: [`data/01_raw/PROVENANCE.md`](data/01_raw/PROVENANCE.md). Pipeline
scripts: `scripts/pilot_0*.py`.

## Immediate Work

1. Decide the exact case study geography, sample areas, and analysis unit.
2. Freeze the PlanX plugin version and record the algorithm chain.
3. Build a compact abstract argument: problem, aim, method, expected/initial outputs, originality.
4. Prepare Turkish and English title, abstract, and keywords.
5. Submit via CMT before **29 June 2026**.

## Authoring Rule

The congress ethics text is strict about AI-generated content. Treat AI support in this folder as planning, organization, quality control, and critique. The final submitted abstract/full text should be author-owned, verified, and rewritten in the author's own academic voice.
