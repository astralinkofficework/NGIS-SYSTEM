import re
from playwright.sync_api import sync_playwright
s = open('pages/shared/announcements.html', encoding='utf-8').read()
print('share slot occurrences in source:', len(re.findall(r'data-ngis-icon="share"', s)))
for m in list(re.finditer(r'.{40}data-ngis-icon="share".{20}', s))[:3]:
    print('  ', re.sub(r'\s+', ' ', m.group(0)))
# context: are they inside a <template> or hidden or inside script string?
print('has <template>:', '<template' in s)
print('share in JS template strings (backtick/quote):', bool(re.search(r'[\'"`].{0,40}data-ngis-icon="share"', s)))

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_context(viewport={'width':1280,'height':800}).new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text[:160]) if m.type == 'error' else None)
    pg.goto('http://localhost:3000/pages/shared/announcements.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(4000)
    d = pg.evaluate("""() => {
      const slots = [...document.querySelectorAll('[data-ngis-icon="share"]')];
      return {
        total: slots.length,
        withSvg: slots.filter(x => x.querySelector('svg')).length,
        sample: slots.slice(0,3).map(x => ({
          parent: x.parentElement ? x.parentElement.className.slice(0,40) : '',
          tag: x.tagName, display: getComputedStyle(x).display,
          ngisLoaded: !!(window.NGIS && window.NGIS.icon),
          iconFn: window.NGIS ? (window.NGIS.icon('share')||'').slice(0,40) : 'NO-NGIS'
        }))
      };
    }""")
    print('\nLIVE:', d)
    for e in errs[:5]:
        print('  ERR:', e)
    b.close()
