with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'pages/admin/admin-news.html' in line:
        for j in range(max(0, i-5), min(len(lines), i+15)):
            print(f"{j+1}: {repr(lines[j])}")
        break

