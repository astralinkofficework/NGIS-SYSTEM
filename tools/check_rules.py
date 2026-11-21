import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'dark');
        }""")
        await page.wait_for_timeout(300)
        
        res = await page.evaluate('''() => {
            let uiSheet = null;
            for (let s of document.styleSheets) {
                if (s.href && s.href.includes('ui-cleanup.css')) {
                    uiSheet = s;
                    break;
                }
            }
            if (!uiSheet) return "ui-cleanup not found";
            const cardEl = document.querySelector('#cardAttendance');
            const matching = [];
            for (let i = 0; i < uiSheet.cssRules.length; i++) {
                const r = uiSheet.cssRules[i];
                if (r.selectorText && (r.selectorText.includes('dark') || r.selectorText.includes('hub-card'))) {
                    if (cardEl.matches(r.selectorText)) {
                        matching.push({ i, selector: r.selectorText, bg: r.style.backgroundColor || r.style.background });
                    }
                }
            }
            return {
                totalRules: uiSheet.cssRules.length,
                matching: matching
            };
        }''')
        print(res)
        await browser.close()

asyncio.run(check())
