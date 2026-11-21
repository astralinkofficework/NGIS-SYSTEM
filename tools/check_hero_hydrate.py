with open('assets/js/hero.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('hydrate')
if idx != -1:
    print("Found hydrate in hero.js:")
    print(text[idx-50:idx+400])
else:
    print("NO HYDRATE CALL FOUND IN HERO.JS!")
