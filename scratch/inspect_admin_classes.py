with open('pages/admin/admin-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('btn-edit-class')
if idx != -1:
    print(text[idx-100:idx+400])

