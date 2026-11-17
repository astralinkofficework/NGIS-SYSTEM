import json

with open('data/sidebar_nav.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p, pdata in data['portals'].items():
    print(f"Portal: {p}, keys: {list(pdata.keys()) if isinstance(pdata, dict) else type(pdata)}")
    if isinstance(pdata, dict):
        for k, v in pdata.items():
            print(f"  {k}: {type(v)}, len: {len(v) if isinstance(v, (list, dict)) else v}")
            if isinstance(v, list) and len(v) > 0:
                print(f"    sample item: {v[0]}")
