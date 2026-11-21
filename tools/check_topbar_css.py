with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.hero-topbar')
while idx != -1:
    print("Match at", idx)
    print(text[idx:idx+600])
    print("=" * 40)
    idx = text.find('.hero-topbar', idx+1)
