import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
configs = set()

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r'tailwind\.config\s*=\s*\{.*?\}\s*;?', content, re.DOTALL)
    for m in matches:
        if any(h in m for h in ['021024', '052659', '5483B3', '7DA0CA', 'C1E8FF', 'EAF6FF', 'DCE8F3']):
            configs.add(path)

print(f'{len(configs)} HTML files have blue colors inside tailwind.config:')
for p in sorted(configs):
    print(' ', p)

