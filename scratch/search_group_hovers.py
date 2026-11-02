import os
import re

html_files = []
for root, dirs, fnames in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']):
        continue
    for f in fnames:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

findings = []
for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Search for group-hover on backgrounds
    for m in re.finditer(r'class="([^"]*group-hover:bg-[^"]*)"', content):
        findings.append((p, 'group-hover:bg', m.group(1)))
    
    # Search for card elements with hover:bg-
    for m in re.finditer(r'class="([^"]*(?:card|ws-card|hub-card|dept-card|stat-card)[^"]*hover:bg-[^"]*)"', content):
        findings.append((p, 'card hover:bg', m.group(1)))

print(f'Total findings: {len(findings)}')
for p, kind, cls in findings:
    print(f'[{p}] {kind} -> {cls}')

