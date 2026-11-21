import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        # Try both default and with dept query
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html')
        await page.wait_for_timeout(1000)
        
        cards = await page.locator('.card, [class*="card"], .module-card, .dept-card, a.block, .rounded-xl, .rounded-2xl').all()
        print('Total candidate card elements found:', len(cards))
        
        # Check first 8 elements
        for i, card in enumerate(cards[:15]):
            tag = await card.evaluate('el => el.tagName')
            cls = await card.evaluate('el => el.className')
            text = (await card.inner_text()).strip().replace('\n', ' ')[:40]
            bg_normal = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
            
            # Hover over it
            await card.hover()
            await page.wait_for_timeout(200)
            bg_hover = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
            transform_hover = await card.evaluate('el => window.getComputedStyle(el).transform')
            
            # Also check children backgrounds
            child_bgs = await card.evaluate("""el => {
                return Array.from(el.children).map(c => ({
                    tag: c.tagName,
                    cls: c.className,
                    bg: window.getComputedStyle(c).backgroundColor
                }));
            }""")
            
            print(f'Card {i}: <{tag} class="{cls[:40]}"> text="{text}"')
            print(f'   Normal BG: {bg_normal} -> Hover BG: {bg_hover} | Transform: {transform_hover}')
            print(f'   Children: {child_bgs[:3]}')

        # Take screenshot of hovering over the first interactive card (like attendance or curriculum)
        for card in cards:
            text = await card.inner_text()
            if 'Attendance' in text or 'Curriculum' in text or 'Notice' in text or 'Overview' in text:
                print('Found Attendance / target card!')
                await card.hover()
                await page.wait_for_timeout(400)
                await page.screenshot(path='tools/hover_target_card.png')
                
                # Check active state
                box = await card.bounding_box()
                if box:
                    await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                    await page.mouse.down()
                    await page.wait_for_timeout(200)
                    bg_active = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
                    trans_active = await card.evaluate('el => window.getComputedStyle(el).transform')
                    print(f'   Active BG: {bg_active} | Transform: {trans_active}')
                    await page.screenshot(path='tools/active_target_card.png')
                    await page.mouse.up()
                break

        await browser.close()

asyncio.run(main())
