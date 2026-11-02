import json
import urllib.request

with open('scratch/phase0_inventory.json', 'r', encoding='utf-8') as f:
    inventory = json.load(f)

print(f"Testing {len(inventory)} routes against http://127.0.0.1:3000 ...")

errors = []
success = 0

for item in inventory:
    path = item.get('path', '')
    url = f"http://127.0.0.1:3000/{path.replace('\\', '/')}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        if res.status == 200:
            success += 1
        else:
            errors.append((url, res.status))
    except Exception as e:
        errors.append((url, str(e)))

print(f"Results: {success}/{len(inventory)} pages returned 200 OK.")
if errors:
    print(f"Encountered {len(errors)} errors:")
    for u, err in errors:
        print(f"  {u}: {err}")
else:
    print("ALL 74 PAGES RETURNED 200 OK! Zero broken pages.")

