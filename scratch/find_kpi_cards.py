import glob

for cf in glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True):
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    if 'dash-kpi-card' in text or 'dash-quick-btn' in text:
        print(f"Found in {cf}")

