import asyncio
from playwright.async_api import async_playwright

async def detect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        pages_to_test = [
            'http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-10a',
            'http://127.0.0.1:3000/pages/teacher/teacher.html',
            'http://127.0.0.1:3000/pages/student/student.html'
        ]
        
        for url in pages_to_test:
            print(f"\nTesting URL: {url}")
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(800)
            
            # Find cards on the page
            cards = await page.locator('.ws-card, .card, .stat-card, .sh-card, .ql-card, .item-card, [class*="card"]').element_handles()
            print(f"Found {len(cards)} card elements")
            
            if cards:
                card = cards[0]
                # Check style before hover
                style_before = await card.evaluate("el => window.getComputedStyle(el).background")
                
                # Hover over card
                await card.hover()
                await page.wait_for_timeout(300)
                style_hover = await card.evaluate("el => window.getComputedStyle(el).background")
                
                # Check before/after pseudo elements
                pseudo_info = await card.evaluate("""el => {
                    const before = window.getComputedStyle(el, '::before');
                    const after = window.getComputedStyle(el, '::after');
                    return {
                        beforeContent: before.content,
                        beforeBg: before.background,
                        beforeRadius: before.borderRadius,
                        afterContent: after.content,
                        afterBg: after.background,
                        afterRadius: after.borderRadius,
                    };
                }""")
                print("Pseudo info on hover:", pseudo_info)
                
                # Click / mousedown
                box = await card.bounding_box()
                if box:
                    await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                    await page.mouse.down()
                    await page.wait_for_timeout(300)
                    
                    # Check any ripple elements added to DOM
                    children_info = await card.evaluate("""el => {
                        const styleActive = window.getComputedStyle(el).background;
                        const children = Array.from(el.querySelectorAll('*')).map(c => ({
                            tag: c.tagName,
                            cls: c.className,
                            bg: window.getComputedStyle(c).background,
                            radius: window.getComputedStyle(c).borderRadius
                        }));
                        return { styleActive, childrenCount: children.length, children: children.slice(0, 5) };
                    }""")
                    print("During mousedown:", children_info['styleActive'])
                    await page.mouse.up()
                    
        await browser.close()

asyncio.run(detect())

