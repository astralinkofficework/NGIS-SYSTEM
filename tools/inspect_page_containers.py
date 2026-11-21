import glob, re
from collections import Counter

tag_classes = Counter()
container_selectors = Counter()

pages = glob.glob('pages/**/*.html', recursive=True)

for p in pages:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # find main tag or primary container
            mains = re.findall(r'<main[^>]*class=[\"\']([^\"\']*)[\"\']', content)
            for m in mains:
                tag_classes['main: ' + m] += 1
            
            divs = re.findall(r'<div[^>]*class=[\"\']([^\"\']*(?:page|content|container|workspace|shell)[^\"\']*)[\"\']', content)
            for d in divs:
                # get primary token
                for token in d.split():
                    if any(k in token for k in ['page', 'content', 'container', 'workspace', 'shell']):
                        container_selectors[token] += 1
    except Exception as e:
        pass

print("=== MAIN TAG CLASSES ===")
for k, v in tag_classes.most_common(10):
    print(f"{k}: {v}")

print("\n=== CONTAINER CLASSES ===")
for k, v in container_selectors.most_common(15):
    print(f"{k}: {v}")
