with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\w+):\s*\{[^}]*groups:\s*\[(.*?)\n\s*\]\s*\}', text, re.DOTALL)
for role, groups_text in matches:
    ph_icons = re.findall(r'icon:\s*["\'](ph[^"\']+)["\']', groups_text)
    if ph_icons:
        print(f"Role {role} has ph icons:", ph_icons)

