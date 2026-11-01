import os, re
from bs4 import BeautifulSoup

files = [f for f in os.listdir('pages/shared') if f.endswith('.html')]
print(f"Auditing links across {len(files)} shared pages...")

all_links = []

for f in sorted(files):
    p = os.path.join('pages/shared', f)
    with open(p, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # 1. Check all <a> tags
        for a in soup.find_all('a'):
            href = a.get('href')
            if href:
                all_links.append((f, 'a', href, a.text.strip()[:30]))
                
        # 2. Check all onclick handlers
        for el in soup.find_all(attrs={'onclick': True}):
            oc = el['onclick']
            m = re.search(r'location\.href\s*=\s*[\'"`]([^\'"`]+)[\'"`]', oc)
            if m:
                all_links.append((f, 'onclick', m.group(1), el.text.strip()[:30]))
                
        # 3. Check inline script redirects
        redirs = re.findall(r'(?:window\.)?location\.(?:href|replace)\s*=\s*[\'"`]([^\'"`]+)[\'"`]', content)
        for r in redirs:
            all_links.append((f, 'script_redirect', r, 'redirect'))

print(f"Total outgoing links in shared pages: {len(all_links)}")
for l in all_links:
    if any(k in l[2].lower() for k in ['teacher', 'admin', 'principal', 'staff', 'student']):
        print(f"  In {l[0]} ({l[1]}): {l[2]} [{l[3]}]")

