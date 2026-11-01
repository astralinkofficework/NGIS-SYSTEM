with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('DISCIPLINE GROUP')
print(text[idx-200:idx+600].encode('ascii', errors='replace').decode('ascii'))

