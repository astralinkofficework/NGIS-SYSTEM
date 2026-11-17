import json

with open('tools/discovery_audit_results.json', encoding='utf-8') as f:
    d = json.load(f)

dups = d.get('duplicate_tags', [])
print("Type of duplicate_tags:", type(dups))
if isinstance(dups, dict):
    for k, v in dups.items():
        print(f"File: {k}")
        print(f"  {v}")
elif isinstance(dups, list):
    for item in dups:
        print(item)
