import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        card = page.locator('#cardAttendance')
        await card.hover()
        await page.wait_for_timeout(200)
        
        # Check all matching rules that have hover
        res = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const list = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && r.selectorText.includes(':hover')) {
                            if (el.matches(r.selectorText)) {
                                list.push({
                                    sheet: s.href ? s.href.split('/').pop() : 'inline',
                                    selector: r.selectorText,
                                    bg: r.style.backgroundColor || r.style.background,
                                    prio: r.style.getPropertyPriority('background') || r.style.getPropertyPriority('background-color')
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return list;
        }''')
        print(f"Total matching :hover rules: {len(res)}")
        for r in res:
            if r['bg']:
                print(f"[{r['sheet']}] {r['selector'][:80]}... --> {r['bg']} !{r['prio']}")
        await browser.close()

asyncio.run(test())
