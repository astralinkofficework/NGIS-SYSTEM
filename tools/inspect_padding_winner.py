from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/admin/admin-campus.html', wait_until='networkidle')
    
    el_info = page.evaluate('''() => {
        const el = document.querySelector('.page, #mainContent, .hub-container, .subpage-container');
        if (!el) return 'none';
        
        // Find which rule is setting paddingLeft
        let winner = '';
        for (let sheet of document.styleSheets) {
            try {
                for (let rule of sheet.cssRules) {
                    if (rule.selectorText && el.matches(rule.selectorText)) {
                        if (rule.style.paddingLeft || rule.style.padding) {
                            winner += `${sheet.href ? sheet.href.split('/').pop() : 'inline'}: ${rule.selectorText} -> ${rule.style.paddingLeft || rule.style.padding}\\n`;
                        }
                    }
                }
            } catch(e) {}
        }
        return {
            tag: el.tagName,
            id: el.id,
            className: el.className,
            computedPadL: window.getComputedStyle(el).paddingLeft,
            rules: winner
        };
    }''')
    print("Admin Campus:", el_info)
    
    page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
    dept_info = page.evaluate('''() => {
        const el = document.querySelector('.page, #mainContent, .hub-container, .subpage-container');
        if (!el) return 'none';
        let winner = '';
        for (let sheet of document.styleSheets) {
            try {
                for (let rule of sheet.cssRules) {
                    if (rule.selectorText && el.matches(rule.selectorText)) {
                        if (rule.style.paddingLeft || rule.style.padding) {
                            winner += `${sheet.href ? sheet.href.split('/').pop() : 'inline'}: ${rule.selectorText} -> ${rule.style.paddingLeft || rule.style.padding}\\n`;
                        }
                    }
                }
            } catch(e) {}
        }
        return {
            tag: el.tagName,
            id: el.id,
            className: el.className,
            computedPadL: window.getComputedStyle(el).paddingLeft,
            rules: winner
        };
    }''')
    print("\nShared Department:", dept_info)
    browser.close()
