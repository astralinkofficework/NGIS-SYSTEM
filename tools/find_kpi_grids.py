import os, re

kpi_grid_re = re.compile(r'grid-cols-1\s+sm:grid-cols-2\s+lg:grid-cols-4')

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as fp:
                for i, line in enumerate(fp, 1):
                    if kpi_grid_re.search(line):
                        print(f"{path}:{i}: {line.strip()[:100]}")
