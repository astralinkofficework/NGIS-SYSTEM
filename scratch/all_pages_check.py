"""Full sweep: load every portal page, assert engine loaded, slots hydrated,
and zero JS page/console errors. Fast headless, no screenshots."""
import glob, json
from playwright.sync_api import sync_playwright
BASE = 'http://localhost:3000/'

pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']
urls = []
for p in pages:
    rel = p.replace('\\', '/')
    if rel == 'index.html':
        urls.append(rel)
    else:
        urls.append(rel)  # server serves repo root, so pages/... works directly

PROBE = """() => {
  const slots = [...document.querySelectorAll('[data-ngis-icon]')];
  const unhydrated = slots.filter(s => !s.querySelector('svg')).map(s => s.getAttribute('data-ngis-icon'));
  return { engine: !!(window.NGIS && window.NGIS.icon), slots: slots.length,
           unhydrated: unhydrated.slice(0,8) };
}"""

bad = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for rel in urls:
        ctx = b.new_context(viewport={'width': 1280, 'height': 800})
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.on('console', lambda m: errs.append('CONSOLE: ' + m.text[:160]) if m.type == 'error' else None)
        try:
            pg.goto(BASE + rel, wait_until='domcontentloaded', timeout=25000)
            pg.wait_for_timeout(1600)
        except Exception as e:
            errs.append('NAV: ' + str(e)[:120])
        try:
            d = pg.evaluate(PROBE)
        except Exception as e:
            d = {'engine': False, 'slots': -1, 'unhydrated': ['EVAL_FAIL: ' + str(e)[:80]]}
        flag = []
        if not d['engine']: flag.append('NO-ENGINE')
        if d['unhydrated']: flag.append('UNHYD(%d):%s' % (len(d['unhydrated']), ','.join(d['unhydrated'][:4])))
        if errs: flag.append('ERR(%d):%s' % (len(errs), errs[0][:80]))
        if flag:
            bad.append((rel, flag))
            print('FAIL %-46s %s' % (rel, ' | '.join(flag)))
        ctx.close()
    b.close()

print('\nChecked %d pages. Problem pages: %d' % (len(urls), len(bad)))
if not bad:
    print('ALL CLEAN: engine loaded, all action slots hydrated, zero console/page errors.')
json.dump([b[0] for b in bad], open('scratch/svg_shots/all_pages_bad.json', 'w'))
