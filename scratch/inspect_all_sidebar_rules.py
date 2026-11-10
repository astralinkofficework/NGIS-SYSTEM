from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
    page.wait_for_timeout(500)
    
    rules = page.evaluate("""() => {
        const el = document.querySelector('#sidebar');
        const list = [];
        for (let i = 0; i < document.styleSheets.length; i++) {
            const sheet = document.styleSheets[i];
            try {
                for (let j = 0; j < sheet.cssRules.length; j++) {
                    const r = sheet.cssRules[j];
                    if (r.selectorText && el.matches(r.selectorText)) {
                        const bg = r.style.getPropertyValue('background');
                        const bgc = r.style.getPropertyValue('background-color');
                        if (bg || bgc) {
                            list.push({
                                sheet: sheet.href ? sheet.href.split('?')[0].split('/').pop() : 'inline',
                                selector: r.selectorText,
                                bg: bg,
                                bgc: bgc,
                                prio_bg: r.style.getPropertyPriority('background'),
                                prio_bgc: r.style.getPropertyPriority('background-color')
                            });
                        }
                    }
                }
            } catch(e) {}
        }
        return list;
    }""")
    for r in rules:
        print(r)
    browser.close()

