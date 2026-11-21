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
        await page.locator('#cardAttendance').hover()
        await page.wait_for_timeout(200)
        
        info = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const hubVar = window.getComputedStyle(el).getPropertyValue('--hub-card-bg');
            const htmlTheme = document.documentElement.getAttribute('data-theme');
            const matches = [];
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.selectorText && el.matches(r.selectorText)) {
                            const bg = r.style.backgroundColor || r.style.background;
                            const prio = r.style.getPropertyPriority('background') || r.style.getPropertyPriority('background-color');
                            if (prio === 'important') {
                                matches.push({
                                    sheet: s.href ? s.href.split('/').pop() : 'inline',
                                    selector: r.selectorText,
                                    bg: bg
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return {
                htmlTheme: htmlTheme,
                hubVar: hubVar,
                computedBg: window.getComputedStyle(el).backgroundColor,
                matches: matches
            };
        }''')
        print("Theme:", info['htmlTheme'], "HubVar:", repr(info['hubVar']), "Computed:", info['computedBg'])
        for m in info['matches']:
            print(f"[{m['sheet']}] {m['selector'][:70]}... --> {m['bg']}")
        await browser.close()

asyncio.run(test())
