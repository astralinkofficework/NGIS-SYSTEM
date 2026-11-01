import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    sheets = json.load(f)

print("All Class rows:")
for r in sheets['All Class'][:40]:
    non_empty = [f"[{i}]: {c}" for i, c in enumerate(r['cells']) if str(c).strip()]
    if non_empty:
        print(f"R{r['row_idx']}: " + " | ".join(non_empty))
