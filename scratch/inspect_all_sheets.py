import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    sheets = json.load(f)

for sname, rows in sheets.items():
    print(f"================ SHEET: {sname} ================")
    # Print non-empty rows up to 15
    count = 0
    for r in rows:
        non_empty = [f"[{i}]: {c}" for i, c in enumerate(r['cells']) if str(c).strip()]
        if non_empty:
            print(f"R{r['row_idx']}: " + " | ".join(non_empty[:15]))
            count += 1
            if count >= 12:
                break
    print()
