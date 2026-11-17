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
            const decls = [];
            for (const s of document.styleSheets) {
                try {
                    for (const r of s.cssRules) {
                        if (r.style && r.style.gridTemplateColumns && el.matches(r.selectorText)) {
                            decls.push({ sel: r.selectorText, val: r.style.gridTemplateColumns, media: r.parentRule ? r.parentRule.conditionText : '' });
                        }
                    }
                } catch(e) {}
            }
            return decls;
        }""")
        print("All matching gridTemplateColumns rules:", res)
        await browser.close()

asyncio.run(inspect())
