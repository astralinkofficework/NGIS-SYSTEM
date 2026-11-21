import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-roles-permissions.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        heavy_elements = await page.evaluate('''() => {
            const heavy = [];
            document.querySelectorAll('*').forEach(el => {
                const fw = window.getComputedStyle(el).fontWeight;
                const num = parseInt(fw, 10);
                if (num > 500) {
                    heavy.push({ tag: el.tagName, text: el.textContent.trim().slice(0, 30), fw: fw, cls: el.className });
                }
            });
            return heavy.slice(0, 20);
        }''')
        
        print(f"Found {len(heavy_elements)} elements with fontWeight > 500:")
        for h in heavy_elements:
            print(f"  [{h['tag']}] fw={h['fw']} text='{h['text']}' cls='{h['cls']}'")
            
        await browser.close()

asyncio.run(main())
