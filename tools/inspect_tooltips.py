import glob
import re

sample_titles = []
for p in glob.glob('pages/**/*.html', recursive=True):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    for m in re.finditer(r'<([a-zA-Z0-9]+)[^>]*\btitle=["\']([^"\']+)["\'][^>]*>', text):
        tag = m.group(1).lower()
        if tag == 'head' or tag == 'title':
            continue
        sample_titles.append((p, tag, m.group(2), m.group(0)[:120]))

print(f"Total HTML elements with title attribute: {len(sample_titles)}")
for p, tag, title, snippet in sample_titles[:15]:
    print(f"[{tag}] {title} | File: {p}")
