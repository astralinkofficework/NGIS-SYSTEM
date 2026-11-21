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
            for (let sIdx = 0; sIdx < document.styleSheets.length; sIdx++) {
                const sheet = document.styleSheets[sIdx];
                const sName = sheet.href ? sheet.href.split('/').pop() : 'inline-' + sIdx;
                sheet.disabled = true;
                const newBg = window.getComputedStyle(el).backgroundColor;
                sheet.disabled = false;
                if (newBg !== 'rgb(255, 255, 255)') {
                    return { foundInSheet: sName, newBg: newBg };
                }
            }
            return "Not in any disabled stylesheet";
        }''')
        print("Culprit sheet:", culprit)
        await browser.close()

asyncio.run(test())
