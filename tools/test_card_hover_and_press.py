import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # 1. Department page test
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        
        print('\n=== TEST 1: Department Page (http://127.0.0.1:3000/pages/shared/department.html) ===', flush=True)
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)
        # Prevent link navigation during click/press testing
        await page.evaluate("() => document.addEventListener('click', e => e.preventDefault(), true)")
        
        card = page.locator('#cardAttendance')
        assert await card.count() > 0, "Card #cardAttendance not found"
        
        # Check Default state
        bg_default = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        trans_default = await card.evaluate('el => window.getComputedStyle(el).transform')
        print(f'1. Default State: BG = {bg_default}, Transform = {trans_default}')
        assert '255, 255, 255' in bg_default, f"Expected solid white background, got {bg_default}"
        
        # Check children backgrounds in default state
        children_bgs = await card.evaluate('''el => {
            return {
                top: window.getComputedStyle(el.querySelector('.hub-card-top')).backgroundColor,
                body: window.getComputedStyle(el.querySelector('.hub-card-body')).backgroundColor,
                footer: window.getComputedStyle(el.querySelector('.hub-card-footer')).backgroundColor,
                title: window.getComputedStyle(el.querySelector('.hub-card-title')).backgroundColor,
                desc: window.getComputedStyle(el.querySelector('.hub-card-desc')).backgroundColor
            };
        }''')
        print(f'   Children BGs in default state: {children_bgs}')
        assert 'rgba(0, 0, 0, 0)' in children_bgs['body'], f"Body should be transparent, got {children_bgs['body']}"
        assert 'rgba(0, 0, 0, 0)' in children_bgs['top'], f"Top should be transparent, got {children_bgs['top']}"
        assert 'rgba(0, 0, 0, 0)' in children_bgs['footer'], f"Footer should be transparent, got {children_bgs['footer']}"
        
        # Hover state
        await card.hover()
        await page.wait_for_timeout(300)
        bg_hover = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        trans_hover = await card.evaluate('el => window.getComputedStyle(el).transform')
        print(f'2. Hover State: BG = {bg_hover}, Transform = {trans_hover}')
        assert '255, 255, 255' in bg_hover, f"Card background must remain solid white on hover! Got {bg_hover}"
        assert trans_hover != 'none', f"Card should have hover transform, got {trans_hover}"
        await page.screenshot(path='tools/dept_card_hovered.png')
        
        # Press / Pointerdown state
        box = await card.bounding_box()
        await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        await page.mouse.down()
        await page.wait_for_timeout(200)
        bg_pressed = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        trans_pressed = await card.evaluate('el => window.getComputedStyle(el).transform')
        opacity_pressed = await card.evaluate('el => window.getComputedStyle(el).opacity')
        print(f'3. Pressed State: BG = {bg_pressed}, Transform = {trans_pressed}, Opacity = {opacity_pressed}')
        assert '255, 255, 255' in bg_pressed, f"Card background must remain solid white when pressed! Got {bg_pressed}"
        assert opacity_pressed == '1', f"Card opacity should remain 1, got {opacity_pressed}"
        await page.screenshot(path='tools/dept_card_pressed.png')
        
        # Release state
        await page.mouse.up()
        await page.wait_for_timeout(300)
        bg_released = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        trans_released = await card.evaluate('el => window.getComputedStyle(el).transform')
        print(f'4. Released State: BG = {bg_released}, Transform = {trans_released}')
        assert '255, 255, 255' in bg_released, f"Card background must remain solid white on release! Got {bg_released}"
        
        # Mouse leave
        await page.mouse.move(10, 10)
        await page.wait_for_timeout(400)
        trans_leave = await card.evaluate('el => window.getComputedStyle(el).transform')
        print(f'5. Mouse Leave State: Transform = {trans_leave}')
        assert trans_leave == 'none' or 'matrix(1,' in trans_leave, f"Card should return to original, got {trans_leave}"
        
        # Dark mode test
        print('\n=== TEST 2: Department Page in Dark Mode ===')
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('ngis-theme', 'dark');
        }""")
        await page.wait_for_timeout(400)
        
        bg_dark_default = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        print(f'1. Dark Mode Default: BG = {bg_dark_default}')
        assert 'rgb(0, 0, 0)' in bg_dark_default or 'rgb(15, 23, 42)' in bg_dark_default, f"Expected dark bg, got {bg_dark_default}"
        
        # Check dark mode children (should NOT have white patches)
        dark_children = await card.evaluate('''el => {
            return {
                body: window.getComputedStyle(el.querySelector('.hub-card-body')).backgroundColor,
                title: window.getComputedStyle(el.querySelector('.hub-card-title')).backgroundColor
            };
        }''')
        print(f'   Dark Mode Children: {dark_children}')
        assert 'rgba(0, 0, 0, 0)' in dark_children['body'], f"Body must be transparent, got {dark_children['body']}"
        
        # Dark mode hover
        theme_before_hover = await page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        print(f"Theme before hover: {theme_before_hover}")
        await card.hover()
        await page.wait_for_timeout(300)
        theme_after_hover = await page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        print(f"Theme after hover: {theme_after_hover}")
        bg_dark_hover = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        print(f'2. Dark Mode Hover: BG = {bg_dark_hover}')
        assert '255, 255, 255' not in bg_dark_hover, f"Dark card must NOT turn white on hover! Got {bg_dark_hover}"
        await page.screenshot(path='tools/dept_card_dark_hovered.png')
        
        # Dark mode press
        await page.mouse.down()
        await page.wait_for_timeout(200)
        bg_dark_pressed = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        print(f'3. Dark Mode Pressed: BG = {bg_dark_pressed}')
        assert 'transparent' not in bg_dark_pressed and bg_dark_pressed != 'rgba(0, 0, 0, 0)', "Dark card must NOT become transparent on press"
        await page.mouse.up()
        await page.mouse.move(10, 10)
        await page.wait_for_timeout(300)
        
        # 3. Landing page portal cards test
        print('\n=== TEST 3: Landing Page Portal Cards (http://127.0.0.1:3000/index.html) ===', flush=True)
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(800)
        await page.evaluate("() => document.addEventListener('click', e => e.preventDefault(), true)")
        
        pcard = page.locator('.portal-card').first
        if await pcard.count() > 0:
            bg_p = await pcard.evaluate('el => window.getComputedStyle(el).backgroundColor')
            await pcard.hover()
            await page.wait_for_timeout(200)
            trans_phover = await pcard.evaluate('el => window.getComputedStyle(el).transform')
            print(f'Portal Card Default BG = {bg_p}, Hover Transform = {trans_phover}')
            
            # Press
            pbox = await pcard.bounding_box()
            await page.mouse.move(pbox['x'] + pbox['width']/2, pbox['y'] + pbox['height']/2)
            await page.mouse.down()
            await page.wait_for_timeout(150)
            trans_ppress = await pcard.evaluate('el => window.getComputedStyle(el).transform')
            print(f'Portal Card Pressed Transform = {trans_ppress}')
            await page.mouse.up()
        
        print('\n=== TEST 4: Console Error Check ===')
        print('Total console errors encountered:', len(errors))
        if errors:
            for err in errors:
                print('Error:', err)
        assert len(errors) == 0, "Console errors were logged!"
        
        await browser.close()
        print('\n ALL CARD HOVER & PRESS INTERACTION TESTS PASSED!')

asyncio.run(main())
