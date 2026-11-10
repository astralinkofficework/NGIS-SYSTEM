"""Functional verification: click row actions & kebab, confirm behavior preserved
and that the icons are inline SVG (not font glyphs)."""
from playwright.sync_api import sync_playwright
BASE = 'http://localhost:3000/'

def probe_more_menu(page):
    # does clicking a kebab reveal a menu (any newly visible menu/popover)?
    before = page.evaluate("() => document.querySelectorAll('.menu.show,[role=menu]:not([hidden]),.dropdown-menu.show,.action-dropdown-menu.show').length")
    btns = page.query_selector_all('button.btn-more, button[data-action="more"], button[aria-label="More options"]')
    opened = 0
    for b in btns[:3]:
        try:
            b.click(timeout=1500)
            page.wait_for_timeout(400)
            vis = page.evaluate("() => [...document.querySelectorAll('.menu,[role=menu],.dropdown-menu,.action-dropdown-menu,.popover,.dropdown')].filter(e=>e.offsetParent!==null && e.getBoundingClientRect().height>10 && !e.classList.contains('hidden')).length")
            if vis > 0:
                opened += 1
            page.keyboard.press('Escape')
            page.wait_for_timeout(150)
        except Exception as e:
            pass
    return len(btns), opened

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for path in ['pages/admin/admin-users.html', 'pages/admin/admin-exams.html',
                 'pages/student/student-services.html', 'pages/teacher/teacher-roster.html']:
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        pg.goto(BASE + path, wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(2500)
        # count action buttons that contain an SVG vs a font glyph
        stats = pg.evaluate("""() => {
          const btns = [...document.querySelectorAll('button, a[href]')].filter(x => x.querySelector('[data-ngis-icon], .ngis-icon-inline, .material-symbols-outlined, .ph'));
          let svg=0, font=0, noLabel=0;
          for (const x of btns) {
            const slot = x.querySelector('[data-ngis-icon], .ngis-icon-inline');
            if (slot && slot.querySelector('svg')) svg++;
            const glyph = x.querySelector('.material-symbols-outlined, .ph');
            if (glyph && (glyph.textContent||'').trim() && !x.querySelector('svg')) font++;
            if (slot && !x.getAttribute('title') && !x.getAttribute('aria-label')) noLabel++;
          }
          return {svg, font, noLabel};
        }""")
        nmore, opened = probe_more_menu(pg)
        print('%-40s svgBtns=%-3d fontBtns=%-3d unlabeled=%-3d kebab=%-3d openedMenu=%-2d errs=%d'
              % (path, stats['svg'], stats['font'], stats['noLabel'], nmore, opened, len(errs)))
        for e in errs[:2]:
            print('    ERR', e)
        ctx.close()
    b.close()
