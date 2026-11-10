with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('pagesTableBody')
if idx != -1:
    print(text[idx-50:idx+800])

