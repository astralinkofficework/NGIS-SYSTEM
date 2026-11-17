import os, re

case_attr_re = re.compile(r'\[[a-zA-Z0-9_\-]+[~\|\^\$\*]?=[\'"][^\'"]*[\'"]\s+i\]')

matches = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.js') or file.endswith('.html') or file.endswith('.css'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, 1):
                    m = case_attr_re.search(line)
                    if m:
                        matches.append((path, line_no, m.group(0), line.strip()))

print(f"Total case-insensitive attribute selector matches: {len(matches)}")
for path, line_no, mat, line in matches:
    print(f"{path}:{line_no}: {mat} => {line}")
