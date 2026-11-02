with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
selectors = ['dash-kpi-row', 'dash-quick-row', 'ov-inner-grid', 'ov-feed-panel', 'id-modal-overlay', 'id-card-wrapper']
for s in selectors:
    print(f"=== Rules for {s} ===")
    matches = re.findall(rf'([^{{}}]*{s}[^{{}}]*\{{[^}}]*\}})', text)
    for m in matches:
        cleaned = m.strip().encode('ascii', errors='replace').decode('ascii')
        print(cleaned[:120].replace('\n', ' '))

