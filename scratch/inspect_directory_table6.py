with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind('pagesTableBody.innerHTML')
if idx != -1:
    print(text[idx-600:idx+50])

