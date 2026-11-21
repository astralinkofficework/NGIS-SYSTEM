with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind('hydrate')
print("Last hydrate occurrences:", idx)
print(text[idx-200:idx+400])
