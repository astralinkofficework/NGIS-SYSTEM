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
        
        culprit = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            let dsSheet = null;
            for (let s of document.styleSheets) {
                if (s.href && s.href.includes('design-system.css')) {
                    dsSheet = s;
                    break;
                }
            }
            if (!dsSheet) return "dsSheet not found";
            
            for (let i = 0; i < dsSheet.cssRules.length; i++) {
                const r = dsSheet.cssRules[i];
                const oldCss = r.cssText;
                try {
                    dsSheet.deleteRule(i);
                    const currentBg = window.getComputedStyle(el).backgroundColor;
                    dsSheet.insertRule(oldCss, i);
                    if (currentBg !== 'rgb(255, 255, 255)') {
                        return { ruleIndex: i, selector: r.selectorText, cssText: oldCss.substring(0, 150), newBg: currentBg };
                    }
                } catch(e) {
                    dsSheet.insertRule(oldCss, i);
                }
            }
            return "No single rule in dsSheet changed it";
        }''')
        print(culprit)
        await browser.close()

asyncio.run(test())
