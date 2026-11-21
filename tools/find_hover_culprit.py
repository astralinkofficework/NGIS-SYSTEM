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
        
        res = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const nodes = Array.from(document.querySelectorAll('link[rel="stylesheet"], style'));
            const results = [];
            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i];
                const tag = node.tagName.toLowerCase();
                const src = node.href ? node.href.split('/').pop() : (node.id || 'style-' + i);
                const parent = node.parentNode;
                const next = node.nextSibling;
                
                node.remove();
                const bg = window.getComputedStyle(el).backgroundColor;
                parent.insertBefore(node, next);
                
                if (bg !== 'rgb(255, 255, 255)') {
                    results.push({ node: `${tag}: ${src}`, bgWhileRemoved: bg });
                }
            }
            return results;
        }''')
        print("Sheets that caused rgb(255, 255, 255) when hovered in dark mode:", res)
        await browser.close()

asyncio.run(test())
