import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:3000/pages/principal/principal-approvals.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until='networkidle')
    pg.wait_for_timeout(1400)

    def metrics():
        return pg.evaluate("""() => {
            const t = document.querySelector('table');
            const wrap = t.closest('.table-responsive');
            return {
                tableW: t.scrollWidth, wrapW: wrap.clientWidth,
                docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
                rows: document.querySelectorAll('#approvalsTableBody tr').length,
                h1: getComputedStyle(document.querySelector('.page h1')).fontSize,
                kpi: getComputedStyle(document.getElementById('statTotal')).fontSize,
            };
        }""")

    print('desktop 1440:', metrics())
    pg.screenshot(path='scratch/appr_desktop.png', full_page=True)

    # tab filter
    pg.click('[data-tab="pending"]')
    pg.wait_for_timeout(300)
    print('pending rows:', pg.evaluate("() => [...document.querySelectorAll('#approvalsTableBody tr')].filter(r=>r.querySelector('.row-checkbox')).length"))
    pg.click('[data-tab="all"]')

    # authorize first pending -> count changes
    before = pg.evaluate("() => document.getElementById('statPending').textContent")
    pg.evaluate("() => { const b=[...document.querySelectorAll('#approvalsTableBody button')].find(x=>x.textContent.includes('Authorize')); if(b) b.click(); }")
    pg.wait_for_timeout(400)
    after = pg.evaluate("() => document.getElementById('statPending').textContent")
    print('pending before/after authorize:', before, '->', after)

    # select all -> batch bar
    pg.click('#selectAllCheckbox')
    pg.wait_for_timeout(200)
    print('batch bar visible:', pg.evaluate("() => !document.getElementById('batchBar').classList.contains('hidden')"))

    pg.set_viewport_size({'width': 768, 'height': 900})
    pg.wait_for_timeout(400)
    print('tablet 768:', metrics())
    pg.screenshot(path='scratch/appr_tablet.png', full_page=True)

    pg.set_viewport_size({'width': 390, 'height': 844})
    pg.wait_for_timeout(400)
    m = pg.evaluate("""() => ({
        docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        hamburger: !!document.querySelector('.mobile-hamburger-btn'),
        heroHidden: (() => { const h = document.getElementById('heroBanner'); return h ? getComputedStyle(h).display : 'removed'; })(),
    })""")
    print('mobile 390:', m)
    pg.screenshot(path='scratch/appr_mobile.png', full_page=True)

    print('pageerrors:', errs or 'NONE')
    b.close()
