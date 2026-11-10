with open('pages/admin/admin-services.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'openModal' in l and 'tbody' not in l:
        for j in range(max(0, i-4), min(len(lines), i+8)):
            print(f"{j+1}: {lines[j].strip()}")
        print("---")

