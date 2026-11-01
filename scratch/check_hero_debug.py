import asyncio
from playwright.async_api import async_playwright

async def check_desktop():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.on('console', lambda msg: print(f'Console [{msg.type}]: {msg.text}') if msg.type in ['error', 'warning'] else None)
        
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        
        hero_info = await page.evaluate('''() => {
            const h = document.getElementById('heroBanner');
            const overlap = document.querySelector('.dash-overlap');
            return {
                heroExists: !!h,
                heroHtml: h ? h.innerHTML.slice(0, 200) : '',
                heroH: h ? h.offsetHeight : 0,
                heroDisplay: h ? window.getComputedStyle(h).display : 'none',
                overlapMargin: overlap ? window.getComputedStyle(overlap).marginTop : 'none',
                scrollY: window.scrollY
            };
        }''')
        print('Hero Info:', hero_info)
        print('Errors:', errors)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_desktop())

