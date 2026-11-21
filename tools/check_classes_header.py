import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/admin/admin-classes.html', wait_until='networkidle')
        
        info = await page.evaluate('''() => {
            const h2 = document.querySelector('h2');
            const header = h2.closest('header');
            
            header.style.setProperty('flex-direction', 'row', 'important');
            const resWithImportant = window.getComputedStyle(header).flexDirection;
            
            header.style.setProperty('flex-direction', 'row'); // without important
            const resWithoutImportant = window.getComputedStyle(header).flexDirection;
            
            return { resWithImportant, resWithoutImportant };
        }''')
        print(info)
        await browser.close()

asyncio.run(main())
