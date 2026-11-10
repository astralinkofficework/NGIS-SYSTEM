import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
search_inputs = []

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.finditer(r'<input[^>]*placeholder=["\'][^"\']*[Ss]earch[^"\']*["\'][^>]*>', content)
    for m in matches:
        tag = m.group(0)
        # Check if it has an icon before it without pl-10 / pl-11 / 44px
        search_inputs.append((path, tag))

print(f'Total search inputs found: {len(search_inputs)}')
for p, tag in search_inputs[:15]:
    print(f'{p}:')
    print('  ', tag[:120])

