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
            const card = document.querySelector('#kpiGrid > div');
            const cs = window.getComputedStyle(card);
            const rules = [];
            for (const s of document.styleSheets) {
                try {
                    for (const r of s.cssRules) {
                        if (r.selectorText && card.matches(r.selectorText)) {
                            rules.push({ sel: r.selectorText, cssText: r.cssText });
                        }
                    }
                } catch(e) {}
            }
            return {
                csGridColumn: cs.gridColumn,
                csGridColumnStart: cs.gridColumnStart,
                csGridColumnEnd: cs.gridColumnEnd,
                rules: rules
            };
        }""")
        print("Card computed grid columns:", res)
        await browser.close()

asyncio.run(inspect())
