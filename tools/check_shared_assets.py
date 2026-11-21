import glob, re

scripts = {}
links = {}
for h in glob.glob('pages/**/*.html', recursive=True):
    with open(h, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    for s in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', t):
        s_clean = s.split('?')[0].split('/')[-1]
        scripts[s_clean] = scripts.get(s_clean, 0) + 1
    for l in re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', t):
        if 'css' in l:
            l_clean = l.split('?')[0].split('/')[-1]
            links[l_clean] = links.get(l_clean, 0) + 1

print('Top scripts loaded in pages:')
for s, c in sorted(scripts.items(), key=lambda x: -x[1])[:15]:
    print(f'  {s}: {c} pages')

print('\nTop CSS loaded in pages:')
for l, c in sorted(links.items(), key=lambda x: -x[1])[:15]:
    print(f'  {l}: {c} pages')
