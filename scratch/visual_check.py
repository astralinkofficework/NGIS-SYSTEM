"""Capture: admin-users kebab open (SVG menu icons) + mobile action layout."""
from playwright.sync_api import sync_playwright
BASE = 'http://localhost:3000/'

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # Desktop: open the kebab menu on admin-users
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()
    pg.goto(BASE + 'pages/admin/admin-users.html', wait_until='networkidle')
    pg.wait_for_timeout(2500)
    kebab = pg.query_selector('button[data-action="more"]')
    info = {}
    if kebab:
        kebab.click()
        pg.wait_for_timeout(500)
        info = pg.evaluate("""() => {
          const open = [...document.querySelectorAll('.dropdown-menu-list.open')];
          const vis = open.filter(m => m.offsetParent !== null);
          const items = vis.length ? [...vis[0].querySelectorAll('.dropdown-menu-item')] : [];
          return { openMenus: vis.length, items: items.map(i => (i.textContent||'').trim()),
                   svgInItems: items.filter(i => i.querySelector('svg')).length,
                   fontInItems: items.filter(i => i.querySelector('.material-symbols-outlined,.ph')).length };
        }""")
        pg.screenshot(path='scratch/svg_shots/kebab_open.png')
    print('admin-users kebab open:', info)
    ctx.close()

    # Mobile: admin-exams actions remain accessible + hamburger present
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    pg.goto(BASE + 'pages/admin/admin-exams.html', wait_until='networkidle')
    pg.wait_for_timeout(2500)
    mob = pg.evaluate("""() => {
      const hb = document.querySelector('.hamburger-btn,.mobile-hamburger-btn,.htb-hamburger,[data-action="toggle-sidebar"]');
      const groups = [...document.querySelectorAll('.action-group, td .action-icon-btn')];
      const btns = [...document.querySelectorAll('.action-icon-btn')].slice(0,6).map(x => { const r=x.getBoundingClientRect(); return {w:Math.round(r.width),h:Math.round(r.height),vis:r.width>0&&x.offsetParent!==null}; });
      return { hamburger: !!hb && hb.offsetParent!==null, actionBtns: btns.length, sample: btns };
    }""")
    print('mobile admin-exams:', mob, 'errs=', errs)
    pg.screenshot(path='scratch/svg_shots/mobile_admin_exams.png')
    ctx.close()
    b.close()
