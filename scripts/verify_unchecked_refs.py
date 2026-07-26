"""Verify DOI-bearing refs.bib entries that are NOT already in a verification report.
Targets only the previously-unchecked entries to satisfy the 'verify every citation' bar.
"""
import re, os, time, requests
from difflib import SequenceMatcher

SRC = 'paper/manuscript/src/refs.bib'
REPORTS = [
    'references/verification/independent_verification_report.md',
    'references/verification/v3_verification_report.md',
]
H = {'User-Agent': 'icus2026-refcheck/1.0 (mailto:yusuf.eminoglu@deu.edu.tr)'}

bib = open(SRC, encoding='utf-8').read()
entries = {}
for block in re.split(r'(?=@)', bib):
    m = re.match(r'@(\w+)\{\s*([^,]+),', block)
    if not m:
        continue
    key = m.group(2).strip()
    doi = re.search(r'doi\s*=\s*\{([^}]+)\}', block)
    title = re.search(r'title\s*=\s*\{+([^@]*?)\}+,\s*\n', block)
    entries[key] = dict(type=m.group(1), doi=doi.group(1) if doi else None,
                        title=(title.group(1) if title else '').strip())

checked = set()
for rp in REPORTS:
    if os.path.exists(rp):
        txt = open(rp, encoding='utf-8').read()
        for k in re.findall(r'`?([A-Za-z]+\d{4}[A-Za-z]+)`?', txt):
            checked.add(k)

todo = [k for k in entries if k not in checked]
print('Total entries:', len(entries), '| already in a report:', len(set(entries) & checked),
      '| to verify now:', len(todo))
print()

def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', '', s.lower())).strip()

for k in sorted(todo):
    e = entries[k]
    if not e['doi']:
        print(f'[SKIP no-DOI] {k} ({e["type"]})  -- software/book without DOI by design')
        continue
    try:
        r = requests.get(f'https://api.crossref.org/works/{e["doi"]}', headers=H, timeout=30)
        if r.status_code != 200:
            print(f'[FAIL http {r.status_code}] {k} doi={e["doi"]}')
            continue
        m = r.json()['message']
        crt = (m.get('title') or ['?'])[0]
        sim = SequenceMatcher(None, norm(e['title']), norm(crt)).ratio()
        j = (m.get('container-title') or ['?'])[0]
        y = m.get('issued', {}).get('date-parts', [[None]])[0][0]
        flag = 'OK' if sim >= 0.85 else 'TITLE?'
        print(f'[{flag}] {k} | sim={sim:.2f} | {y} | {j} | {e["doi"]}')
    except Exception as ex:
        print(f'[ERR] {k}: {ex}')
    time.sleep(0.3)
