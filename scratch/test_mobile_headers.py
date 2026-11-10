from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for path in ['pages/admin/admin-users.html', 'pages/admin/admin-assignments.html', 'pages/student/student-assignments.html']:
        page = browser.new_page(viewport={'width': 375, 'height': 812})
        page.goto(f'http://127.0.0.1:3000/{path}')
        page.wait_for_timeout(1000)
        
        info = page.evaluate("""() => {
            const h = document.querySelector('header');
            const htb = document.querySelector('.hero-topbar');
            const hb = document.querySelector('[data-action="toggle-sidebar"]');
            const main = document.querySelector('.main');
            return {
                hasHeaderTag: !!h,
                hasHeroTopbar: !!htb,
                heroTopbarVisible: htb ? (htb.offsetWidth > 0 && htb.offsetHeight > 0) : false,
                hasToggle: !!hb,
                toggleVisible: hb ? (hb.offsetWidth > 0 && hb.offsetHeight > 0) : false,
                firstElementsInMain: main ? Array.from(main.children).slice(0, 3).map(c => c.tagName + '.' + c.className) : []
            };
        }""")
        print(f"=== {path} ===")
        print(info)
        page.close()
    browser.close()

