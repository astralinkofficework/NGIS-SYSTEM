"""Inspect real action-button markup so we can plan the SVG conversion."""
import glob, re, collections

pages = sorted(glob.glob('pages/**/*.html', recursive=True))

# 1. What container classes wrap action buttons?
wrap = collections.Counter()
# 2. How are row action buttons written? sample a few patterns
samples = collections.defaultdict(list)

mat_re = re.compile(r'<span[^>]*class="[^"]*material-symbols[^"]*"[^>]*>\s*([a-z_0-9-]+)\s*</span>', re.I)
ph_re = re.compile(r'<i[^>]*class="[^"]*\bph(?:-[a-z]+)?\s+ph-([a-z0-9-]+)[^"]*"[^>]*>\s*</i>', re.I)

for p in pages:
    s = open(p, encoding='utf-8').read()
    for m in mat_re.findall(s):
        wrap['material:' + m] += 1
    for m in ph_re.findall(s):
        wrap['phosphor:' + m] += 1

print('=== Icon-font glyph frequency (all pages) ===')
for k, v in wrap.most_common(80):
    print('%4d  %s' % (v, k))
