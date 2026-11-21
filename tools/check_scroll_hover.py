import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='networkidle')
        await page.wait_for_timeout(800)
        
        card = page.locator('.portal-card').first
        await card.scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        
        # Test hover
        await card.hover()
        await page.wait_for_timeout(400)
        
        info = await card.evaluate("""el => {
            return {
                hover: el.matches(':hover'),
                gsap: !!window.gsap,
                motion: !!window.NGIS_MOTION,
                styleTransform: el.style.transform,
                compTransform: window.getComputedStyle(el).transform,
                compBoxShadow: window.getComputedStyle(el).boxShadow
            };
        }""")
        print("Card hover info:", info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
