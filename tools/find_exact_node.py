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
            const nodes = Array.from(document.querySelectorAll('link[rel="stylesheet"], style'));
            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                const tag = node.tagName.toLowerCase();
                const src = node.href || node.id || ('style-' + i);
                const parent = node.parentNode;
                const next = node.nextSibling;
                
                node.remove();
                const currentBg = window.getComputedStyle(el).backgroundColor;
                parent.insertBefore(node, next);
                
                if (currentBg !== 'rgb(255, 255, 255)') {
                    return { removedSingle: `${tag}: ${src}`, newBg: currentBg };
                }
            }
            return "No single sheet did it alone";
        }''')
        print(culprit)
        await browser.close()

asyncio.run(test())
