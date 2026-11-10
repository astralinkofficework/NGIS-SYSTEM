import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:3000/pages/principal/principal-teachers.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={'width': 1440, 'height': 950})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until='networkidle')
    pg.wait_for_timeout(1200)
    # table fits without page-level horizontal overflow?
    metrics = pg.evaluate("""() => {
        const t = document.querySelector('table');
        const wrap = t.closest('.overflow-x-auto');
        const rows = document.querySelectorAll('#faculty-table-body tr').length;
        const h1 = document.querySelector('h1');
        return {
            tableW: t.scrollWidth, wrapW: wrap.clientWidth,
            docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
            rows,
            h1Size: getComputedStyle(h1).fontSize,
            kpiSize: getComputedStyle(document.getElementById('kpiTotalFaculty')).fontSize,
        };
    }""")
    print('desktop 1440:', metrics)
    pg.screenshot(path='scratch/pt_desktop_compact.png', full_page=False)

    pg.set_viewport_size({'width': 390, 'height': 844})
    pg.wait_for_timeout(500)
    m2 = pg.evaluate("""() => ({
        docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        hamburger: !!document.querySelector('.mobile-hamburger-btn'),
    })""")
    print('mobile 390:', m2)
    pg.screenshot(path='scratch/pt_mobile_compact.png', full_page=False)

    print('pageerrors:', errs or 'NONE')
    b.close()
