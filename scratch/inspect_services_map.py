with open('pages/principal/principal-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('filtered.map(r =>')
if idx != -1:
    print(text[idx:idx+2500])

