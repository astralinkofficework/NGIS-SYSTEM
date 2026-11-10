import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='networkidle')
        
        # Check if any link has href containing principal-assignments
        links = await page.eval_on_selector_all('a', 'els => els.map(e => e.getAttribute("href"))')
        pa_links = [l for l in links if l and 'principal-assignments' in l]
        print('Links to principal-assignments found on principal.html:', pa_links)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())

