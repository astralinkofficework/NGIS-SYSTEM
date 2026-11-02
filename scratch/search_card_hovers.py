import os, re

files = []
for root, dirs, fnames in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']):
        continue
    for f in fnames:
        if f.endswith('.html'):
            files.append(os.path.join(root, f))

findings = []
for path in files:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Look for group and group-hover:bg-
    for m in re.finditer(r'<[a-zA-Z0-9\-]+[^>]*class="[^"]*\bgroup\b[^"]*"[^>]*>[\s\S]*?group-hover:bg-([^"\'\s>]+)', content):
        findings.append((path, 'group-hover:bg-' + m.group(1), m.group(0)[:120]))
    
    # 2. Look for cards with hover:bg-
    for m in re.finditer(r'<[a-zA-Z0-9\-]+[^>]*class="[^"]*(?:card|ws-card|stat|panel|module|hub)[^"]*\bhover:bg-([^"\'\s>]+)[^"]*"', content):
        findings.append((path, 'card hover:bg-' + m.group(1), m.group(0)[:120]))

    # 3. Look for inline styles with hover or radial or ripple
    for m in re.finditer(r'style="[^"]*(?:radial|ripple|gradient)[^"]*"', content):
        findings.append((path, 'inline style', m.group(0)))

print(f'Total findings: {len(findings)}')
for p, kind, snip in findings:
    print(f'[{p}] {kind} -> {snip}')

