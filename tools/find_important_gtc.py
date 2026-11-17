import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 390, "height": 844})
        page = await context.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        rules = await page.evaluate("""() => {
            const el = document.getElementById('kpiGrid');
            const found = [];
            for (let i = 0; i < document.styleSheets.length; i++) {
                const s = document.styleSheets[i];
                try {
                    for (const r of s.cssRules) {
                        if (r.selectorText && el.matches(r.selectorText)) {
                            if (r.style.getPropertyPriority('grid-template-columns') === 'important') {
                                found.push({
                                    sheet: s.href || 'inline',
                                    sel: r.selectorText,
                                    val: r.style.getPropertyValue('grid-template-columns'),
                                    media: r.parentRule ? r.parentRule.conditionText : ''
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return found;
        }""")
        print("Found important rules:", rules)
        await browser.close()

asyncio.run(inspect())
