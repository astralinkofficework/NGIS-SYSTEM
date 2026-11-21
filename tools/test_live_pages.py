import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        # Test 1: admin-departments.html
        await page.goto('http://127.0.0.1:3000/pages/admin/admin-departments.html', wait_until='networkidle')
        info_dept = await page.evaluate('''() => {
            const sec = document.querySelector('section');
            const h1 = sec.querySelector('h1');
            return {
                dir: window.getComputedStyle(sec).flexDirection,
                align: window.getComputedStyle(sec).alignItems,
                h1X: h1.getBoundingClientRect().x
            };
        }''')
        print('admin-departments live test:', info_dept)
        await page.screenshot(path=r'C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536\live_admin_dept.png')
        
        # Test 2: admin-classes.html
        await page.goto('http://127.0.0.1:3000/pages/admin/admin-classes.html', wait_until='networkidle')
        info_classes = await page.evaluate('''() => {
            const sec = document.querySelector('section');
            const h1 = sec ? sec.querySelector('h1') : null;
            return {
                dir: sec ? window.getComputedStyle(sec).flexDirection : null,
                h1X: h1 ? h1.getBoundingClientRect().x : null
            };
        }''')
        print('admin-classes live test:', info_classes)
        await page.screenshot(path=r'C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536\live_admin_classes.png')
        
        # Test 3: admin-campuses.html
        await page.goto('http://127.0.0.1:3000/pages/admin/admin-campuses.html', wait_until='networkidle')
        info_campuses = await page.evaluate('''() => {
            const sec = document.querySelector('section');
            const h1 = sec ? sec.querySelector('h1') : null;
            return {
                dir: sec ? window.getComputedStyle(sec).flexDirection : null,
                h1X: h1 ? h1.getBoundingClientRect().x : null
            };
        }''')
        print('admin-campuses live test:', info_campuses)
        await page.screenshot(path=r'C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536\live_admin_campuses.png')

        await browser.close()

asyncio.run(main())
