import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        
        rules = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const list = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && r.selectorText.includes(':hover')) {
                            // Check if splitting by comma contains hub-card or [class*="card"]
                            const selectors = r.selectorText.split(',');
                            for (let sel of selectors) {
                                sel = sel.trim();
                                if (sel.includes('.hub-card:hover') || sel.includes('[class*="card"]:hover') || sel.includes('.card:hover') || sel.includes('a[href]:hover') || sel.includes('a.hub-card:hover')) {
                                    const bg = r.style.backgroundColor || r.style.background;
                                    const prio = r.style.getPropertyPriority('background') || r.style.getPropertyPriority('background-color');
                                    list.push({
                                        sheet: s.href ? s.href.split('/').pop() : 'inline',
                                        selector: sel,
                                        bg: bg,
                                        prio: prio
                                    });
                                }
                            }
                        }
                    }
                } catch(e) {}
            }
            return list;
        }''')
        print(f"Total matching selectors: {len(rules)}")
        for r in rules:
            if r['bg']:
                print(f"[{r['sheet']}] {r['selector']} --> {r['bg']} !{r['prio']}")
        await browser.close()

asyncio.run(test())
