import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)

        mob_btn = await page.query_selector('.principal-mobile-view [data-action="toggle-sidebar"]')
        is_vis = await mob_btn.is_visible() if mob_btn else False
        box = await mob_btn.bounding_box() if mob_btn else None
        print("Mobile view hamburger is visible:", is_vis)
        print("Bounding box:", box)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test())

