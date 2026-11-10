with open('pages/admin/admin-campus.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('link-btn')
if idx != -1:
    print(text[idx-200:idx+600])

