import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        grid = await page.query_selector("#kpiGrid")
        grid_box = await grid.bounding_box()
        print(f"kpiGrid bounding box: y={grid_box['y']} h={grid_box['height']} w={grid_box['width']}")

        cards = await page.query_selector_all("#kpiGrid > div")
        for i, c in enumerate(cards):
            b = await c.bounding_box()
            print(f"Card {i+1}: y={b['y']}, h={b['height']}, w={b['width']}")

        await browser.close()

asyncio.run(inspect())
