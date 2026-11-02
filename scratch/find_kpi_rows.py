import glob
import re

for cf in glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True):
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    if 'dash-kpi-row' in text or 'dash-quick-row' in text:
        print(f"Found in {cf}:")
        for m in re.findall(r'([^{}]*(?:dash-kpi-row|dash-quick-row)[^{}]*\{[^}]*\})', text):
            cleaned = m.strip().encode('ascii', errors='replace').decode('ascii')
            print(" ", cleaned[:100].replace('\n', ' '))

