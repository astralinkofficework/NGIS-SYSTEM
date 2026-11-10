import re, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
lay = open('assets/js/layout.js', encoding='utf-8').read()
nav = set()
for h in re.findall(r'href:\s*"([^"]+)"', lay):
    h = h.split('?')[0]
    m = re.search(r'pages/[\w-]+/-?[\w.-]*\.html|pages/[\w-]+/[\w.-]+\.html|index\.html', h)
    if m: nav.add(os.path.basename(m.group(0)))
pages = {os.path.basename(p) for p in re.glob if False} if False else {os.path.basename(p) for p in __import__('glob').glob('pages/*/*.html')}
# in-page link graph (exclude layout.js)
import glob
htmls = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']
linked = set()
for f in htmls:
    txt = open(f, encoding='utf-8', errors='replace').read()
    for m in re.findall(r'(?:href|action|window\.location(?:\.href)?\s*=|location\.assign\()\s*[\'"]?[^\'"]*?([\w-]+\.html)', txt):
        linked.add(m)
print('== pages not in sidebar ==')
for p in sorted(pages - nav):
    tag = 'in-page-links' if p in linked else 'UNREACHABLE-except-direct-url'
    print(f'  {p:<40} {tag}')
print('== sidebar targets missing on disk ==', sorted(nav - pages - {'index.html'}) or 'none')
