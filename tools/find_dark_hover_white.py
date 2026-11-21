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
        
        res = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const rules = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && el.matches(r.selectorText)) {
                            const bg = r.style.backgroundColor || r.style.background;
                            const prio = r.style.getPropertyPriority('background') || r.style.getPropertyPriority('background-color');
                            if (bg && bg.includes('255, 255, 255')) {
                                rules.push({
                                    sheet: s.href ? s.href.split('/').pop() : 'inline',
                                    selector: r.selectorText,
                                    bg: bg,
                                    prio: prio
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return rules;
        }''')
        for r in res:
            print(f"[{r['sheet']}] {r['selector'][:80]}... --> {r['bg']} !{r['prio']}")
        await browser.close()

asyncio.run(test())
