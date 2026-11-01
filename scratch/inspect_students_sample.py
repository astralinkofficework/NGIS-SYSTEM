import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    raw_sheets = json.load(f)

def inspect_sheet_students(sname):
    rows = raw_sheets[sname]
    print(f"\n--- {sname} ---")
    for idx, r in enumerate(rows):
        cells = r['cells']
        # Find where student row starts
        if len(cells) > 2 and str(cells[0]).replace('.0', '').isdigit():
            num = int(float(cells[0]))
            print(f"  Row {idx}: No={num}, Col1={cells[1] if len(cells)>1 else ''}, Col2={cells[2] if len(cells)>2 else ''}, Col3={cells[3] if len(cells)>3 else ''}, Col4={cells[4] if len(cells)>4 else ''}, Col5={cells[5] if len(cells)>5 else ''}")
        elif any('Total' in str(c) for c in cells):
            print(f"  End at Row {idx}: {[c for c in cells if str(c).strip()]}")

for s in ['ម.ត ក រសៀល', '១ក វេនព្រឹក', '១០ក ព្រឹក', '១២ក ព្រឹក']:
    inspect_sheet_students(s)
