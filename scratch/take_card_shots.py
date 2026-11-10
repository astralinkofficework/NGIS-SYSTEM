import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-departments.html")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/dept_cards_before.png")

        await page.goto("http://127.0.0.1:3000/pages/principal/principal-classes.html")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/classes_cards_before.png")

        await page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/principal_cards_before.png")

        await browser.close()

asyncio.run(main())

