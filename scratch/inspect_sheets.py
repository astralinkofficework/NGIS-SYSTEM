import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Sheet list:")
for name in data:
    print(f"  {name}: {len(data[name])} rows")

first_sheet_name = list(data.keys())[0]
print(f"\n--- First 15 rows of {first_sheet_name} ---")
for r in data[first_sheet_name][:15]:
    row_vals = [f"col{i}: {c}" for i, c in enumerate(r['cells']) if str(c).strip()]
    print(f"Row {r['row_idx']}: {row_vals}")

if 'All Class' in data:
    print("\n--- All Class rows ---")
    for r in data['All Class'][:30]:
        row_vals = [f"col{i}: {c}" for i, c in enumerate(r['cells']) if str(c).strip()]
        if row_vals:
            print(f"Row {r['row_idx']}: {row_vals}")
