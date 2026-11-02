import os, re

pattern = re.compile(r'class=["\'][^"\']*(?:hamburger|menu-btn|toggle-sidebar)[^"\']*["\']|data-action=["\']toggle-sidebar["\']')

found = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()
            for idx, line in enumerate(lines):
                if pattern.search(line):
                    found.append((p, idx+1, line.strip()))

print(f"Total hamburger buttons found in pages: {len(found)}")
for p, l_no, line in found:
    print(f"{p}:{l_no} -> {line[:120]}")

