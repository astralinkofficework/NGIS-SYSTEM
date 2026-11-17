import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        res = await page.evaluate("""() => {
            const el = document.getElementById('kpiGrid');
            // test what happens if we set style.gridTemplateColumns = 'repeat(2, minmax(0, 1fr))'
            el.style.gridTemplateColumns = 'repeat(2, minmax(0, 1fr))';
            return {
                computedAfterInline: window.getComputedStyle(el).gridTemplateColumns,
                card1Width: el.firstElementChild.offsetWidth,
                card2Width: el.children[1].offsetWidth
            };
        }""")
        print("Inline test result:", res)
        await browser.close()

asyncio.run(inspect())
