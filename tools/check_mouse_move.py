import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        card = page.locator('.portal-card').first
        box = await card.bounding_box()
        print("Card bounding box:", box)
        
        await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        await page.wait_for_timeout(300)
        
        is_hovered = await card.evaluate("el => el.matches(':hover')")
        print("Matches :hover:", is_hovered)
        
        info = await card.evaluate("""el => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                boxShadow: cs.boxShadow,
                transition: cs.transition
            };
        }""")
        print("Card hover info:", info)
        
        # Test NGIS_MOTION.cardLiftEnter directly
        await card.evaluate("el => window.NGIS_MOTION.cardLiftEnter(el)")
        await page.wait_for_timeout(300)
        lift_info = await card.evaluate("""el => {
            const cs = window.getComputedStyle(el);
            return {
                transform: cs.transform,
                boxShadow: cs.boxShadow
            };
        }""")
        print("Direct NGIS_MOTION.cardLiftEnter info:", lift_info)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
