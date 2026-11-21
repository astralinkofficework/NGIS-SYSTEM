with open('assets/js/sticky-layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function updateStickiness')
print(text[idx-200:idx+2500])
