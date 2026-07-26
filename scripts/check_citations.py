import re, glob, os
src = 'paper/manuscript/src'
keys = set()
for f in glob.glob(os.path.join(src, '**', '*.tex'), recursive=True):
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'\\cite[a-z]*\*?(?:\[[^\]]*\])?\{([^}]*)\}', t):
        for k in m.group(1).split(','):
            k = k.strip()
            if k:
                keys.add(k)
bib = open(os.path.join(src, 'refs.bib'), encoding='utf-8').read()
defined = set(re.findall(r'@\w+\{\s*([^,]+),', bib))
print('cite keys used :', len(keys))
print('bib entries    :', len(defined))
missing = sorted(keys - defined)
unused = sorted(defined - keys)
print('\nUNDEFINED (cited but not in refs.bib):', len(missing))
for k in missing:
    print('   -', k)
print('\nUNUSED (in refs.bib, never cited):', len(unused))
for k in unused:
    print('   -', k)
