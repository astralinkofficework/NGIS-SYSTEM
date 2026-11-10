with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('viewTable')
if idx != -1:
    print(text[idx:idx+1500])

