with open('pages/admin/admin-departments.html', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if '<h1' in line:
            print(f"admin-departments.html:{i}:")
            for j in range(max(0, i-3), min(len(lines), i+4)):
                print("  " + lines[j].strip())
