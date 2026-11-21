import glob
import re
from collections import Counter

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
js_files = glob.glob('assets/js/*.js')

colored_containers = Counter()
colored_borders = Counter()
inline_bg_cards = []

container_re = re.compile(r'<div[^>]*class=["\']([^"\']*\b(?:card|panel|box|widget|section|banner)\b[^"\']*)["\']', re.IGNORECASE)
color_bg_re = re.compile(r'\b(?:bg-(?:blue|purple|indigo|amber|rose|pink|cyan|violet|emerald)-[0-9]{2,3})\b')
border_re = re.compile(r'\b(?:border-(?:blue|purple|indigo|amber|rose|pink|cyan|violet)-[0-9]{2,3})\b')
inline_bg_re = re.compile(r'<div[^>]*style=["\'][^"\']*background(?:-color)?:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\))[^"\']*["\']')

for hf in html_files:
    # ignore timetable builders which legitimately have subject cells
    is_tt = 'timetable' in hf.lower()
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for m in container_re.finditer(content):
        cls = m.group(1)
        colors = color_bg_re.findall(cls)
        if colors:
            colored_containers[f"{hf} -> {colors} in {cls[:50]}"] += 1
            
    for m in border_re.finditer(content):
        colored_borders[m.group(0)] += 1
        
    if not is_tt:
        for m in inline_bg_re.finditer(content):
            val = m.group(1).upper()
            if val not in ['#FFFFFF', '#F7F9F7', '#FFFFFF;', '#F7F9F7;', 'TRANSPARENT']:
                inline_bg_cards.append((hf, val, m.group(0)[:80]))

print(f"\n--- COLORED CONTAINERS FOUND: {len(colored_containers)} ---")
for k, v in colored_containers.most_common(15):
    print(f"  {k}")

print(f"\n--- COLORED BORDER CLASSES: {len(colored_borders)} ---")
for k, v in colored_borders.most_common(10):
    print(f"  {k}: {v}")

print(f"\n--- NON-NEUTRAL INLINE CARD BACKGROUNDS (SAMPLE): {len(inline_bg_cards)} ---")
for hf, val, tag in inline_bg_cards[:15]:
    print(f"  {hf} [{val}]: {tag}")
