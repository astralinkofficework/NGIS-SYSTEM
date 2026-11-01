import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page.wait_for_timeout(800)
        
        # Check window scrollWidth vs innerWidth
        scroll_width = await page.evaluate('() => document.documentElement.scrollWidth')
        inner_width = await page.evaluate('() => window.innerWidth')
        print(f'Mobile scrollWidth: {scroll_width}, innerWidth: {inner_width}')
        
        # Check overflow elements if any
        overflows = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('*'));
            return els.filter(el => {
                const rect = el.getBoundingClientRect();
                return rect.right > window.innerWidth + 1 || rect.left < -1;
            }).map(el => ({
                tag: el.tagName,
                cls: el.className,
                id: el.id,
                right: el.getBoundingClientRect().right
            })).slice(0, 10);
        }''')
        print('Overflow elements:', overflows)

        # Check hero banner topbar and elements
        hero = await page.query_selector('.hero')
        if hero:
            h_box = await hero.bounding_box()
            print('Hero box:', h_box)

        # Check cards grid
        grid = await page.query_selector('.hub-grid')
        if grid:
            g_box = await grid.bounding_box()
            print('Grid box:', g_box)

        # Check advisor strip
        adv = await page.query_selector('.hub-advisor-strip')
        if adv:
            a_box = await adv.bounding_box()
            print('Advisor box:', a_box)

        await browser.close()

asyncio.run(main())

