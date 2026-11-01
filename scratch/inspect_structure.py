import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for sname, rows in data.items():
    if sname in ['All Class', 'បំប៉ន', 'New', 'Stop May 2024', 'Transfer', 'Stop', 'Transfer to C2', 'Hold', '១២ក ព្រឹកចាស់']:
        print(f"Special Sheet: {sname}, rows: {len(rows)}")
        continue
    # Regular class sheet
    print(f"=== Sheet: {sname} ===")
    for r in rows[:10]:
        cells = [c for c in r['cells'] if str(c).strip()]
        if cells:
            print(f"  Row {r['row_idx']}: {cells[:10]}")
    print()
