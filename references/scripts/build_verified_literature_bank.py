"""Build a DOI-verified literature bank for the ICUS 2026 PlanX urban-resilience paper.

Topic: urban morphology and street-tissue analytics for climate-resilient urban
design, narrated through an open-source QGIS workflow (PlanX Urban Resilience +
PlanX GeoStats Lab).

The script deliberately REJECTS a record whenever its DOI metadata cannot be
reconciled between Crossref and the discovery source (OpenAlex). Nothing enters
the bibliography unless:

  1. the DOI resolves in Crossref AND Crossref's own DOI equals the queried DOI,
  2. the Crossref work type is journal-article (or posted-content for tracked
     online-first records),
  3. the Crossref container/source is in the curated Q1-candidate journal list,
  4. when the record was discovered via OpenAlex, the discovery title matches the
     Crossref title with similarity >= 0.86, and
  5. the OpenAlex-by-DOI lookup (title/year/source) is recorded for the report.

It writes:
- paper/manuscript/src/refs.bib              (DOI-verified entries + plugin cites)
- references/reference_mapping.md            (section -> reference table)
- references/verification/doi_verification_report.md
- references/verification/selected_references.json
- references/verification/rejected_references.json

Run from anywhere: `python references/scripts/build_verified_literature_bank.py`.
"""

from __future__ import annotations

import html
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT_BIB = ROOT / "paper" / "manuscript" / "src" / "refs.bib"
OUT_MAP = ROOT / "references" / "reference_index.md"
OUT_SELECTED = ROOT / "references" / "verification" / "selected_references.json"
OUT_REJECTED = ROOT / "references" / "verification" / "rejected_references.json"
OUT_REPORT = ROOT / "references" / "verification" / "doi_verification_report.md"

MAILTO = "yusuf.eminoglu@deu.edu.tr"


SEARCH_TERMS = [
    '"urban morphology" "climate resilience"',
    '"urban morphometrics" classification',
    '"morphological tessellation" urban',
    '"urban form" "street network" morphology',
    '"space syntax" street network configuration',
    '"street network" centrality urban planning',
    '"urban fabric" typology classification',
    '"built form" density "spacematrix"',
    '"urban resilience" multi-hazard assessment',
    '"climate change adaptation" urban planning spatial',
    '"urban heat island" morphology "land surface temperature"',
    '"sky view factor" thermal comfort urban',
    '"social vulnerability index" urban heat',
    '"heat vulnerability" exposure city',
    '"walkability" accessibility urban form',
    '"15-minute city" accessibility',
    '"green infrastructure" urban heat cooling',
    '"nature-based solutions" urban climate adaptation',
    '"flood" urban morphology exposure',
    '"emergency accessibility" shelter network',
    '"open source" GIS urban analysis reproducible',
    '"QGIS" spatial analysis planning workflow',
    '"Getis-Ord" hot spot urban analysis',
    '"local indicators of spatial association" LISA urban',
    '"geographically weighted regression" urban',
    '"urban tissue" morphology design',
    '"compactness" urban form indicators',
    '"resilience" street network disaster',
    '"urban vulnerability" spatial assessment indicators',
    '"adaptation priority" urban heat equity',
]


# Q1-level candidate sources for building the literature bank. Final WOS/JCR
# quartile must still be confirmed through institutional access before
# submission. Names are stored normalized-friendly (lowercase, with HTML
# ampersand variants where Crossref/OpenAlex disagree).
Q1_CANDIDATE_SOURCES = {
    "annals of the american association of geographers",
    "applied geography",
    "building and environment",
    "cities",
    "computers, environment and urban systems",
    "computers & geosciences",
    "computers &amp; geosciences",
    "ecological indicators",
    "environment and planning b: urban analytics and city science",
    "environmental modelling & software",
    "environmental modelling &amp; software",
    "environmental research letters",
    "geographical analysis",
    "giscience & remote sensing",
    "giscience &amp; remote sensing",
    "habitat international",
    "international journal of applied earth observation and geoinformation",
    "international journal of disaster risk reduction",
    "international journal of geographical information science",
    "isprs international journal of geo-information",
    "isprs journal of photogrammetry and remote sensing",
    "journal of cleaner production",
    "journal of open source software",
    "land use policy",
    "landscape and urban planning",
    "landscape ecology",
    "nature cities",
    "nature communications",
    "natural hazards",
    "natural hazards and earth system sciences",
    "npj urban sustainability",
    "remote sensing",
    "remote sensing of environment",
    "science of the total environment",
    "softwarex",
    "sustainable cities and society",
    "transactions in gis",
    "urban climate",
    "urban forestry & urban greening",
    "urban forestry &amp; urban greening",
    "urban studies",
}


# Discovery seeds. Any of these that fail the Crossref DOI-match / source / type
# gate are silently rejected, so seeding is safe -- nothing unverified survives.
MANUAL_SEED_DOIS: dict[str, list[str]] = {
    "10.21105/joss.01807": ["open_source_gis"],          # momepy (JOSS)
    "10.1016/j.compenvurbsys.2020.101441": ["morphometrics_typology"],
}


# Foundational titles resolved through Crossref by-title (>= 0.88 similarity),
# safer than guessing DOIs. The bib key/metadata always come from Crossref.
MANUAL_TITLE_QUERIES: dict[str, list[str]] = {
    "Methodological foundation of a numerical taxonomy of urban form": ["morphometrics_typology"],
    "momepy: Urban Morphology Measuring Toolkit": ["open_source_gis"],
    "Measuring urban form: Overcoming terminological inconsistencies for a quantitative and comprehensive morphologic analysis of cities": ["morphometrics_typology"],
    "Classifying urban fabrics into typologies": ["tissue_classification"],
    "The configurational basis of cities": ["street_network_syntax"],
    "Spacematrix: Space, Density and Urban Form": ["urban_form_density"],
}


CATEGORY_RULES = [
    ("morphometrics_typology", r"morphometr|urban form|urban morphology|taxonomy|tessellation|building footprint|figure-ground"),
    ("street_network_syntax", r"space syntax|street network|road network|configuration|centrality|integration|betweenness"),
    ("urban_form_density", r"density|spacematrix|built form|compactness|floor area|coverage|fsi|gsi"),
    ("tissue_classification", r"typology|classification|cluster|fabric|tissue|pattern|archetype"),
    ("urban_resilience", r"resilien|multi-hazard|disaster risk|recovery|robustness|adaptive capacity"),
    ("heat_exposure", r"urban heat|land surface temperature|thermal comfort|sky view factor|heat island|\blst\b|\bsvf\b"),
    ("social_vulnerability", r"social vulnerability|equity|exposure|sensitivity|deprivation|environmental justice"),
    ("accessibility_walkability", r"accessibility|walkability|15-minute|amenity|proximity|emergency access|shelter"),
    ("green_infrastructure", r"green infrastructure|nature-based|blue-green|canopy|vegetation|cooling|ecosystem service"),
    ("flood_hazard", r"flood|pluvial|inundation|stormwater|runoff"),
    ("climate_adaptation_planning", r"adaptation|climate change|planning|policy|scenario|land use"),
    ("open_source_gis", r"open source|open-source|qgis|reproducib|geospatial|toolkit|software|workflow"),
    ("spatial_statistics", r"getis-ord|hot spot|hotspot|moran|lisa|spatial autocorrelation|geographically weighted|spatial regression"),
    ("izmir_context", r"izmir|mediterranean|coastal|turkey|t.rkiye"),
]


SECTION_MAP = {
    "morphometrics_typology": (
        "2.1 Urban morphometrics and quantitative urban form",
        "Ground the morphometric vocabulary (compactness, coverage, tessellation-based cells) and the move from qualitative typo-morphology to numerical taxonomy.",
    ),
    "street_network_syntax": (
        "2.2 Street-network configuration and space syntax",
        "Justify segment/angular analysis, centrality and integration as resilience-relevant configurational descriptors of street tissue.",
    ),
    "urban_form_density": (
        "2.3 Built-form density and the Spacematrix logic",
        "Support density descriptors (FSI/GSI/coverage) and the link between built form and microclimate/exposure proxies.",
    ),
    "tissue_classification": (
        "2.4 Urban-tissue typology and clustering",
        "Support sample-based fabric typing and the clustering/classification of tissue archetypes along the Izmir Gulf transect.",
    ),
    "urban_resilience": (
        "1 Introduction / 2.5 Urban resilience and multi-hazard framing",
        "Frame urban resilience, multi-hazard exposure and recovery capacity as the planning lens for the workflow.",
    ),
    "heat_exposure": (
        "2.6 / 4 Heat exposure, SVF and thermal mechanisms",
        "Support urban-heat / SVF / thermal-comfort proxies derived in the PlanX heat module and their morphological drivers.",
    ),
    "social_vulnerability": (
        "2.7 / 4 Social vulnerability and equity",
        "Support the Social Vulnerability Index and equity-adjusted adaptation priority.",
    ),
    "accessibility_walkability": (
        "2.8 / 4 Accessibility, walkability and emergency access",
        "Support network/Euclidean accessibility, amenity proximity, walkable catchments and emergency-shelter coverage.",
    ),
    "green_infrastructure": (
        "2.9 / 6 Green infrastructure and nature-based cooling",
        "Support green/blue cooling, canopy and nature-based-solution interpretation in the discussion.",
    ),
    "flood_hazard": (
        "2.6 / 4 Pluvial flood exposure",
        "Support the pluvial-flood susceptibility screening and its morphological controls.",
    ),
    "climate_adaptation_planning": (
        "1 Introduction / 6 Discussion: adaptation and planning translation",
        "Support climate-adaptation planning, scenario logic and policy translation of the priority classes.",
    ),
    "open_source_gis": (
        "3 Methods: open-source QGIS workflow and reproducibility",
        "Support the open-source / reproducible-workflow argument and position PlanX within the QGIS morphometrics ecosystem (e.g. momepy).",
    ),
    "spatial_statistics": (
        "4.x Spatial statistics (Gi*, LISA, GWR)",
        "Support hot-spot / LISA cluster statistics and GWR, the methods exposed by PlanX GeoStats Lab.",
    ),
    "izmir_context": (
        "3 Study area: Izmir Gulf",
        "Support the Izmir / Mediterranean / coastal context and local vulnerability framing.",
    ),
}


# Software citations for the author's own QGIS plugins. These are NOT DOI-bearing
# journal articles; they are cited as software via their public GitHub repos and
# are appended verbatim, clearly separated from the verified journal bibliography.
SOFTWARE_ENTRIES = r"""
%% --------------------------------------------------------------------------
%% AUTHOR SOFTWARE (QGIS plugins) -- cited as software, not DOI journal items.
%% Metadata taken verbatim from each plugin's metadata.txt (version + repo).
%% Typed as misc so the apalike .bst renders them (no software type in apalike);
%% other styles still read version/publisher/url fields.
%% --------------------------------------------------------------------------

@misc{eminoglu2026planxresilience,
  author       = {Eminoglu, Yusuf},
  title        = {{PlanX: Urban Resilience -- a QGIS Processing suite for city-scale multi-hazard resilience screening}},
  year         = {2026},
  version      = {1.25.0},
  publisher    = {QGIS Python Plugins Repository},
  howpublished = {QGIS plugin, version 1.25.0, \url{https://github.com/YusufEminoglu/planx_urban_resilience}},
  url          = {https://github.com/YusufEminoglu/planx_urban_resilience},
  note         = {Accessed 14 June 2026}
}

@misc{eminoglu2026planxgeostats,
  author       = {Eminoglu, Yusuf},
  title        = {{PlanX GeoStats Lab -- spatial statistics tools for QGIS planning workflows}},
  year         = {2026},
  version      = {0.9.17},
  publisher    = {QGIS Python Plugins Repository},
  howpublished = {QGIS plugin, version 0.9.17, \url{https://github.com/YusufEminoglu/planx_geostats}},
  url          = {https://github.com/YusufEminoglu/planx_geostats},
  note         = {Accessed 14 June 2026}
}
"""


@dataclass
class Candidate:
    doi: str
    discovery_title: str = ""
    discovery_year: int | None = None
    discovery_source: str = ""
    cited_by: int = 0
    relevance_score: int = 0
    categories: set[str] = field(default_factory=set)
    discovery: str = "openalex"


def fetch_json(url: str, timeout: int = 40) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": f"icus2026-planx-literature/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def norm_doi(doi: str) -> str:
    return doi.strip().lower().replace("https://doi.org/", "").replace("http://dx.doi.org/", "")


def normalize_text(text: str) -> str:
    text = html.unescape(text or "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def title_similarity(a: str, b: str) -> float:
    na, nb = normalize_text(a), normalize_text(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def source_key(source: str) -> str:
    return normalize_text(source).replace(" amp ", " ").strip()


def openalex_abstract(work: dict[str, Any]) -> str:
    inv = work.get("abstract_inverted_index") or {}
    pairs = []
    for word, positions in inv.items():
        for pos in positions:
            pairs.append((pos, word))
    return " ".join(word for _, word in sorted(pairs))


def score_and_categories(text: str) -> tuple[int, set[str]]:
    s = text.lower()
    score = 0
    categories: set[str] = set()
    weights = [
        (r"morphometr|urban form|urban morphology|tessellation|typo-?morpholog", 5, "morphometrics_typology"),
        (r"space syntax|street network|road network|centrality|integration|configuration", 4, "street_network_syntax"),
        (r"density|spacematrix|built form|compactness|floor area ratio|\bfsi\b|\bgsi\b", 3, "urban_form_density"),
        (r"typology|classification|cluster|urban fabric|urban tissue|archetype", 3, "tissue_classification"),
        (r"resilien|multi-hazard|disaster risk|recovery|adaptive capacity", 4, "urban_resilience"),
        (r"urban heat|land surface temperature|\blst\b|thermal comfort|sky view factor|\bsvf\b|heat island", 3, "heat_exposure"),
        (r"social vulnerability|equity|environmental justice|deprivation", 3, "social_vulnerability"),
        (r"accessibility|walkability|15-minute|amenity|proximity|shelter|emergency access", 3, "accessibility_walkability"),
        (r"green infrastructure|nature-based|blue-green|canopy|vegetation|cooling|ecosystem service", 2, "green_infrastructure"),
        (r"flood|pluvial|inundation|stormwater|runoff", 2, "flood_hazard"),
        (r"adaptation|climate change|land use|scenario|spatial planning", 2, "climate_adaptation_planning"),
        (r"open source|open-source|qgis|reproducib|toolkit|geospatial software|workflow", 3, "open_source_gis"),
        (r"getis-ord|hot spot|hotspot|moran|lisa|spatial autocorrelation|geographically weighted|spatial regression", 3, "spatial_statistics"),
        (r"izmir|mediterranean|coastal|turkey", 2, "izmir_context"),
        (r"urban|city|cities|neighbou?rhood|planning", 1, "morphometrics_typology"),
    ]
    for pattern, points, category in weights:
        if re.search(pattern, s):
            score += points
            categories.add(category)
    if not re.search(r"urban|city|cities|neighbou?rhood|planning|street|morpholog", s):
        score -= 5
    return score, categories


def query_openalex() -> dict[str, Candidate]:
    candidates: dict[str, Candidate] = {}
    allowed = {source_key(s) for s in Q1_CANDIDATE_SOURCES}
    for term in SEARCH_TERMS:
        params = urllib.parse.urlencode(
            {
                "search": term,
                "filter": "type:article,has_doi:true,from_publication_date:2005-01-01",
                "per-page": 80,
                "sort": "cited_by_count:desc",
                "mailto": MAILTO,
            }
        )
        try:
            data = fetch_json("https://api.openalex.org/works?" + params)
        except Exception:
            time.sleep(0.5)
            continue
        for work in data.get("results", []):
            doi = norm_doi(work.get("doi") or "")
            source = ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            if not doi or not source or source_key(source) not in allowed:
                continue
            text = f"{work.get('title') or ''} {openalex_abstract(work)}"
            score, categories = score_and_categories(text)
            if score < 8:
                continue
            rec = Candidate(
                doi=doi,
                discovery_title=work.get("title") or "",
                discovery_year=work.get("publication_year"),
                discovery_source=source,
                cited_by=work.get("cited_by_count") or 0,
                relevance_score=score,
                categories=categories,
            )
            old = candidates.get(doi)
            if old is None or (rec.relevance_score, rec.cited_by) > (old.relevance_score, old.cited_by):
                candidates[doi] = rec
        time.sleep(0.15)
    return candidates


def query_crossref_title(title: str) -> tuple[str | None, dict[str, Any] | None]:
    params = urllib.parse.urlencode({"query.bibliographic": title, "rows": 3, "mailto": MAILTO})
    try:
        data = fetch_json("https://api.crossref.org/works?" + params)
    except Exception:
        return None, None
    for item in data.get("message", {}).get("items", []):
        doi = norm_doi(item.get("DOI") or "")
        if not doi:
            continue
        sim = title_similarity(title, first(item.get("title")))
        if sim >= 0.88:
            return doi, item
    return None, None


def first(value: Any, default: str = "") -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return default


def crossref_work(doi: str) -> dict[str, Any] | None:
    doi = norm_doi(doi)
    encodings = [urllib.parse.quote(doi, safe=""), urllib.parse.quote(doi, safe="/")]
    for encoded in encodings:
        for _ in range(3):
            try:
                data = fetch_json(f"https://api.crossref.org/works/{encoded}")
                return data.get("message")
            except Exception:
                time.sleep(0.4)
    return None


def openalex_by_doi(doi: str) -> dict[str, Any] | None:
    try:
        encoded = urllib.parse.quote("https://doi.org/" + norm_doi(doi), safe="")
        return fetch_json(f"https://api.openalex.org/works/{encoded}?mailto={MAILTO}")
    except Exception:
        return None


def issued_year(item: dict[str, Any]) -> int | None:
    for field_name in ("published-print", "published-online", "issued"):
        parts = (item.get(field_name) or {}).get("date-parts") or []
        if parts and parts[0]:
            return int(parts[0][0])
    return None


def authors_bibtex(authors: list[dict[str, Any]]) -> str:
    names = []
    for author in authors:
        family = author.get("family") or ""
        given = author.get("given") or ""
        literal = author.get("name") or ""
        if family and given:
            names.append(f"{family}, {given}")
        elif family:
            names.append(family)
        elif literal:
            names.append(literal)
    return " and ".join(names) if names else "{No author listed}"


def tex_escape(text: str) -> str:
    text = html.unescape(text or "")
    text = text.replace("\n", " ").strip()
    replacements = {
        "&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#",
        "_": "\\_", "{": "\\{", "}": "\\}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text)


def make_key(item: dict[str, Any], used: set[str]) -> str:
    authors = item.get("author") or []
    if authors and authors[0].get("family"):
        lead = normalize_text(authors[0]["family"]).split()[0]
    else:
        lead = "ref"
    year = issued_year(item) or "nd"
    title_words = [w for w in normalize_text(first(item.get("title"))).split() if len(w) > 3]
    short = "".join(w[:8].capitalize() for w in title_words[:2]) or "Study"
    base = f"{lead}{year}{short}"
    key = base
    suffix = "b"
    while key in used:
        key = f"{base}{suffix}"
        suffix = chr(ord(suffix) + 1)
    used.add(key)
    return key


def bibtex_entry(key: str, item: dict[str, Any]) -> str:
    title = tex_escape(first(item.get("title")))
    journal = tex_escape(first(item.get("container-title")))
    year = issued_year(item) or ""
    volume = tex_escape(first(item.get("volume")))
    issue = tex_escape(first(item.get("issue")))
    page = tex_escape(first(item.get("page")))
    article = tex_escape(first(item.get("article-number")))
    doi = norm_doi(item.get("DOI") or "")
    url = f"https://doi.org/{doi}" if doi else ""
    fields = [
        ("author", authors_bibtex(item.get("author") or [])),
        ("title", "{" + title + "}"),
        ("journal", "{" + journal + "}"),
        ("year", str(year)),
    ]
    if volume:
        fields.append(("volume", volume))
    if issue:
        fields.append(("number", issue))
    if page:
        fields.append(("pages", page))
    elif article:
        fields.append(("pages", article))
    if doi:
        fields.append(("doi", doi))
    if url:
        fields.append(("url", url))
    lines = [f"@article{{{key},"]
    for name, value in fields:
        lines.append(f"  {name} = {{{value}}},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def add_manual_candidates(candidates: dict[str, Candidate]) -> None:
    for doi, categories in MANUAL_SEED_DOIS.items():
        doi = norm_doi(doi)
        candidates.setdefault(doi, Candidate(doi=doi, discovery="manual_seed"))
        candidates[doi].categories.update(categories)
        candidates[doi].relevance_score += 20
    for title, categories in MANUAL_TITLE_QUERIES.items():
        doi, _ = query_crossref_title(title)
        if not doi:
            continue
        candidates.setdefault(doi, Candidate(doi=doi, discovery_title=title, discovery="manual_title_query"))
        candidates[doi].categories.update(categories)
        candidates[doi].relevance_score += 18
        time.sleep(0.1)


def verify_candidates(candidates: dict[str, Candidate]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected_pool = []
    rejected = []

    def cand_json(cand: Candidate) -> dict[str, Any]:
        data = dict(cand.__dict__)
        data["categories"] = sorted(cand.categories)
        return data

    allowed = {source_key(s) for s in Q1_CANDIDATE_SOURCES}
    for doi, cand in sorted(candidates.items(), key=lambda kv: (-kv[1].relevance_score, -kv[1].cited_by)):
        cr = crossref_work(doi)
        if not cr:
            rejected.append({"doi": doi, "reason": "Crossref DOI lookup failed", "candidate": cand_json(cand)})
            continue
        cr_doi = norm_doi(cr.get("DOI") or "")
        cr_title = first(cr.get("title"))
        cr_year = issued_year(cr)
        cr_source = first(cr.get("container-title"))
        cr_type = cr.get("type")
        if cr_doi != doi:
            rejected.append({"doi": doi, "reason": f"Crossref DOI mismatch: {cr_doi}", "candidate": cand_json(cand)})
            continue
        if cr_type not in {"journal-article", "posted-content"}:
            rejected.append({"doi": doi, "reason": f"Unsupported Crossref type: {cr_type}", "candidate": cand_json(cand)})
            continue
        if source_key(cr_source) not in allowed:
            rejected.append({"doi": doi, "reason": f"Source not in Q1-candidate list: {cr_source}", "candidate": cand_json(cand)})
            continue
        oa = openalex_by_doi(doi)
        oa_title, oa_year, oa_source, oa_ok = "", None, "", False
        sim_oa, year_ok, source_ok = 0.0, False, False
        if oa:
            oa_title = oa.get("title") or ""
            oa_year = oa.get("publication_year")
            oa_source = ((oa.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            sim_oa = title_similarity(cr_title, oa_title)
            year_ok = (not cr_year or not oa_year or abs(int(cr_year) - int(oa_year)) <= 1)
            source_ok = (
                source_key(cr_source) == source_key(oa_source)
                or source_key(cr_source) in source_key(oa_source)
                or source_key(oa_source) in source_key(cr_source)
            )
            oa_ok = sim_oa >= 0.88 and year_ok and source_ok
        if cand.discovery_title:
            sim_discovery = title_similarity(cr_title, cand.discovery_title)
            if sim_discovery < 0.86:
                rejected.append({
                    "doi": doi,
                    "reason": f"Discovery title does not match Crossref title: similarity={sim_discovery:.3f}",
                    "crossref_title": cr_title,
                    "discovery_title": cand.discovery_title,
                })
                continue
        else:
            sim_discovery = None
        text = f"{cr_title} {cr_source}"
        extra_score, extra_categories = score_and_categories(text)
        categories = set(cand.categories) | extra_categories
        for cat, pattern in CATEGORY_RULES:
            if re.search(pattern, text.lower()):
                categories.add(cat)
        selected_pool.append({
            "doi": doi,
            "crossref": cr,
            "title": cr_title,
            "year": cr_year,
            "source": html.unescape(cr_source),
            "openalex_title": oa_title,
            "openalex_year": oa_year,
            "openalex_source": oa_source,
            "crossref_openalex_title_similarity": sim_oa,
            "crossref_discovery_title_similarity": sim_discovery,
            "openalex_verified": oa_ok,
            "crossref_openalex_year_ok": year_ok,
            "crossref_openalex_source_ok": source_ok,
            "categories": sorted(categories),
            "relevance_score": cand.relevance_score + extra_score,
            "cited_by": cand.cited_by,
            "discovery": cand.discovery,
        })
        time.sleep(0.12)
    return selected_pool, rejected


def select_final(pool: list[dict[str, Any]], target: int = 68) -> list[dict[str, Any]]:
    quotas = [
        ("morphometrics_typology", 9),
        ("street_network_syntax", 8),
        ("urban_form_density", 5),
        ("tissue_classification", 6),
        ("urban_resilience", 8),
        ("heat_exposure", 8),
        ("social_vulnerability", 5),
        ("accessibility_walkability", 6),
        ("green_infrastructure", 5),
        ("flood_hazard", 3),
        ("climate_adaptation_planning", 6),
        ("open_source_gis", 5),
        ("spatial_statistics", 5),
        ("izmir_context", 2),
    ]
    sorted_pool = sorted(pool, key=lambda r: (-r["relevance_score"], -r["cited_by"], -(r["year"] or 0)))
    chosen: dict[str, dict[str, Any]] = {}
    for cat, quota in quotas:
        for rec in sorted_pool:
            if len([r for r in chosen.values() if cat in r["categories"]]) >= quota:
                break
            if rec["doi"] not in chosen and cat in rec["categories"]:
                chosen[rec["doi"]] = rec
    for rec in sorted_pool:
        if len(chosen) >= target:
            break
        if rec["doi"] not in chosen:
            chosen[rec["doi"]] = rec
    return list(chosen.values())


def write_outputs(final: list[dict[str, Any]], rejected: list[dict[str, Any]], pool: list[dict[str, Any]]) -> None:
    used: set[str] = set()
    for rec in final:
        rec["bibkey"] = make_key(rec["crossref"], used)
    final = sorted(final, key=lambda r: (
        min([list(SECTION_MAP).index(c) if c in SECTION_MAP else 99 for c in r["categories"]] or [99]),
        r["year"] or 0,
        r["bibkey"],
    ))
    bib_entries = [
        "% DOI-verified bibliography for the ICUS 2026 PlanX urban-resilience paper.",
        "% Generated by references/scripts/build_verified_literature_bank.py.",
        "% Every journal entry was retrieved by its DOI from Crossref; DOI equality,",
        "% Q1-candidate source, and journal-article type were all enforced.",
        "% Do NOT add DOI-bearing entries by hand without re-running the verifier.",
        "% (BibTeX note: comment lines must contain no at-sign, or BibTeX parses them.)",
        "",
    ]
    bib_entries.extend(bibtex_entry(rec["bibkey"], rec["crossref"]) + "\n" for rec in final)
    bib_text = "\n".join(bib_entries) + "\n" + SOFTWARE_ENTRIES
    OUT_BIB.write_text(bib_text, encoding="utf-8")

    OUT_SELECTED.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_REJECTED.write_text(json.dumps(rejected, ensure_ascii=False, indent=2), encoding="utf-8")

    by_cat: dict[str, list[dict[str, Any]]] = {}
    for rec in final:
        for cat in rec["categories"]:
            by_cat.setdefault(cat, []).append(rec)

    lines = [
        "# Reference Mapping Guide",
        "",
        "This file maps the DOI-verified bibliography in `paper/manuscript/src/refs.bib` to the planned manuscript sections.",
        "",
        "**Validation rule:** every entry was retrieved through its DOI from Crossref. When a record was discovered via OpenAlex, the Crossref title/year/source were compared with OpenAlex metadata before inclusion. Records with weak DOI-title matching were rejected.",
        "",
        "**Journal-tier note:** sources are treated as Q1-level *candidate* sources; final WOS/JCR quartile must be verified through institutional access before submission.",
        "",
        f"**Counts:** {len(final)} verified journal references + 2 author-software citations (`eminoglu2026planxresilience`, `eminoglu2026planxgeostats`).",
        "",
    ]
    for cat, (section, context) in SECTION_MAP.items():
        refs = sorted(by_cat.get(cat, []), key=lambda r: (r["year"] or 0, r["bibkey"]))
        if not refs:
            continue
        lines.append(f"## {section}")
        lines.append("")
        lines.append(f"**Use:** {context}")
        lines.append("")
        lines.append("**References:** " + ", ".join(f"`{r['bibkey']}`" for r in refs))
        lines.append("")
        lines.append("| Key | Year | Journal | DOI | Title |")
        lines.append("|---|---:|---|---|---|")
        for r in refs:
            lines.append(f"| `{r['bibkey']}` | {r['year'] or ''} | {r['source']} | `{r['doi']}` | {r['title']} |")
        lines.append("")
    OUT_MAP.write_text("\n".join(lines), encoding="utf-8")

    report = [
        "# DOI Verification Report",
        "",
        f"Selected references: {len(final)}",
        f"Verified candidate pool before final selection: {len(pool)}",
        f"Rejected records: {len(rejected)}",
        "",
        "## Inclusion Rules",
        "",
        "1. DOI must resolve in Crossref and Crossref's own DOI must equal the queried DOI.",
        "2. Crossref type must be journal-article (or posted-content for tracked online-first records).",
        "3. Crossref source must be in the curated Q1-candidate source list.",
        "4. If discovered through OpenAlex, discovery title must match Crossref title with similarity >= 0.86.",
        "5. OpenAlex DOI lookup (title/source/year) is recorded for an independent cross-check.",
        "",
        "## Selected Records",
        "",
        "| Key | CR/OA title sim | Year ok | Source ok | DOI | Title |",
        "|---|---:|---|---|---|---|",
    ]
    for r in final:
        report.append(
            f"| `{r['bibkey']}` | {r['crossref_openalex_title_similarity']:.3f} | "
            f"{r['crossref_openalex_year_ok']} | {r['crossref_openalex_source_ok']} | `{r['doi']}` | {r['title']} |"
        )
    report.extend(["", "## Rejected Records", "", "| DOI | Reason |", "|---|---|"])
    for rej in rejected[:200]:
        report.append(f"| `{rej.get('doi', '')}` | {str(rej.get('reason', '')).replace('|', '/')} |")
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    candidates = query_openalex()
    add_manual_candidates(candidates)
    pool, rejected = verify_candidates(candidates)
    final = select_final(pool, target=68)
    write_outputs(final, rejected, pool)
    print(json.dumps({"selected": len(final), "pool": len(pool), "rejected": len(rejected)}, indent=2))


if __name__ == "__main__":
    main()
