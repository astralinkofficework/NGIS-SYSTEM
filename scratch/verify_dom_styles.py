import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        
        # Check computed styles of inner panels
        panels = await page.query_selector_all('.ov-inner-panel, .ov-deadline-panel')
        for i, panel in enumerate(panels):
            bg = await panel.evaluate('el => window.getComputedStyle(el).backgroundColor')
            border_top = await panel.evaluate('el => window.getComputedStyle(el).borderTopWidth')
            border_bottom = await panel.evaluate('el => window.getComputedStyle(el).borderBottomWidth')
            print(f'Panel {i}: bg={bg}, borderTop={border_top}, borderBottom={border_bottom}')

        # Check font weights across key headings and labels
        elements = await page.query_selector_all('h1, h2, h3, h4, .ov-profile-name, .ov-card-title, .sec-head h3')
        heavy_weights = []
        for el in elements:
            tag = await el.evaluate('el => el.tagName')
            text = (await el.inner_text()).strip()[:25]
            weight = await el.evaluate('el => window.getComputedStyle(el).fontWeight')
            if int(weight) > 500:
                heavy_weights.append((tag, text, weight))
            else:
                print(f'{tag} ("{text}"): weight={weight} (OK)')
                
        if heavy_weights:
            print(f'WARNING: Found heavy font weights: {heavy_weights}')
        else:
            print('SUCCESS: All font weights strictly <= 500 (No bold fonts)!')

        await browser.close()

asyncio.run(main())

