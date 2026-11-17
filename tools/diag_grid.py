import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        diag = await page.evaluate("""() => {
            const el = document.getElementById('kpiGrid');
            const cs = window.getComputedStyle(el);
            return {
                display: cs.display,
                gtc: cs.gridTemplateColumns,
                gtr: cs.gridTemplateRows,
                width: cs.width,
                cardCount: el.children.length,
                card1_top: el.children[0].getBoundingClientRect().top,
                card2_top: el.children[1].getBoundingClientRect().top,
                card1_left: el.children[0].getBoundingClientRect().left,
                card2_left: el.children[1].getBoundingClientRect().left,
            };
        }""")
        print("Diagnostic:", diag)
        await browser.close()

asyncio.run(inspect())
