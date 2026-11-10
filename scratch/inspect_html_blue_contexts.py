import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
pattern = re.compile(r'([^\s"\'<>{};()]+)?(#[0-9a-fA-F]{6}|#021024|#052659|#5483B3|#7DA0CA|#C1E8FF|#EAF6FF|#DCE8F3)([^\s"\'<>{};()]+)?', re.IGNORECASE)

contexts = {}
for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for match in re.finditer(r'(#[0-9a-fA-F]{6})', content, re.IGNORECASE):
        hex_val = match.group(1).upper()
        if hex_val in ['#021024', '#052659', '#5483B3', '#7DA0CA', '#C1E8FF', '#EAF6FF', '#DCE8F3']:
            start = max(0, match.start() - 25)
            end = min(len(content), match.end() + 25)
            snippet = content[start:end].replace('\n', ' ')
            contexts.setdefault(hex_val, set()).add(snippet[:70])

for hex_val, samples in contexts.items():
    print(f'=== {hex_val} ({len(samples)} distinct contexts) ===')
    for s in list(samples)[:5]:
        print('  ', s)

