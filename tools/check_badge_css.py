with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.htb-ctrl-badge')
print(text[idx-50:idx+800])
