# Urban Morphology Research Design

## Recommended Direction

The stronger paper is a detailed urban analytics / morphology study, not a generic resilience index paper.

**Proposed core idea:** compare selected street-based urban tissue samples in the Izmir Gulf or Izmir functional urban region, then evaluate how their morphology, accessibility, microclimate exposure proxies, and resilience indicators differ.

In the paper narrative, PlanX Urban Resilience can be the umbrella, while the analytical chain can use:

- PlanX main: network, space syntax, morphology, microclimate, accessibility;
- PlanX Urban Resilience: heat, social vulnerability, emergency/accessibility, recovery, composite priority;
- optional supporting packages such as Urbanity if external graph enrichment is useful;
- optional UMEP-like microclimate references through PlanX main's embedded microclimate tools.

## Best Case Study Geometry

### Recommended: Izmir Gulf tissue transect

This is the best balance of academic richness and practical feasibility before the abstract deadline.

Possible sample families:

1. Historic / traditional center fabric.
2. Planned grid and high-accessibility urban core.
3. Mid/high-rise apartment block fabric.
4. Industrial or logistics edge.
5. Hillside/incremental residential tissue.
6. Waterfront redevelopment or mixed-use corridor.
7. Peripheral expansion / new development edge.

Each sample can be normalized as:

- 400 m / 800 m walking catchment,
- 500 m x 500 m grid cell,
- street-corridor buffer,
- or neighborhood fragment clipped to a comparable area.

## Measurement Framework

| Dimension | Example indicators | Likely tool source |
|---|---|---|
| Street configuration | integration, choice, NACH/NAIN, centrality, meshedness, orientation entropy | PlanX main |
| Building morphology | coverage, compactness, elongation, tessellation, GSI, FSI, OSR, L | PlanX main |
| Accessibility | service areas, multi-amenity access, nearest facility, OD costs | PlanX main |
| Microclimate proxy | sky view factor, shadow/sun hours, heat island risk grid | PlanX main / Urban Resilience |
| Resilience screening | heat comfort risk, social vulnerability, emergency accessibility, recovery capacity | PlanX Urban Resilience |
| Synthesis | tissue classes, priority score, dominant drivers, hot-spots/outliers | PlanX Urban Resilience / GeoStats if needed |

## Possible Argument

Climate-resilient urban planning often evaluates risk at administrative scales. However, adaptation capacity is also shaped at the scale of street networks and urban tissue. Different fabrics can produce different combinations of shade, openness, density, walkability, emergency access, exposure, and social vulnerability. The study therefore proposes a street-based morphology and resilience workflow for comparing urban tissue samples.

## Why This Is Good for a Student Collaboration

Halil Topcu's urban design master's background can anchor the interpretation:

- reading tissue types,
- selecting representative samples,
- linking quantitative indicators to design morphology,
- translating results into design/planning implications.

The technical PlanX workflow supplies the analytical backbone, while the urban design reading prevents the study from becoming only a software or index exercise.

## Recommended First Abstract Claim

The abstract can state that the study develops a reproducible QGIS workflow for street-based urban tissue comparison and tests it on selected Izmir samples. It can focus on how urban form indicators and resilience indicators jointly reveal adaptation priorities.

## Preferred Title Direction

**Street-Based Urban Tissue Analytics for Climate Resilience: An Open-Source QGIS Workflow in the Izmir Gulf**

Turkish working title:

**Sokak Bazli Kentsel Doku Analitigi ile Iklim Direncliligi: Izmir Korfezi Orneginde Acik Kaynakli Bir QGIS Is Akisi**

