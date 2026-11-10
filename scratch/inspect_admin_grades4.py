with open('pages/admin/admin-grades.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('pctStr')
if idx != -1:
    print(text[idx:idx+800])

