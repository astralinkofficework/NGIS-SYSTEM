import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/all_sheets.json', 'r', encoding='utf-8') as f:
    sheets = json.load(f)

all_class_rows = sheets['All Class']

print("All Class entries:")
for r in all_class_rows:
    cells = r['cells']
    if len(cells) > 6 and str(cells[0]).replace('.0', '').isdigit():
        idx = int(float(cells[0]))
        c_name = cells[1] if len(cells) > 1 else ''
        room = cells[2] if len(cells) > 2 else ''
        students = cells[3] if len(cells) > 3 else ''
        t_kh = cells[6] if len(cells) > 6 else ''
        t_zh = cells[7] if len(cells) > 7 else ''
        t_gender = cells[8] if len(cells) > 8 else ''
        sched = cells[9] if len(cells) > 9 else ''
        print(f"[{idx}] {c_name} | Rm: {room} | Students: {students} | Teacher: {t_kh} ({t_zh}) | {sched}")
