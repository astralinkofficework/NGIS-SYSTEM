import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        info = await page.evaluate("""() => {
            const grid = document.getElementById('kpiGrid');
            const cs = window.getComputedStyle(grid);
            const firstCard = grid.firstElementChild;
            const cardCs = window.getComputedStyle(firstCard);
            return {
                gridClass: grid.className,
                display: cs.display,
                gridTemplateColumns: cs.gridTemplateColumns,
                firstCardWidth: cardCs.width
            };
        }""")
        print("kpiGrid info:", info)
        await browser.close()

asyncio.run(inspect())
