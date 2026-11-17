import os, re

qs_dynamic = re.compile(r'(querySelector|querySelectorAll|closest|matches)\s*\(\s*([^)]*[\+\$][^)]*)\)')

matches = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.js') or file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, 1):
                    m = qs_dynamic.search(line)
                    if m:
                        matches.append((path, line_no, m.group(1), m.group(2).strip(), line.strip()))

print(f"Total dynamic querySelector matches: {len(matches)}")
for path, line_no, fn, arg, line in matches:
    print(f"{path}:{line_no} [{fn}]: {arg}")
