import glob
import re
from collections import Counter

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
js_files = glob.glob('assets/js/*.js') + glob.glob('assets/components/*.js')
css_files = glob.glob('assets/css/*.css')

print(f"Scanning {len(html_files)} HTML, {len(js_files)} JS, {len(css_files)} CSS files.")

color_classes = Counter()
gradients = Counter()
badge_classes = Counter()
button_classes = Counter()
hex_colors = Counter()

color_re = re.compile(r'\b(bg|text|border)-(blue|purple|indigo|pink|violet|fuchsia|cyan|teal|amber|orange|emerald|rose|red|yellow|lime|sky)-([0-9]{2,3})\b')
grad_re = re.compile(r'bg-gradient-[^\s"\'<>]+|linear-gradient\([^)]+\)')
badge_re = re.compile(r'class=["\'][^"\']*\b(badge|chip|pill|tag|status)\b[^"\']*["\']')
btn_re = re.compile(r'class=["\'][^"\']*\b(btn|button)\b[^"\']*["\']')
hex_re = re.compile(r'#[0-9a-fA-F]{3,8}\b')

for fpath in html_files + js_files:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        continue

    for m in color_re.finditer(content):
        color_classes[m.group(0)] += 1
    for m in grad_re.finditer(content):
        gradients[m.group(0)] += 1
    for m in badge_re.finditer(content):
        badge_classes[m.group(0)] += 1
    for m in btn_re.finditer(content):
        button_classes[m.group(0)] += 1
    for m in hex_re.finditer(content):
        hex_colors[m.group(0).upper()] += 1

print("\n=== TOP 40 TAILWIND COLOR UTILITIES ===")
for k, v in color_classes.most_common(40):
    print(f"  {k:20}: {v}")

print("\n=== TOP 20 HEX COLORS ===")
for k, v in hex_colors.most_common(20):
    print(f"  {k:10}: {v}")

print("\n=== TOP GRADIENTS ===")
for k, v in gradients.most_common(10):
    print(f"  {k[:50]:50}: {v}")

print("\n=== UNIQUE BADGE PATTERNS ===")
sample_badges = [b for b, _ in badge_classes.most_common(20)]
for b in sample_badges:
    print(f"  {b[:90]}")
