import asyncio
from playwright.async_api import async_playwright

async def test_small_screens():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for w in [320, 360, 375, 414]:
            context = await browser.new_context(viewport={"width": w, "height": 700})
            page = await context.new_page()
            await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
            await page.wait_for_timeout(400)
            scroll_w = await page.evaluate("() => document.documentElement.scrollWidth")
            client_w = await page.evaluate("() => document.documentElement.clientWidth")
            overflow = max(0, scroll_w - client_w)
            print(f"Viewport {w}px: clientWidth={client_w}px, scrollWidth={scroll_w}px, overflow={overflow}px")
            await page.close()
            await context.close()
        await browser.close()

asyncio.run(test_small_screens())
