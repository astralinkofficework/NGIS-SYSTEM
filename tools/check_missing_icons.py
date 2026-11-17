import json

with open('data/sidebar_nav.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for portal_name, pdata in data['portals'].items():
    groups = pdata.get('groups', [])
    print(f"\n=================== PORTAL: {portal_name} ({len(groups)} groups) ===================")
    for g in groups:
        g_icon = g.get('icon')
        print(f"Group: '{g.get('label')}' (id: {g.get('id')}, group icon: '{g_icon}')")
        links = g.get('links', [])
        for l in links:
            icon = l.get('icon')
            if not icon or icon == 'null' or icon == 'none' or icon.strip() == '':
                print(f"   [MISSING ICON] id: '{l.get('id')}', label: '{l.get('label')}', href: '{l.get('href')}'")
            else:
                pass
