import os

count = 0
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                txt = fp.read()
            if '<div id="heroBanner"></div>' in txt:
                new_txt = txt.replace('<div id="heroBanner"></div>', '<header id="heroBanner" role="banner"></header>')
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(new_txt)
                count += 1
                print(f"Updated: {p.replace('\\', '/')}")

print(f"Total updated: {count}")

