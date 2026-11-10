import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
t = open('pages/admin/admin.html', encoding='utf-8').read()
# top-level structure: find <main ...> and its direct children sections/divs with ids/classes
body = t[t.find('<body'):]
# list major blocks: ids on div/section/main with role-ish names
for m in re.finditer(r'<(main|section|div|aside|header)\b[^>]*(?:id="([^"]+)"|class="([^"]{0,80})")[^>]*>', body):
    tag, i_, c = m.group(1), m.group(2), m.group(3)
    line = body[:m.start()].count('\n') + t[:t.find('<body')].count('\n') + 1
    key = i_ or (c.split()[0] if c else '')
    if tag in ('main','section') or key in ('page','dashboard','overview','stats','kpiRow','chartsRow'):
        print(f'{line:>5} <{tag} id="{i_}" class="{(c or "")[:60]}>')
print('---')
# find headings h3/h4 + card grid classes
h = re.findall(r'<h[34][^>]*>([^<]{3,70})</h', body)
print('h3/h4:', h[:30])
# where does data come from? fetch/api calls
apis = set(re.findall(r"NGISAuth\.api\(\s*['\"]([^'\"]+)", body)) | set(re.findall(r"fetch\(\s*['\"]([^'\"]+)", body))
print('API endpoints used:', list(apis)[:20])
# hero config
hc = re.search(r'window\.HERO_CONFIG\s*=\s*\{.{0,400}', body, re.S)
print('HERO_CONFIG:', ' '.join(hc.group(0).split())[:300] if hc else 'none')
pg = re.search(r'window\.PAGE\s*=\s*\{[^}]*\}', body)
print('PAGE:', ' '.join(pg.group(0).split()) if pg else 'none')
