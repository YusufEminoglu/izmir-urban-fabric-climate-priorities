#!/usr/bin/env python3
"""Crossref-verify the v3 manuscript-core references and emit BibTeX.

Quality bar (see memory q1-quality-bar-literature-grounded): every DOI is
retrieved from Crossref, DOI equality is enforced, and the work must be a
journal-article. Output:
  references/refs_v3_verified.bib   -- verified entries only
  references/verification/v3_verification_report.md
Classic items without a DOI (Hillier&Hanson 1984, Hwang&Yoon 1981, Cutter 2003,
Stewart&Oke 2012) are intentionally excluded here; handle separately.
"""
import json, time, urllib.request, urllib.error, sys, os

MAILTO = "yusuf.emnglu@gmail.com"

# citekey -> DOI  (citekeys follow the existing refs.bib style: authorYearTitleword)
ANCHORS = {
    "boeing2017Osmnx":                 "10.1016/j.compenvurbsys.2017.05.004",
    "boeing2025ModelingNetworks":      "10.1111/gean.70009",
    "canguzel2024ClimateChange":       "10.1007/s11069-024-06798-5",
    "debray2025UniversalPatterns":     "10.1016/j.jag.2025.104610",
    "fang2024Urbanclassifier":         "10.1016/j.compenvurbsys.2024.102132",
    "fleischmann2020Morphologic":      "10.1016/j.compenvurbsys.2019.101441",
    "imroz2025IntegratedAssess":       "10.1016/j.jenvman.2025.127984",
    "iqbal2025HeatStress":             "10.5194/nhess-25-2481-2025",
    "li2026BlockGrid":                 "10.1016/j.envsoft.2025.106738",
    "liu2026Nonlinear":                "10.1016/j.scs.2025.107100",
    "neumann2026ClimateJustice":       "10.1016/j.envdev.2025.101365",
    "turner2025Guhvi":                 "10.1016/j.uclim.2025.102716",
    "vartholomaios2025Detection":      "10.1007/s43762-025-00206-9",
    "wangH2025FifteenMinute":          "10.1016/j.tra.2025.104583",
    "wangJ2024FigureGround":           "10.1016/j.compenvurbsys.2024.102076",
    "wangZ2025MarginalInteraction":    "10.1016/j.buildenv.2025.112673",
    "wangZ2025PlainPlateau":           "10.1016/j.scs.2024.106046",
    "wei2025NatureBased":              "10.1038/s44284-025-00349-0",
    "zhang2024MultiObjective":         "10.1016/j.apenergy.2024.124117",
    "zhu2025SpongeCities":             "10.1016/j.resconrec.2025.108179",
}


def fetch(doi):
    url = f"https://api.crossref.org/works/{doi}?mailto={MAILTO}"
    req = urllib.request.Request(url, headers={"User-Agent": f"icus2026/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]


def fmt_authors(m):
    out = []
    for a in m.get("author", []):
        fam = a.get("family", "").strip()
        giv = a.get("given", "").strip()
        if fam and giv:
            out.append(f"{fam}, {giv}")
        elif fam:
            out.append(fam)
        elif a.get("name"):
            out.append(a["name"])
    return " and ".join(out)


def bibtex(key, m):
    j = (m.get("container-title") or [""])[0]
    title = (m.get("title") or [""])[0]
    year = ""
    for f in ("published-print", "published-online", "published", "issued"):
        p = m.get(f, {}).get("date-parts", [[None]])
        if p and p[0] and p[0][0]:
            year = str(p[0][0]); break
    fields = [
        ("author", fmt_authors(m)),
        ("title", "{" + title + "}"),
        ("journal", "{" + j + "}"),
        ("year", year),
        ("volume", m.get("volume", "")),
        ("number", m.get("issue", "")),
        ("pages", (m.get("page", "") or "").replace("-", "--") if m.get("page") else ""),
        ("doi", m.get("DOI", "")),
        ("url", "https://doi.org/" + m.get("DOI", "")),
    ]
    lines = [f"@article{{{key},"]
    for name, val in fields:
        if val:
            lines.append(f"  {name} = {{{val}}},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bibs, report = [], []
    ok = fail = 0
    for key, doi in ANCHORS.items():
        try:
            m = fetch(doi)
        except Exception as e:
            report.append(f"- [FAIL net] {key} {doi}: {e}"); fail += 1; continue
        got = (m.get("DOI") or "").lower()
        typ = m.get("type", "")
        if got != doi.lower():
            report.append(f"- [FAIL doi] {key}: asked {doi} got {got}"); fail += 1; continue
        if typ != "journal-article":
            report.append(f"- [FAIL type] {key} {doi}: type={typ}"); fail += 1; continue
        j = (m.get("container-title") or [""])[0]
        ttl = (m.get("title") or [""])[0]
        bibs.append(bibtex(key, m))
        report.append(f"- [OK] {key} | {j} | {ttl[:65]}")
        ok += 1
        time.sleep(0.4)

    bib_path = os.path.join(here, "refs_v3_verified.bib")
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write("% v3 manuscript-core references -- Crossref-verified by verify_v3_anchors.py\n")
        f.write("% DOI equality + journal-article type enforced. Do not hand-edit DOIs.\n\n")
        f.write("\n\n".join(bibs) + "\n")
    rep_path = os.path.join(here, "verification", "v3_verification_report.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(f"# v3 anchor verification\n\nOK={ok} FAIL={fail} of {len(ANCHORS)}\n\n")
        f.write("\n".join(report) + "\n")
    print(f"OK={ok} FAIL={fail} -> {bib_path}")
    print("\n".join(report))


if __name__ == "__main__":
    main()
