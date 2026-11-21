with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('hydrate()')
while idx != -1:
    print(text[max(0, idx-50):min(len(text), idx+150)])
    print("-" * 30)
    idx = text.find('hydrate()', idx+1)
