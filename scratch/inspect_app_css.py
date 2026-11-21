import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"app.css has {len(lines)} lines")

# Let's inspect root tokens and button rules in app.css
for i, line in enumerate(lines[:120]):
    if any(k in line for k in ['--primary', '--bg', '--surface', '--accent', '.btn', '.badge', '.table', 'table']):
        print(f"{i+1:3d}: {line.strip()}")
