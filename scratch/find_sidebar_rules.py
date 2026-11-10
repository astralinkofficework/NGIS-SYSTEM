from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    rules = page.evaluate("""() => {
        const el = document.querySelector('#sidebar');
        const matched = [];
        for (const sheet of document.styleSheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule.selectorText && el.matches(rule.selectorText)) {
                        if (rule.style.backgroundColor || rule.style.background) {
                            matched.push({
                                href: sheet.href ? sheet.href.split('/').pop() : 'inline',
                                selector: rule.selectorText,
                                bg: rule.style.backgroundColor || rule.style.background
                            });
                        }
                    }
                }
            } catch(e) {}
        }
        return matched;
    }""")
    for r in rules:
        print(r)
    browser.close()

