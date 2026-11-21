import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)
        await page.evaluate('''() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.documentElement.classList.add('dark');
        }''')
        await page.wait_for_timeout(300)
        
        matches = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            let dsSheet = null;
            for (let s of document.styleSheets) {
                if (s.href && s.href.includes('design-system.css')) {
                    dsSheet = s;
                    break;
                }
            }
            if (!dsSheet) return [];
            const list = [];
            for (let i = 0; i < dsSheet.cssRules.length; i++) {
                const r = dsSheet.cssRules[i];
                if (r.selectorText) {
                    try {
                        if (el.matches(r.selectorText)) {
                            list.push({ i, selector: r.selectorText, bg: r.style.backgroundColor || r.style.background });
                        }
                    } catch(e) {}
                }
            }
            return list;
        }''')
        print(f"Total matching rules in design-system.css: {len(matches)}")
        for m in matches:
            print(f"Rule {m['i']}: {m['selector'][:80]} --> {m['bg']}")
        await browser.close()

asyncio.run(test())
