import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    sheets = json.load(f)

for sname in ['បំប៉ន', 'Stop May 2024', 'Transfer', 'Stop', 'Transfer to C2', 'Hold']:
    rows = sheets.get(sname, [])
    print(f"=== Sheet: {sname} (total {len(rows)} rows) ===")
    for r in rows[:15]:
        non_empty = [f"[{i}]: {c}" for i, c in enumerate(r['cells']) if str(c).strip()]
        if non_empty:
            print(f"  R{r['row_idx']}: " + " | ".join(non_empty[:12]))
