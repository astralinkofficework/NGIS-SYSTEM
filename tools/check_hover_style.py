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
        await page.wait_for_timeout(300)
        
        info = await card.evaluate("""el => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                boxShadow: cs.boxShadow,
                transition: cs.transition,
                classes: el.className
            };
        }""")
        print("Card hover info:", info)
        
        # Check media query support in headless Chromium
        media = await page.evaluate("() => window.matchMedia('(hover: hover) and (pointer: fine)').matches")
        print("Media query '(hover: hover) and (pointer: fine)' matches in browser:", media)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
