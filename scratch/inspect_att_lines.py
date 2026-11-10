with open('pages/admin/admin-attendance.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'openOverrideModal' in l:
        for j in range(max(0, i-5), min(len(lines), i+8)):
            print(f"{j+1}: {lines[j].strip()}")

