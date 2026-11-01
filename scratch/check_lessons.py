with open('pages/shared/lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('window.PAGE')
print(text[max(0, idx-300):min(len(text), idx+300)].encode('ascii', errors='replace').decode('ascii'))

