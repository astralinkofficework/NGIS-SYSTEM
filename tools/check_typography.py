import os
import re

css_weight_re = re.compile(r'font-weight\s*:\s*(?:700|800|900|bold|bolder)', re.IGNORECASE)
tw_bold_re = re.compile(r'\b(?:font-bold|font-extrabold|font-black)\b')

violations = []

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'tools', '.system_generated']):
        continue
    for file in files:
        if file.endswith(('.html', '.css', '.js')):
            path = os.path.normpath(os.path.join(root, file))
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if 'rule: no bold' in line.lower() or 'avoid' in line.lower() or 'agents.md' in line.lower():
                            continue
                        if css_weight_re.search(line):
                            violations.append((path, i + 1, 'css_weight', line.strip()))
                        elif tw_bold_re.search(line):
                            violations.append((path, i + 1, 'tailwind_bold', line.strip()))
            except Exception:
                pass

print(f"Total potential heavy weight instances found: {len(violations)}")
for v in violations[:30]:
    print(f"{v[0]}:{v[1]} [{v[2]}] {v[3][:80]}")
