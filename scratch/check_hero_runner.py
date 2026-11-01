import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on('pageerror', lambda e: print('PageError:', e))
        page.on('console', lambda m: print('Console:', m.text))
        
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        
        res = await page.evaluate('''() => {
            const el = document.getElementById('heroBanner');
            return {
                heroBannerElement: !!el,
                scripts: Array.from(document.querySelectorAll('script')).map(s => s.src || 'inline')
            };
        }''')
        print(res)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())

