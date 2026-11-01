import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        
        rect = await page.evaluate('''() => {
            const hero = document.querySelector('.hero');
            const main = document.querySelector('.main');
            const body = document.body;
            return {
                scrollY: window.scrollY,
                heroRect: hero ? hero.getBoundingClientRect() : null,
                mainRect: main ? main.getBoundingClientRect() : null
            };
        }''')
        print(rect)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())

