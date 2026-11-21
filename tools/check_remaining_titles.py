import os
import re

attr_re = re.compile(r'\btitle\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)

for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            no_code = re.sub(r'<script\b[^>]*>.*?</script>', '', c, flags=re.I|re.S)
            no_code = re.sub(r'<style\b[^>]*>.*?</style>', '', no_code, flags=re.I|re.S)
            no_code = re.sub(r'<title[^>]*>.*?</title>', '', no_code, flags=re.I|re.S)
            matches = list(attr_re.finditer(no_code))
            if matches:
                print(f"{p}: {len(matches)} matches outside script:")
                for m in matches[:3]:
                    print("   ", m.group(0))
