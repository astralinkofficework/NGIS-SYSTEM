import json

with open("data/data_dictionary.json", "r", encoding="utf-8") as f:
    dd = json.load(f)

print("data_dictionary keys:", list(dd.keys()))
for k in dd.keys():
    if isinstance(dd[k], list):
        print(f"  {k}: {len(dd[k])} items")
        if dd[k]:
            print(f"    sample: {list(dd[k][0].keys()) if isinstance(dd[k][0], dict) else dd[k][0]}")
    elif isinstance(dd[k], dict):
        print(f"  {k}: {list(dd[k].keys())}")

