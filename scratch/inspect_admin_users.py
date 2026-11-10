with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('action-icon-btn')
if idx != -1:
    print("Found action-icon-btn:", text[idx-50:idx+300])
else:
    print("No action-icon-btn, searching for render or tbody in admin-users")
    idx2 = text.find('userTableBody')
    if idx2 != -1:
        print(text[idx2-50:idx2+600])

