import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:3000/pages/principal/principal-reports.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until='networkidle')
    pg.wait_for_timeout(1300)

    m = pg.evaluate("""() => {
        const t = document.querySelector('table');
        const wrap = t.closest('.tbl-scroll');
        const rows = document.querySelectorAll('#clearanceBody tr');
        const pend = document.querySelector('#clearanceBody tr[data-status="pending"]');
        return {
            tableW: t.scrollWidth, wrapW: wrap.clientWidth,
            docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
            rowCount: rows.length,
            h1: document.querySelector('.gr-h1')?.textContent.trim(),
            gpa: document.getElementById('repAvgGpa').textContent,
            att: document.getElementById('repAttRate').textContent,
            pass: document.getElementById('repHonorRoll').textContent,
            pendStatus: pend?.dataset.status,
        };
    }""")
    print('desktop 1440:', m)

    # search filter
    pg.fill('#tableSearch', 'jenkins')
    pg.wait_for_timeout(200)
    vis = pg.evaluate("() => [...document.querySelectorAll('#clearanceBody tr')].filter(r=>r.style.display!=='none').length")
    print('search "jenkins" -> visible rows:', vis)
    pg.fill('#tableSearch', '')

    # status filter
    pg.select_option('#statusFilter', 'ready')
    pg.wait_for_timeout(200)
    vis2 = pg.evaluate("() => [...document.querySelectorAll('#clearanceBody tr')].filter(r=>r.style.display!=='none').length")
    print("status 'ready' -> visible rows:", vis2)
    pg.select_option('#statusFilter', '')

    # select all
    pg.click('#selectAllCheckbox')
    pg.wait_for_timeout(150)
    checked = pg.evaluate("() => document.querySelectorAll('.row-checkbox:checked').length")
    print('select-all -> checked:', checked)

    # bold check
    bold = pg.evaluate("""() => {
        let n = 0;
        document.querySelectorAll('body *').forEach(el => {
            const w = getComputedStyle(el).fontWeight;
            if (w === '700' || w === '800' || w === '600' || parseInt(w) >= 600) n++;
        });
        return n;
    }""")
    print('elements with weight >=600 (should be 0):', bold)

    pg.screenshot(path='scratch/pr_reports_desktop.png')

    pg.set_viewport_size({'width': 390, 'height': 844})
    pg.wait_for_timeout(400)
    m2 = pg.evaluate("""() => ({
        docOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        hamburger: !!document.querySelector('.mobile-hamburger-btn'),
    })""")
    print('mobile 390:', m2)
    pg.screenshot(path='scratch/pr_reports_mobile.png')

    print('pageerrors:', errs or 'NONE')
    b.close()
