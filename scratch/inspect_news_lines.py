with open('pages/admin/admin-news.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'deletePost' in l:
        for j in range(max(0, i-4), min(len(lines), i+8)):
            print(f"{j+1}: {lines[j].strip()}")
        print("---")

