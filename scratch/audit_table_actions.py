import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
results = {}

for h in html_files:
    if '.kilo' in h or 'node_modules' in h or 'scratch' in h:
        continue
    with open(h, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    td_matches = re.findall(r'<td[^>]*>(.*?)</td>', content, re.DOTALL | re.IGNORECASE)
    actions_found = []
    for td in td_matches:
        if ('<button' in td or '<a' in td) and ('btn' in td or 'action' in td or 'onclick' in td or 'edit' in td.lower() or 'view' in td.lower() or 'delete' in td.lower() or 'download' in td.lower()):
            clean_td = ' '.join(td.split())
            if len(clean_td) < 500:
                actions_found.append(clean_td)
    if actions_found:
        results[h] = actions_found

print(f"HTML files with table action cells: {len(results)}")
for f, acts in sorted(results.items()):
    print(f"\n=== {f} ({len(acts)} action cells) ===")
    for a in acts[:3]:
        print(" ", a[:160])
