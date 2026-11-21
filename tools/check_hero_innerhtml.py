with open('assets/js/hero.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('placeholder.innerHTML = html')
print("After innerHTML in hero.js:")
print(text[idx:idx+1500])
