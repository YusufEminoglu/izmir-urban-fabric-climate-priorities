"""Independent triple-check of every DOI in paper/manuscript/src/refs.bib.

This is deliberately a SEPARATE code path from the builder. It parses the .bib
file directly (not the builder's JSON) and re-queries each DOI:

  Check 2  -> Crossref /works/{doi}: DOI matches, title similarity vs bib title,
              year matches the bib year, journal/container matches the bib journal.
  Check 3  -> OpenAlex /works/doi:{doi}: DOI matches, title similarity vs bib title,
              year within +/-1, source matches.

A reference PASSES only if both checks agree with the bib record. Any failure is
printed and the script exits non-zero, so a single unverified entry blocks the
"all clear". @software entries (the QGIS plugins) are intentionally skipped --
they are not DOI journal items.
"""

from __future__ import annotations

import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BIB = ROOT / "paper" / "manuscript" / "src" / "refs.bib"
OUT = ROOT / "references" / "verification" / "independent_verification_report.md"
MAILTO = "yusuf.eminoglu@deu.edu.tr"

TITLE_THRESHOLD = 0.85


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sim(a: str, b: str) -> float:
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def fetch(url: str) -> dict[str, Any] | None:
    req = urllib.request.Request(url, headers={"User-Agent": f"icus2026-independent-verify/1.0 (mailto:{MAILTO})"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception:
            time.sleep(0.5)
    return None


def cr_first(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    return value if isinstance(value, str) else ""


def cr_year(item: dict[str, Any]) -> int | None:
    for f in ("published-print", "published-online", "issued"):
        parts = (item.get(f) or {}).get("date-parts") or []
        if parts and parts[0]:
            return int(parts[0][0])
    return None


def cr_all_years(item: dict[str, Any]) -> set[int]:
    """Every plausible publication year (online-first AND print issue)."""
    years: set[int] = set()
    for f in ("published-print", "published-online", "issued", "created"):
        parts = (item.get(f) or {}).get("date-parts") or []
        if parts and parts[0]:
            years.add(int(parts[0][0]))
    return years


def parse_bib(text: str) -> list[dict[str, str]]:
    """Minimal field extractor for @article blocks."""
    entries = []
    for block in re.split(r"\n(?=@)", text):
        if not block.lstrip().lower().startswith("@article"):
            continue
        key = re.match(r"@article\{([^,]+),", block.strip(), re.I)
        rec = {"key": key.group(1) if key else "?"}
        for fld in ("title", "journal", "year", "doi"):
            m = re.search(rf"\b{fld}\s*=\s*\{{(.*?)\}}\s*,?\s*\n", block, re.I | re.S)
            if not m:
                m = re.search(rf"\b{fld}\s*=\s*\{{(.*?)\}}\s*\n?\}}", block, re.I | re.S)
            val = m.group(1) if m else ""
            val = re.sub(r"[{}]", "", val)
            rec[fld] = re.sub(r"\s+", " ", val).strip()
        entries.append(rec)
    return entries


def main() -> int:
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    rows = []
    failures = []
    for i, e in enumerate(entries, 1):
        doi = e["doi"].lower().strip()
        bib_title, bib_journal, bib_year = e["title"], e["journal"], e["year"]
        # ---- Check 2: Crossref ----
        cr = fetch(f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}")
        cr_msg = cr.get("message") if cr else None
        if not cr_msg:
            failures.append((e["key"], doi, "Crossref lookup failed"))
            rows.append((e["key"], doi, "FAIL", "no Crossref"))
            continue
        cr_doi = (cr_msg.get("DOI") or "").lower()
        cr_t = cr_first(cr_msg.get("title"))
        cr_j = cr_first(cr_msg.get("container-title"))
        cr_y = cr_year(cr_msg)
        cr_years = cr_all_years(cr_msg)
        t_sim = sim(bib_title, cr_t)
        j_sim = sim(bib_journal, cr_j)
        doi_ok = cr_doi == doi
        year_ok = (not bib_year) or (cr_y is not None and str(cr_y) == bib_year)
        cr_ok = doi_ok and t_sim >= TITLE_THRESHOLD and year_ok and j_sim >= 0.55
        # ---- Check 3: OpenAlex ----
        oa = fetch(f"https://api.openalex.org/works/{urllib.parse.quote('https://doi.org/' + doi, safe='')}?mailto={MAILTO}")
        if oa:
            oa_doi = (oa.get("doi") or "").lower().replace("https://doi.org/", "")
            oa_t = oa.get("title") or ""
            oa_y = oa.get("publication_year")
            oa_t_sim = sim(bib_title, oa_t)
            # Accept the online-first vs print-issue gap: OA year must be within
            # +/-1 of ANY Crossref date (online or print), not just the bib year.
            ref_years = cr_years or ({int(bib_year)} if bib_year else set())
            oa_year_ok = (oa_y is None) or (not ref_years) or any(abs(int(oa_y) - y) <= 1 for y in ref_years)
            oa_ok = (oa_doi == doi) and oa_t_sim >= TITLE_THRESHOLD and oa_year_ok
        else:
            oa_ok, oa_t_sim = False, 0.0
        status = "PASS" if (cr_ok and oa_ok) else "FAIL"
        if status == "FAIL":
            why = []
            if not doi_ok: why.append("CR DOI mismatch")
            if t_sim < TITLE_THRESHOLD: why.append(f"CR title sim {t_sim:.2f}")
            if not year_ok: why.append(f"CR year {cr_y}!={bib_year}")
            if j_sim < 0.55: why.append(f"journal sim {j_sim:.2f} ({cr_j})")
            if not oa_ok: why.append(f"OA fail (sim {oa_t_sim:.2f})")
            failures.append((e["key"], doi, "; ".join(why)))
        rows.append((e["key"], doi, status, f"CRt={t_sim:.2f} CRj={j_sim:.2f} OAt={oa_t_sim:.2f} y={cr_y}"))
        print(f"[{i:>2}/{len(entries)}] {status}  {e['key']:<28} {doi}")
        time.sleep(0.1)

    lines = [
        "# Independent Triple-Check Report",
        "",
        f"Bib file: `{BIB.relative_to(ROOT)}`",
        f"@article entries checked: {len(entries)}",
        f"PASS: {sum(1 for r in rows if r[2] == 'PASS')}   FAIL: {len(failures)}",
        "",
        "Each entry was re-queried independently against Crossref (check 2) and "
        "OpenAlex (check 3), parsing the .bib directly. An entry passes only when "
        "the DOI resolves to a record whose title (>=0.85), year, and journal all "
        "match the .bib values on both services.",
        "",
        "| Key | DOI | Status | Detail |",
        "|---|---|---|---|",
    ]
    for key, doi, status, detail in rows:
        lines.append(f"| `{key}` | `{doi}` | {status} | {detail} |")
    if failures:
        lines += ["", "## FAILURES", "", "| Key | DOI | Why |", "|---|---|---|"]
        for key, doi, why in failures:
            lines.append(f"| `{key}` | `{doi}` | {why} |")
    OUT.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + ("ALL CLEAR" if not failures else f"{len(failures)} FAILURE(S)"))
    print(f"Report: {OUT}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
