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
            const matched = [];
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.selectorText && el.matches(rule.selectorText)) {
                            if (rule.style.gridTemplateColumns || rule.style.display) {
                                matched.push({ sel: rule.selectorText, gtc: rule.style.gridTemplateColumns, disp: rule.style.display });
                            }
                        }
                    }
                } catch(_) {}
            }
            return matched;
        }""")
        print("Matched rules on #kpiGrid:", rules)
        await browser.close()

asyncio.run(inspect())
