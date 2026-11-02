import os, re

with open('scratch/find_hamburgers.py', 'r') as f:
    pass

import json
with open('scratch/phase0_inventory.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

pattern = re.compile(r'class=["\'][^"\']*(?:hamburger|menu-btn|toggle-sidebar)[^"\']*["\']|data-action=["\']toggle-sidebar["\']')

for page in pages:
    p = page['path']
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
    for idx, line in enumerate(lines):
        if pattern.search(line):
            start = max(0, idx - 4)
            end = min(len(lines), idx + 5)
            print(f"=== {p}:{idx+1} ===")
            for j in range(start, end):
                print(f"  {lines[j].strip()[:90]}")
            print()

