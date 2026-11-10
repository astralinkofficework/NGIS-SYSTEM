with open('pages/admin/admin-grades.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('adminGradesTbody')
if idx != -1:
    print(text[idx-50:idx+900])

