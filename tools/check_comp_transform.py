import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        card = page.locator('.portal-card').first
        await card.hover()
        await page.wait_for_timeout(200)
        
        computed = await card.evaluate("""el => {
            return {
                transform: window.getComputedStyle(el).transform,
                webkitTransform: window.getComputedStyle(el).webkitTransform,
                translate: window.getComputedStyle(el).translate,
                scale: window.getComputedStyle(el).scale
            };
        }""")
        print("Computed:", computed)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
