with open('pages/admin/admin-grade-release.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('btn-authorize')
if idx != -1:
    print(text[idx-200:idx+600])

