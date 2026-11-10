with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'openDetailModal(item.id)' in l or 'openHandoverModal' in l:
        for j in range(max(0, i-4), min(len(lines), i+8)):
            print(f"{j+1}: {lines[j].strip()}")
        print("---")

