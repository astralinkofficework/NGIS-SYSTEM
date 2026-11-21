import os
import re

attr_pattern = re.compile(r'\btitle\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)

matches = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                cleaned = re.sub(r'<title[^>]*>.*?</title>', '', content, flags=re.IGNORECASE | re.DOTALL)
                found = attr_pattern.findall(cleaned)
                if found:
                    matches.append((path, len(found), found))

print(f"Total HTML files with title attributes: {len(matches)}")
print(f"Total title attributes: {sum(m[1] for m in matches)}")
title_types = {}
for p, count, found in matches:
    for q, val in found:
        title_types[val] = title_types.get(val, 0) + 1

sorted_titles = sorted(title_types.items(), key=lambda x: x[1], reverse=True)
print("Top 15 title attribute values:")
for val, count in sorted_titles[:15]:
    print(f"  '{val}': {count}")
