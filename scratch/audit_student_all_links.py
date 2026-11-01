import os, re
from bs4 import BeautifulSoup

files = [f for f in os.listdir('pages/student') if f.endswith('.html')]
print(f"Auditing links across {len(files)} student pages...")

all_links = []

for f in sorted(files):
    p = os.path.join('pages/student', f)
    with open(p, 'r', encoding='utf-8', errors='ignore') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        
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

print(f"Total outgoing links found in student pages: {len(all_links)}")

# Check for any teacher or admin links in student pages
foreign_links = [l for l in all_links if 'teacher' in l[2].lower() or 'admin' in l[2].lower() or 'principal' in l[2].lower() or 'staff' in l[2].lower()]
print(f"Foreign portal links in student pages: {len(foreign_links)}")
for fl in foreign_links:
    print(f"  In {fl[0]} ({fl[1]}): {fl[2]} [{fl[3]}]")

