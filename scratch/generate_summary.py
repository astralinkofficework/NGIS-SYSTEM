import json

with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    sheets = json.load(f)

with open('scratch/summary_utf8.txt', 'w', encoding='utf-8') as out:
    for sname, rows in sheets.items():
        out.write(f"================ SHEET: {sname} ================\n")
        count = 0
        for r in rows:
            non_empty = [f"[{i}]: {c}" for i, c in enumerate(r['cells']) if str(c).strip()]
            if non_empty:
                out.write(f"R{r['row_idx']}: " + " | ".join(non_empty[:15]) + "\n")
                count += 1
                if count >= 12:
                    break
        out.write("\n")
print("Summary written")
