import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html')
        await page.wait_for_timeout(500)
        
        rules = await page.evaluate('''() => {
            const el = document.querySelector('.hub-card-body');
            const matched = [];
            for (let sheet of document.styleSheets) {
                try {
                    for (let rule of sheet.cssRules) {
                        if (rule.selectorText && el.matches(rule.selectorText)) {
                            if (rule.style.backgroundColor || rule.style.background) {
                                matched.push({
                                    selector: rule.selectorText,
                                    bg: rule.style.backgroundColor || rule.style.background,
                                    href: sheet.href ? sheet.href.split('/').pop() : 'inline'
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return matched;
        }''')
        print('Matched rules for .hub-card-body:')
        for r in rules:
            print(r)
            
        # Also check .hub-card-title
        rules_title = await page.evaluate('''() => {
            const el = document.querySelector('.hub-card-title');
            const matched = [];
            for (let sheet of document.styleSheets) {
                try {
                    for (let rule of sheet.cssRules) {
                        if (rule.selectorText && el.matches(rule.selectorText)) {
                            if (rule.style.backgroundColor || rule.style.background) {
                                matched.push({
                                    selector: rule.selectorText,
                                    bg: rule.style.backgroundColor || rule.style.background,
                                    href: sheet.href ? sheet.href.split('/').pop() : 'inline'
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return matched;
        }''')
        print('Matched rules for .hub-card-title:')
        for r in rules_title:
            print(r)

        await browser.close()

asyncio.run(main())
