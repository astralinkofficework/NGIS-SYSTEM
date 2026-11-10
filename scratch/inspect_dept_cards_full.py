with open(r'pages\shared\department.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(''.join(lines[80:250]))

