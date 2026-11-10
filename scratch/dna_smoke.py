import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:3000'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 950})
    errs, bad404 = [], []
    def on_err(e): errs.append(e)
    def on_resp(r, page=None):
        if r.status >= 400 and not r.url.endswith('favicon.ico'): bad404.append(r.url)
    pg.on('pageerror', on_err)
    pg.on('response', on_resp)

    # ── Grade Release page ──
    pg.goto(BASE + '/pages/admin/admin-grade-release.html', wait_until='networkidle')
    pg.wait_for_timeout(900)
    print('== admin-grade-release ==')
    print('sidebar visible:', pg.locator('.sidebar').first.is_visible())
    act = pg.locator('.nav-link.active').first
    print('active item:', act.inner_text().strip().replace('\n', ' ')[:40])
    print('active bg:', act.evaluate('el => getComputedStyle(el).backgroundColor'))
    print('active color:', act.evaluate('el => getComputedStyle(el).color'))
    hero = pg.locator('.hero').first
    print('hero bg:', hero.evaluate('el => getComputedStyle(el).backgroundColor'))
    n_ht = pg.locator('.hero-title').count()
    print('hero-title count:', n_ht, '| color:', pg.locator('.hero-title').first.evaluate('el => getComputedStyle(el).color') if n_ht else 'n/a')
    n_hb = pg.locator('.hero').count()
    print('hero classes:', pg.locator('.hero').first.get_attribute('class') if n_hb else 'none')
    print('body bg:', pg.evaluate('getComputedStyle(document.body).backgroundColor'))
    pg.wait_for_timeout(600)
    print('attendance KPI:', pg.locator('#kpiAttendance').inner_text())
    print('table rows:', pg.locator('#clearanceBody tr').count())
    # search filter
    pg.fill('#tableSearch', 'jenkins')
    pg.wait_for_timeout(200)
    vis = pg.locator('#clearanceBody tr:visible').count()
    print('rows after search "jenkins":', vis)
    pg.fill('#tableSearch', '')
    # select all + batch
    pg.check('#selectAllCheckbox')
    pg.wait_for_timeout(150)
    checked = pg.locator('#clearanceBody .row-checkbox:checked').count()
    print('checked after select-all:', checked)
    pg.click('#batchApproveSelectedBtn')
    pg.wait_for_timeout(300)
    print('toast:', pg.locator('#toast').inner_text())
    pg.screenshot(path='scratch/dna_grade_release.png', full_page=False)

    # ── Admin dashboard (palette swap) ──
    pg.goto(BASE + '/pages/admin/admin.html', wait_until='networkidle')
    pg.wait_for_timeout(1200)
    print('== admin.html ==')
    act2 = pg.locator('.nav-link.active').first
    print('active bg:', act2.evaluate('el => getComputedStyle(el).backgroundColor'))
    hero2 = pg.locator('.hero').first
    print('hero bg:', hero2.evaluate('el => getComputedStyle(el).backgroundColor'))
    print('body bg:', pg.evaluate('getComputedStyle(document.body).backgroundColor'))
    pg.screenshot(path='scratch/dna_admin_dash.png', full_page=False)

    print('page errors:', errs or 'NONE')
    print('404s:', bad404 or 'NONE')
    b.close()
