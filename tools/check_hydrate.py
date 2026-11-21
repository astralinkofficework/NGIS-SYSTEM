with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function hydrate(')
if idx == -1:
    idx = text.find('hydrate =')
if idx == -1:
    idx = text.find('hydrate')
print("hydrate idx:", idx)
print(text[idx:idx+1500])
