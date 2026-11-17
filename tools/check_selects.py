import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # Inspect select styles and child SVG
        select_info = await page.evaluate("""() => {
            const selects = Array.from(document.querySelectorAll('select#deptFilter, select#statusFilter, select#sortSelect'));
            return selects.map(s => {
                const cs = window.getComputedStyle(s);
                const nextSpan = s.nextElementSibling;
                const hasSvg = nextSpan && nextSpan.querySelector('svg') !== null;
                return {
                    id: s.id,
                    bgImage: cs.backgroundImage,
                    appearance: cs.appearance || cs.webkitAppearance,
                    hasSvgSibling: hasSvg
                };
            });
        }""")
        print("Select elements audit:")
        for s in select_info:
            print(f"  ID: {s['id']}, bgImage: {s['bgImage'][:40]}..., appearance: {s['appearance']}, hasSvgSibling: {s['hasSvgSibling']}")

        await browser.close()

asyncio.run(inspect())
