"""Wire the global action-icon engine into every portal page.

Idempotent: skips a page that already contains the marker.
Injects, just before </head>:
  <link .../action-icons.css>
  <script .../action-icons.js defer>
Path prefix is computed from each file's depth relative to the repo root.
"""
import glob, os, re

MARK = '<!-- NGIS global action-icon engine -->'
pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']

changed, skipped = [], []
for p in pages:
    s = open(p, encoding='utf-8').read()
    if MARK in s:
        skipped.append(p)
        continue
    depth = p.replace('\\', '/').count('/')  # pages/admin/x.html -> 2
    prefix = '../' * depth if depth else './'
    block = (
        '\n%s\n<link rel="stylesheet" href="%sassets/css/action-icons.css">\n'
        '<script src="%sassets/js/action-icons.js" defer></script>\n'
        % (MARK, prefix, prefix)
    )
    # insert before </head> (last occurrence to stay inside head)
    idx = s.lower().rfind('</head>')
    if idx == -1:
        print('!! no </head> in', p); continue
    new = s[:idx] + block + s[idx:]
    open(p, 'w', encoding='utf-8').write(new)
    changed.append((p, prefix))

print('Wired %d pages, skipped %d already-done.' % (len(changed), len(skipped)))
from collections import Counter
print('Prefix usage:', Counter(pref for _, pref in changed))
if skipped:
    print('Skipped:', skipped[:10])
