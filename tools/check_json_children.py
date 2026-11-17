import json

with open('data/sidebar_nav.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for portal, pdata in data['portals'].items():
    for g in pdata.get('groups', []):
        for l in g.get('links', []):
            if l.get('children'):
                print(f"[{portal}] Dropdown '{l.get('label')}' (id: {l.get('id')}) has {len(l['children'])} children:")
                for c in l['children']:
                    print(f"   - {c.get('label')} (id: {c.get('id')}, icon: {c.get('icon')})")
