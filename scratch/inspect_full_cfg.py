import json

with open("data/system_configuration.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

for k, v in cfg.items():
    if isinstance(v, list):
        print(f"Key: {k} (list of {len(v)} items)")
        if v:
            print("  Item sample:", list(v[0].keys()) if isinstance(v[0], dict) else type(v[0]))
    elif isinstance(v, dict):
        print(f"Key: {k} (dict with {len(v)} keys)")
        print("  Keys:", list(v.keys()))
    else:
        print(f"Key: {k} ({type(v)})")

