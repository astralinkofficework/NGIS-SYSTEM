from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 375, 'height': 812})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-subjects.html', wait_until='networkidle')
    res = page.evaluate('''() => {
        const hbs = document.querySelectorAll('[data-action="toggle-sidebar"]');
        const list = [];
        for (const h of hbs) {
            const r = h.getBoundingClientRect();
            const cs = window.getComputedStyle(h);
            list.push({
                tag: h.tagName,
                classes: h.className,
                rect: { x: r.x, y: r.y, w: r.width, h: r.height },
                display: cs.display,
                visibility: cs.visibility
            });
        }
        return list;
    }''')
    print('Principal subjects hamburger check:', res)
    browser.close()
