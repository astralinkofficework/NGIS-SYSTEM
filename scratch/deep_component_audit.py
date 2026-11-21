import glob
import re
from collections import defaultdict

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
js_files = glob.glob('assets/js/*.js') + glob.glob('assets/components/*.js')

print(f"Auditing {len(html_files)} HTML pages...")

# 1. Button variants
buttons_by_class = defaultdict(list)
button_re = re.compile(r'<(?:button|a)\s+[^>]*class=["\']([^"\']*\b(?:btn|button|action-btn)[^"\']*)["\']', re.IGNORECASE)

for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for m in button_re.finditer(content):
        cls_str = " ".join(sorted(set(m.group(1).split())))
        buttons_by_class[cls_str].append(hf)

print(f"\n--- BUTTON VARIANTS FOUND: {len(buttons_by_class)} ---")
for cls, files in sorted(buttons_by_class.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
    print(f"  [{len(files)} occurrences] {cls[:80]}")

# 2. Badges / Chips / Pills
badge_tags = defaultdict(list)
badge_tag_re = re.compile(r'<(\w+)\s+[^>]*class=["\']([^"\']*\b(?:badge|chip|pill|tag|status-indicator)\b[^"\']*)["\'][^>]*>(.*?)</\1>', re.IGNORECASE | re.DOTALL)

for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for m in badge_tag_re.finditer(content):
        tag, cls, text = m.group(1), m.group(2), m.group(3)
        # clean text
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        if len(clean_text) < 40:
            badge_tags[cls].append((clean_text, hf))

print(f"\n--- BADGE / CHIP PATTERNS FOUND: {len(badge_tags)} ---")
for cls, examples in sorted(badge_tags.items(), key=lambda x: len(x[1]), reverse=True)[:20]:
    ex_texts = list(set(t for t, _ in examples))[:3]
    print(f"  [{len(examples)}] '{cls[:60]}' -> {ex_texts}")

# 3. Table styling
table_re = re.compile(r'<table\s+[^>]*class=["\']([^"\']*)["\']', re.IGNORECASE)
tables_found = defaultdict(list)
for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for m in table_re.finditer(content):
        tables_found[m.group(1)].append(hf)

print(f"\n--- TABLE CLASSES FOUND: {len(tables_found)} ---")
for cls, files in sorted(tables_found.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
    print(f"  [{len(files)}] {cls[:70]}")

# 4. Metric / Stat Card styling
card_re = re.compile(r'class=["\']([^"\']*\b(?:kpi|stat-card|metric-card|ov-kpi|analytics-card|summary-card)\b[^"\']*)["\']', re.IGNORECASE)
cards_found = defaultdict(list)
for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for m in card_re.finditer(content):
        cards_found[m.group(1)].append(hf)

print(f"\n--- METRIC / STAT CARD CLASSES FOUND: {len(cards_found)} ---")
for cls, files in sorted(cards_found.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
    print(f"  [{len(files)}] {cls[:70]}")
