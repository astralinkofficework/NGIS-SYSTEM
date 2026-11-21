with open('assets/js/hero.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('nav')
while idx != -1:
    snippet = text[max(0, idx-50):min(len(text), idx+200)]
    if 'hero-nav' in snippet or 'topbar' in snippet or 'navbar' in snippet or '<header' in snippet or '<nav' in snippet:
        print(f"--- match at {idx} ---")
        print(snippet)
        print("\n")
    idx = text.find('nav', idx+1)
