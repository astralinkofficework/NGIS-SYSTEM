import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        has_rule = await page.evaluate("""() => {
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.selectorText && rule.selectorText.includes('grid-cols-2')) {
                            return { selector: rule.selectorText, cssText: rule.cssText };
                        }
                    }
                } catch(_) {}
            }
            return null;
        }""")
        print("grid-cols-2 rule:", has_rule)
        await browser.close()

asyncio.run(inspect())
