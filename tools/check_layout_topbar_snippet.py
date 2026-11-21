with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<header class="topbar"')
print(text[idx-100:idx+800])
