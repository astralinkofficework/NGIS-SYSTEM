import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        card = page.locator('.portal-card').first
        await card.hover()
        await page.wait_for_timeout(200)
        
        rules = await page.evaluate("""() => {
            const el = document.querySelector('.portal-card');
            const matched = [];
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.selectorText && rule.selectorText.includes('portal-card') && rule.selectorText.includes('hover')) {
                            matched.push({ href: sheet.href, selector: rule.selectorText, cssText: rule.cssText.slice(0, 150) });
                        }
                    }
                } catch(e) {}
            }
            return matched;
        }""")
        print("Matching hover rules for portal-card:")
        for r in rules:
            print(" ", r)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
