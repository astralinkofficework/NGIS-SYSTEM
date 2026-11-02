with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
terms = ['ripple', 'radial', 'circle', '::before', '::after', 'overlay', 'gradient', 'hover']
for t in terms:
    hits = len(re.findall(t, text, re.I))
    print(f"{t}: {hits} hits")

