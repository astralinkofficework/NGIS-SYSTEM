import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        card = page.locator('#cardAttendance')
        await card.hover()
        await page.wait_for_timeout(300)
        
        rules = await page.evaluate('''() => {
            const cardEl = document.querySelector('#cardAttendance');
            const matching = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && cardEl.matches(r.selectorText)) {
                            const tr = r.style.transform;
                            const prio = r.style.getPropertyPriority('transform');
                            if (tr) {
                                matching.push({
                                    sheet: s.href ? s.href.split('/').pop() : 'inline',
                                    selector: r.selectorText,
                                    transform: tr,
                                    prio: prio
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return {
                computedTransform: window.getComputedStyle(cardEl).transform,
                matching: matching
            };
        }''')
        print("Computed Transform:", rules['computedTransform'])
        print("Matching transform rules:")
        for r in rules['matching']:
            print(f"[{r['sheet']}] {r['selector'][:80]}... --> {r['transform']} !{r['prio']}")
        await browser.close()

asyncio.run(test())
