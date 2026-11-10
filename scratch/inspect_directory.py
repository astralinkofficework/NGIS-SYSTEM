with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('esc(p.path)')
if idx != -1:
    print(text[idx-100:idx+400])

