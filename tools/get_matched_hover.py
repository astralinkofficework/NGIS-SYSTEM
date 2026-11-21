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
        
        card = page.locator('#cardAttendance')
        await card.hover()
        await page.wait_for_timeout(200)
        
        # Check matching rules in JS
        matched = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const list = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && (r.selectorText.includes('hub-card') || r.selectorText.includes('card'))) {
                            const bg = r.style.backgroundColor || r.style.background;
                            const prio = r.style.getPropertyPriority('background') || r.style.getPropertyPriority('background-color');
                            // Check if selector ends with :hover or matches element
                            if (bg && (r.selectorText.includes(':hover') || el.matches(r.selectorText))) {
                                list.push({
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
            return {
                computedBg: window.getComputedStyle(el).backgroundColor,
                list: list
            };
        }''')
        print("Computed BG during hover:", matched['computedBg'])
        print(f"Total matching candidates: {len(matched['list'])}")
        for item in matched['list']:
            print(f"[{item['sheet']}] {item['selector'][:80]}... --> {item['bg']} !{item['prio']}")
        await browser.close()

asyncio.run(test())
