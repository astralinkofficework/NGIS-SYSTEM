with open('pages/admin/admin-grade-release.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'btn-authorize' in l:
        for j in range(max(0, i-5), min(len(lines), i+8)):
            print(f"{j+1}: {lines[j].strip()}")
        print("---")

