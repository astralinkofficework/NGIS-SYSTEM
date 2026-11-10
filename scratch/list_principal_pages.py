import json

with open("all_pages_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total pages: {len(data)}")
for p in data:
    path = p.get("path", "") or p.get("file", "") or p.get("url", "")
    if "principal" in str(p):
        print(p.get("title"), "::", p.get("path"), "::", p.get("file"))
