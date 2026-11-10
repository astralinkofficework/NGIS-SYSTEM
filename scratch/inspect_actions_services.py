with open('pages/principal/principal-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('let actionsHtml =')
if idx != -1:
    print(text[idx:idx+1200])

