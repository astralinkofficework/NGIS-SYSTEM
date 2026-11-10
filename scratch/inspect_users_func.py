with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// 5. Actions column')
if idx != -1:
    print(text[idx:idx+2500])
