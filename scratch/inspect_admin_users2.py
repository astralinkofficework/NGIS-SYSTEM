with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderUsers')
if idx == -1:
    idx = text.find('renderTable')
if idx == -1:
    idx = text.find('users.map')
if idx != -1:
    print(text[idx:idx+1500])
else:
    print("Not found, searching 'user-row'")
    idx2 = text.find('user-row')
    if idx2 != -1:
        print(text[idx2-50:idx2+600])

