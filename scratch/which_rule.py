from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    rule = page.evaluate("""() => {
        const el = document.querySelector('#sidebar');
        const matched = [];
        for (const sheet of document.styleSheets) {
            try {
                for (const r of sheet.cssRules) {
                    if (r.selectorText && el.matches(r.selectorText)) {
                        matched.push({
                            sheet: sheet.href ? sheet.href.split('/').pop() : 'inline',
                            selector: r.selectorText,
                            bg: r.style.getPropertyValue('background'),
                            bgc: r.style.getPropertyValue('background-color'),
                            prio: r.style.getPropertyPriority('background') || r.style.getPropertyPriority('background-color')
                        });
                    }
                }
            } catch(e) {}
        }
        return matched;
    }""")
    for r in rule:
        if r['bg'] or r['bgc']:
            print(r)
    browser.close()

