from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    css_source = page.evaluate("""() => {
        const sb = document.querySelector('#sidebar');
        // Let's create an element and check if .sidebar is defined in any other rule
        const res = [];
        for (const sheet of document.styleSheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule.cssText && rule.cssText.includes('.sidebar') && rule.cssText.includes('background')) {
                        res.push({
                            sheet: sheet.href,
                            css: rule.cssText
                        });
                    }
                }
            } catch(e) {}
        }
        return res;
    }""")
    for r in css_source:
        print("SHEET:", r['sheet'])
        print("CSS:", r['css'])
    browser.close()

