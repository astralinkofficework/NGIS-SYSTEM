import os
import re
import json

pages = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            pages.append(os.path.join(root, f).replace('\\', '/'))

print(f"Total HTML pages found: {len(pages)}")

modal_findings = {}
tab_findings = {}
drawer_findings = {}

for p in pages:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        
        # Modals
        m_ids = re.findall(r'id=["\']([^"\']*(?:modal|dialog)[^"\']*)["\']', content, re.I)
        m_classes = re.findall(r'class=["\']([^"\']*(?:modal|dialog)[^"\']*)["\']', content, re.I)
        if m_ids or m_classes:
            modal_findings[p] = {
                'ids': sorted(list(set(m_ids))),
                'classes': sorted(list(set(m_classes)))[:5]
            }

        # Tabs
        tabs = re.findall(r'id=["\']([^"\']*(?:tab)[^"\']*)["\']', content, re.I)
        tab_roles = re.findall(r'role=["\']tab(?:list)?["\']', content, re.I)
        if tabs or tab_roles:
            tab_findings[p] = {
                'ids': sorted(list(set(tabs)))[:10],
                'count': len(tabs) + len(tab_roles)
            }

        # Drawers / Side Panels
        d_ids = re.findall(r'id=["\']([^"\']*(?:drawer|side-panel|slideover|sheet|detail-panel)[^"\']*)["\']', content, re.I)
        if d_ids:
            drawer_findings[p] = sorted(list(set(d_ids)))
    except Exception as e:
        print(f"Error scanning {p}: {e}")

print(f"Pages with modals: {len(modal_findings)}")
print(f"Pages with tabs: {len(tab_findings)}")
print(f"Pages with drawers: {len(drawer_findings)}")

inventory = {
    'summary': {
        'total_pages': len(pages),
        'pages_with_modals': len(modal_findings),
        'pages_with_tabs': len(tab_findings),
        'pages_with_drawers': len(drawer_findings)
    },
    'modals': modal_findings,
    'tabs': tab_findings,
    'drawers': drawer_findings
}

with open('tools/component_scan_raw.json', 'w', encoding='utf-8') as f:
    json.dump(inventory, f, indent=2)

print("Scan complete! Output written to tools/component_scan_raw.json")
