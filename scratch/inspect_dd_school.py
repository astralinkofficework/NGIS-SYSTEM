import json

with open("data/data_dictionary.json", "r", encoding="utf-8") as f:
    dd = json.load(f)

print("Campuses in data_dictionary:")
print(json.dumps(dd.get("school", {}).get("campuses", []), indent=2))

print("\nDepartments in data_dictionary:")
print(json.dumps(dd.get("school", {}).get("departments", []), indent=2))

print("\nGrade Levels in data_dictionary:")
print(json.dumps(dd.get("school", {}).get("gradeLevels", []), indent=2))

