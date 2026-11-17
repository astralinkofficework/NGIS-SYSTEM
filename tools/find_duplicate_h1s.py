import os, re
from bs4 import BeautifulSoup

dup_pages = []

for root, dirs, files in os.walk('pages'):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            soup = BeautifulSoup(content, 'html.parser')
            h1s = soup.find_all('h1')
            if len(h1s) > 1:
                titles = [h.get_text(strip=True) for h in h1s if h.get_text(strip=True)]
                # Check if duplicates exist
                if len(titles) != len(set(titles)):
                    dup_pages.append((path, titles))

print(f"Total pages with duplicate h1 text: {len(dup_pages)}")
for path, titles in dup_pages[:20]:
    print(f"{path}: {titles}")
