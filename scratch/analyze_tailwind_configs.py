import glob
import re

files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
configs = []
for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    m = re.search(r'tailwind\.config\s*=\s*\{.*?\n\s*\};?', c, re.DOTALL)
    if m:
        configs.append((f, m.group(0)))

print(f"Found {len(configs)} tailwind.config blocks")
color_map = {}
for f, cfg in configs:
    pairs = re.findall(r'["\']([a-zA-Z0-9_\-]+)["\']\s*:\s*["\'](#[0-9a-fA-F]{3,8})["\']', cfg)
    for k, v in pairs:
        if k not in color_map:
            color_map[k] = set()
        color_map[k].add(v.upper())

for k, vals in sorted(color_map.items()):
    print(f"{k}: {vals}")

