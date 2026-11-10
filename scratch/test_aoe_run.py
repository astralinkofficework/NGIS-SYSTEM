import sys
sys.path.insert(0, '.')
import admin_operations_engine as AOE

data = AOE.compute_operations_overview()
print("Success:", data["success"])
print("Summary:", data["summary"])
print("Cards count:", len(data["cards"]))
for c in data["cards"]:
    print(f"  [{c['id']}] {c['title']} -> {c['badge']} ({c['status']})")
print("Issues count:", len(data["issues"]))
print("Health services count:", len(data["system_health"]["services"]))
print("Audit activity count:", len(data["audit_activity"]))

