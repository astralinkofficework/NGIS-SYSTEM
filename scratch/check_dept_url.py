import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 390, 'height': 844})
        response = await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        print('Final URL:', page.url)
        print('Title:', await page.title())
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())

