import os, re

space_in_classlist = re.compile(r'classList\.(add|remove|toggle)\s*\(\s*[\'"][^\'"]*\s+[^\'"]*[\'"]')

matches = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain']):
        continue
    for file in files:
        if file.endswith('.js') or file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, 1):
                    m = space_in_classlist.search(line)
                    if m:
                        matches.append((path, line_no, line.strip()))

print(f'Total matches found: {len(matches)}')
for path, line_no, line in matches:
    print(f'{path}:{line_no}: {line}')
