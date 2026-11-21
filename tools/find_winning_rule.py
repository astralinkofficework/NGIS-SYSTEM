import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        res = await page.evaluate('''() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            const el = document.querySelector('#cardAttendance');
            const importantRules = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && el.matches(r.selectorText)) {
                            const bgPrio = r.style.getPropertyPriority('background');
                            const bgColPrio = r.style.getPropertyPriority('background-color');
                            if (bgPrio === 'important' || bgColPrio === 'important') {
                                importantRules.push({
                                    sheet: s.href ? s.href.split('/').pop() : 'inline',
                                    selector: r.selectorText,
                                    bg: r.style.getPropertyValue('background'),
                                    bgColor: r.style.getPropertyValue('background-color')
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return importantRules;
        }''')
        print(f"Total matching !important rules: {len(res)}")
        for r in res:
            print(f"[{r['sheet']}] {r['selector'][:80]}...")
            print(f"   bg: {r['bg']} | bgColor: {r['bgColor']}")
        await browser.close()

asyncio.run(test())
