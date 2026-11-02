import os

pages_without_interactions = []
pages_with_interactions = []

for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                if 'interactions.css' in content:
                    pages_with_interactions.append(path)
                else:
                    pages_without_interactions.append(path)

print(f"Pages WITH interactions.css: {len(pages_with_interactions)}")
print(f"Pages WITHOUT interactions.css: {len(pages_without_interactions)}")
for p in pages_without_interactions[:15]:
    print(" -", p)

