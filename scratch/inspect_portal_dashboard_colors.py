with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
color_re = re.compile(r'#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)')

for i, line in enumerate(lines):
    colors = color_re.findall(line)
    for c in colors:
        c_upper = c.upper()
        if any(c_upper.startswith(k) for k in ['RGBA(36, 85, 214', '#2455D6', '#1E40AF', '#3B82F6', '#8B5CF6', '#EC4899']):
            print(f"Line {i+1:4d}: {line.strip()[:90]}")
