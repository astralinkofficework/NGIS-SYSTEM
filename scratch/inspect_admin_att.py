with open('pages/admin/admin-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('openOverrideModal')
if idx != -1:
    print(text[idx-100:idx+400])

