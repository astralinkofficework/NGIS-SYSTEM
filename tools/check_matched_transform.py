import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        card = page.locator('.portal-card').first
        await card.scroll_into_view_if_needed()
        await card.hover()
        await page.wait_for_timeout(200)
        
        rules = await card.evaluate("""el => {
            const res = [];
            for (let i = 0; i < document.styleSheets.length; i++) {
                const sheet = document.styleSheets[i];
                try {
                    for (let j = 0; j < sheet.cssRules.length; j++) {
                        const rule = sheet.cssRules[j];
                        if (rule.style && rule.style.transform && rule.style.transform !== '') {
                            // Check if selector matches el
                            try {
                                if (el.matches(rule.selectorText)) {
                                    res.push({
                                        href: sheet.href || 'inline',
                                        selector: rule.selectorText,
                                        transform: rule.style.transform,
                                        priority: rule.style.getPropertyPriority('transform')
                                    });
                                }
                            } catch(e) {}
                        }
                    }
                } catch(e) {}
            }
            return res;
        }""")
        print("Matching transform rules:")
        for r in rules:
            print(" ", r)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
