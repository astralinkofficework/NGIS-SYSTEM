import os, re

gtc_re = re.compile(r'grid-template-columns\s*:\s*([^;!]+)!important', re.IGNORECASE)

for root, dirs, files in os.walk('assets/css'):
    for f in files:
        if f.endswith('.css'):
            path = os.path.join(root, f)
            with open(path, encoding='utf-8', errors='ignore') as fp:
                for i, line in enumerate(fp, 1):
                    m = gtc_re.search(line)
                    if m:
                        print(f"{path}:{i}: {line.strip()[:100]}")
