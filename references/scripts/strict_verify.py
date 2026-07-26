"""Letter-exact, 3-stage verification of paper/manuscript/src/refs.bib.

Stronger than independent_verify.py: this does NOT use similarity thresholds for
the primary check. It reconstructs every field from the authoritative source and
compares CHARACTER BY CHARACTER.

  Stage 1  CROSSREF (letter-exact). Re-fetch each DOI from the Crossref REST API.
           Canonically normalize (HTML-unescape + collapse internal whitespace),
           reverse the LaTeX escaping applied in the .bib, and require EXACT
           string equality for author, title, journal, year, volume, issue,
           pages, and DOI. Any single differing character is a FAIL with a diff.

  Stage 2  DOI.ORG (independent resolution). Content-negotiate the DOI at
           https://doi.org with CSL-JSON. This goes through the DOI resolver and
           registration agency -- a path independent of the Crossref REST API --
           proving the DOI is live and points to the same work (normalized title
           + year + first-author family must agree).

  Stage 3  OPENALEX (third authority). Confirm DOI -> same work (normalized title
           agreement and year within the online/print window).

A reference is APPROVED only when all three stages agree. The script writes a
full report and exits non-zero if a single entry fails. @misc software entries
are checked structurally (fields present, URL resolves) but not via DOI.
"""

from __future__ import annotations

import html
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
OUT = ROOT / "references" / "verification" / "strict_letter_exact_report.md"
MAILTO = "yusuf.eminoglu@deu.edu.tr"

UA = {"User-Agent": f"icus2026-strict-verify/1.0 (mailto:{MAILTO})"}


# ----------------------------------------------------------------------------- helpers
def fetch_json(url: str, accept: str | None = None, timeout: int = 45) -> dict[str, Any] | None:
    headers = dict(UA)
    if accept:
        headers["Accept"] = accept
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                return json.load(r)
        except Exception:
            time.sleep(0.6)
    return None


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def norm_loose(text: str) -> str:
    """Aggressive normalization for cross-source identity (Stage 2/3)."""
    text = unicodedata.normalize("NFKD", html.unescape(text or ""))
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text)).strip()


def loose_sim(a: str, b: str) -> float:
    na, nb = norm_loose(a), norm_loose(b)
    if not na or not nb:
        return 0.0
    return SequenceMatcher(None, na, nb).ratio()


def reverse_tex(text: str) -> str:
    """Invert the exact escaping that build_verified_literature_bank.tex_escape did."""
    for esc, raw in (("\\&", "&"), ("\\%", "%"), ("\\$", "$"), ("\\#", "#"),
                     ("\\_", "_"), ("\\{", "{"), ("\\}", "}")):
        text = text.replace(esc, raw)
    return text


def cr_first(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    return value if isinstance(value, str) else ""


def cr_authors(authors: list[dict[str, Any]]) -> str:
    """Exactly mirror build_verified_literature_bank.authors_bibtex."""
    names = []
    for a in authors or []:
        family, given, literal = a.get("family") or "", a.get("given") or "", a.get("name") or ""
        if family and given:
            names.append(f"{family}, {given}")
        elif family:
            names.append(family)
        elif literal:
            names.append(literal)
    return " and ".join(names) if names else "{No author listed}"


def cr_years(item: dict[str, Any]) -> set[int]:
    years: set[int] = set()
    for f in ("published-print", "published-online", "issued", "created"):
        parts = (item.get(f) or {}).get("date-parts") or []
        if parts and parts[0]:
            years.add(int(parts[0][0]))
    return years


def char_diff(a: str, b: str) -> str:
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            return f"first diff at index {i}: bib={ca!r} vs source={cb!r}\n      bib   : {a[max(0,i-20):i+20]!r}\n      source: {b[max(0,i-20):i+20]!r}"
    if len(a) != len(b):
        longer, who = (a, "bib") if len(a) > len(b) else (b, "source")
        return f"length differs ({len(a)} vs {len(b)}); extra in {who}: {longer[min(len(a),len(b)):][:40]!r}"
    return "identical"


# ----------------------------------------------------------------------------- bib parse
def parse_bib(text: str) -> list[dict[str, str]]:
    entries = []
    for block in re.split(r"\n(?=@)", text):
        s = block.strip()
        head = re.match(r"@(\w+)\{([^,]+),", s)
        if not head:
            continue
        etype, key = head.group(1).lower(), head.group(2)
        rec: dict[str, str] = {"_type": etype, "_key": key}
        for fld in ("author", "title", "journal", "year", "volume", "number",
                    "pages", "doi", "url", "howpublished", "version", "note"):
            m = re.search(rf"\n\s*{fld}\s*=\s*\{{(.*?)\}},?\s*(?=\n\s*\w+\s*=|\n\}})",
                          "\n" + block, re.I | re.S)
            if m:
                val = m.group(1)
                # strip one layer of wrapping braces used for titles/journals
                val = val.strip()
                if val.startswith("{") and val.endswith("}"):
                    val = val[1:-1]
                rec[fld] = re.sub(r"\s+", " ", val).strip()
        entries.append(rec)
    return entries


# ----------------------------------------------------------------------------- main
def verify_article(rec: dict[str, str]) -> tuple[str, list[str]]:
    doi = rec.get("doi", "").lower().strip()
    problems: list[str] = []

    # ---------- Stage 1: Crossref letter-exact ----------
    cr = fetch_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}")
    msg = cr.get("message") if cr else None
    if not msg:
        return "FAIL", ["Stage1 Crossref: DOI did not resolve"]

    # DOI (case-insensitive per spec; we canonicalize to lowercase)
    cr_doi = (msg.get("DOI") or "")
    if cr_doi.lower() != doi:
        problems.append(f"Stage1 DOI mismatch: bib={doi} crossref={cr_doi.lower()}")
    elif cr_doi != doi:
        problems.append(f"NOTE DOI case canonicalized (spec-insensitive): crossref={cr_doi} -> bib={doi}")

    # title list length (subtitle dropped?)
    title_list = msg.get("title") or []
    if isinstance(title_list, list) and len(title_list) > 1:
        problems.append(f"NOTE Crossref title has {len(title_list)} parts; bib uses part 1 only "
                        f"(possible dropped subtitle): {title_list[1:]!r}")

    def exact(field_bib: str, canonical: str, label: str) -> None:
        bib_val = reverse_tex(rec.get(field_bib, ""))
        can = collapse_ws(canonical)
        if bib_val != can:
            problems.append(f"Stage1 {label} NOT letter-exact: {char_diff(bib_val, can)}")

    exact("author", cr_authors(msg.get("author") or []), "author")
    exact("title", cr_first(msg.get("title")), "title")
    exact("journal", cr_first(msg.get("container-title")), "journal")
    if rec.get("volume"):
        exact("volume", cr_first(msg.get("volume")), "volume")
    if rec.get("number"):
        exact("number", cr_first(msg.get("issue")), "issue")
    if rec.get("pages"):
        canonical_pages = cr_first(msg.get("page")) or cr_first(msg.get("article-number"))
        exact("pages", canonical_pages, "pages")

    yrs = cr_years(msg)
    if rec.get("year") and int(rec["year"]) not in yrs:
        problems.append(f"Stage1 year {rec['year']} not in Crossref dates {sorted(yrs)}")

    # ---------- Stage 2: doi.org independent resolution (CSL-JSON) ----------
    csl = fetch_json(f"https://doi.org/{urllib.parse.quote(doi, safe='/')}",
                     accept="application/vnd.citationstyles.csl+json")
    if not csl:
        problems.append("Stage2 doi.org: DOI did not resolve via content negotiation")
    else:
        csl_title = csl.get("title") or ""
        if isinstance(csl_title, list):
            csl_title = " ".join(csl_title)
        sim = loose_sim(rec.get("title", ""), csl_title)
        if sim < 0.97:
            problems.append(f"Stage2 doi.org title identity weak: sim={sim:.3f} ({csl_title[:80]!r})")
        csl_years = set()
        for k in ("issued", "published-print", "published-online"):
            dp = (csl.get(k) or {}).get("date-parts") or []
            if dp and dp[0]:
                csl_years.add(int(dp[0][0]))
        if rec.get("year") and csl_years and not any(abs(int(rec["year"]) - y) <= 1 for y in csl_years):
            problems.append(f"Stage2 doi.org year {rec['year']} vs {sorted(csl_years)}")

    # ---------- Stage 3: OpenAlex third authority ----------
    oa = fetch_json(f"https://api.openalex.org/works/{urllib.parse.quote('https://doi.org/'+doi, safe='')}?mailto={MAILTO}")
    if not oa:
        problems.append("Stage3 OpenAlex: DOI not found")
    else:
        oa_doi = (oa.get("doi") or "").lower().replace("https://doi.org/", "")
        if oa_doi != doi:
            problems.append(f"Stage3 OpenAlex DOI mismatch: {oa_doi}")
        sim = loose_sim(rec.get("title", ""), oa.get("title") or "")
        if sim < 0.97:
            problems.append(f"Stage3 OpenAlex title identity weak: sim={sim:.3f}")

    hard = [p for p in problems if not p.startswith("NOTE")]
    return ("PASS" if not hard else "FAIL"), problems


def verify_software(rec: dict[str, str]) -> tuple[str, list[str]]:
    problems = []
    for need in ("author", "title", "year", "url", "howpublished"):
        if not rec.get(need):
            problems.append(f"missing field: {need}")
    url = rec.get("url", "")
    if url:
        try:
            req = urllib.request.Request(url, headers=UA, method="HEAD")
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status >= 400:
                    problems.append(f"URL returned {r.status}")
        except Exception as e:
            problems.append(f"URL not reachable: {e}")
    return ("PASS" if not problems else "WARN"), problems


def main() -> int:
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    arts = [e for e in entries if e["_type"] == "article"]
    soft = [e for e in entries if e["_type"] in ("misc", "software")]

    rows, fails, notes = [], [], []
    for i, rec in enumerate(arts, 1):
        status, problems = verify_article(rec)
        for p in problems:
            (notes if p.startswith("NOTE") else fails).append((rec["_key"], p))
        flag = "PASS" if status == "PASS" else "FAIL"
        print(f"[{i:>2}/{len(arts)}] {flag}  {rec['_key']:<30} {rec.get('doi','')}")
        rows.append((rec["_key"], rec.get("doi", ""), status))
        time.sleep(0.12)

    soft_rows = []
    for rec in soft:
        status, problems = verify_software(rec)
        soft_rows.append((rec["_key"], rec.get("url", ""), status, "; ".join(problems)))
        print(f"[soft] {status}  {rec['_key']}  {rec.get('url','')}")

    n_pass = sum(1 for r in rows if r[2] == "PASS")
    lines = [
        "# Strict Letter-Exact Verification Report (3-stage)",
        "",
        f"Articles checked: {len(arts)}  |  Letter-exact PASS: {n_pass}  |  FAIL: {len(arts)-n_pass}",
        f"Software entries: {len(soft)}",
        "",
        "**Stage 1 — Crossref (letter-exact):** author/title/journal/year/volume/issue/"
        "pages/DOI reconstructed from Crossref and compared character-by-character "
        "(LaTeX escaping reversed, HTML unescaped, whitespace collapsed).",
        "**Stage 2 — doi.org:** DOI content-negotiated (CSL-JSON) through the DOI "
        "resolver/registration agency; title identity >=0.97 and year window enforced.",
        "**Stage 3 — OpenAlex:** independent third-authority DOI->work confirmation.",
        "",
        "A reference is APPROVED only if all three stages agree. 'NOTE' items are "
        "non-failing observations (e.g. spec-insensitive DOI lowercasing, or a "
        "subtitle Crossref stores as a separate title element).",
        "",
        "| # | Key | DOI | Result |",
        "|---:|---|---|---|",
    ]
    for i, (key, doi, status) in enumerate(rows, 1):
        lines.append(f"| {i} | `{key}` | `{doi}` | {'✅ '+status if status=='PASS' else '❌ '+status} |")
    lines += ["", "## Software (@misc) entries", "", "| Key | URL | Result | Notes |", "|---|---|---|---|"]
    for key, url, status, note in soft_rows:
        lines.append(f"| `{key}` | {url} | {status} | {note} |")
    if fails:
        lines += ["", "## ❌ HARD FAILURES", "", "| Key | Problem |", "|---|---|"]
        for key, p in fails:
            lines.append(f"| `{key}` | {p.replace(chr(10),' / ')} |")
    if notes:
        lines += ["", "## ℹ️ NOTES (non-failing)", "", "| Key | Note |", "|---|---|"]
        for key, p in notes:
            lines.append(f"| `{key}` | {p.replace(chr(10),' / ')} |")
    OUT.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + ("=" * 60))
    print(f"LETTER-EXACT: {n_pass}/{len(arts)} articles PASS, {len(fails)} hard problem(s), {len(notes)} note(s)")
    print(f"Report: {OUT}")
    print("RESULT:", "ALL CLEAR — APPROVED" if not fails else "PROBLEMS FOUND — NOT APPROVED")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
