import glob, re

pages = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
pattern = re.compile(r'class=["\'][^"\']*flex-col\s+(?:sm|md|lg):flex-row[^"\']*["\']')

affected = []
for p in pages:
    if 'node_modules' in p:
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    matches = pattern.findall(content)
    if matches:
        affected.append((p, len(matches), matches[0]))

print(f'Total affected files with flex-col (sm/md/lg):flex-row: {len(affected)}')
for p, count, m in affected:
    print(f'{p:<50} ({count} matches): {m[:80]}')
