import os

all_html = []
missing_header = []

for root, dirs, files in os.walk('.'):
    # ignore node_modules, .git, .system_generated
    if any(ignore in root for ignore in ['.git', 'node_modules', '.system_generated', '.agents']):
        continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f).replace('\\', '/')
            all_html.append(p)
            with open(p, 'r', encoding='utf-8') as fp:
                txt = fp.read()
            if '<header' not in txt:
                missing_header.append(p)

print(f"Total HTML files found: {len(all_html)}")
print(f"Total missing <header>: {len(missing_header)}")
for m in missing_header:
    print(f"  Missing: {m}")

