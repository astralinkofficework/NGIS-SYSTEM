import asyncio
from playwright.async_api import async_playwright

async def audit_pages():
    card_selector = ".card:not([class*='-body']):not([class*='-head']):not([class*='-footer']):not([class*='-title']):not([class*='-desc']):not([class*='-icon']):not([class*='-meta']):visible, .hub-card:visible, .dept-card:visible, .portal-card:visible, .module-card:visible, .smx-card:visible"
    
    pages_to_test = [
        ("Student Portal", "http://127.0.0.1:3000/pages/student/student.html", card_selector),
        ("Student Attendance", "http://127.0.0.1:3000/pages/student/student-attendance.html", card_selector),
        ("Student Exams", "http://127.0.0.1:3000/pages/student/student-exams.html", f"{card_selector}, .exw-roadmap-row:visible"),
        ("Teacher Portal", "http://127.0.0.1:3000/pages/teacher/teacher.html", card_selector),
        ("Admin Portal", "http://127.0.0.1:3000/pages/admin/admin.html", card_selector),
        ("Landing Page", "http://127.0.0.1:3000/index.html", ".portal-card:visible")
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        for name, url, selector in pages_to_test:
            print(f"\n--- AUDITING: {name} ({url}) ---")
            errors = []
            page.on('pageerror', lambda err: errors.append(str(err)))
            page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
            
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(800)
            await page.evaluate("() => document.addEventListener('click', e => e.preventDefault(), true)")
            
            cards = page.locator(selector)
            count = await cards.count()
            print(f"Found {count} cards matching '{selector}'")
            if count > 0:
                card = cards.first
                bg_def = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
                
                # Test hover
                await card.hover()
                await page.wait_for_timeout(150)
                bg_hov = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
                trans_hov = await card.evaluate('el => window.getComputedStyle(el).transform')
                
                # Test press
                box = await card.bounding_box()
                if box:
                    await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
                    await page.mouse.down()
                    await page.wait_for_timeout(150)
                    bg_press = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
                    opacity_press = await card.evaluate('el => window.getComputedStyle(el).opacity')
                    await page.mouse.up()
                else:
                    bg_press = bg_hov
                    opacity_press = '1'
                
                print(f"  Default BG: {bg_def} | Hover BG: {bg_hov} | Pressed BG: {bg_press} | Opacity: {opacity_press}")
                assert 'transparent' not in bg_hov and bg_hov != 'rgba(0, 0, 0, 0)', f"Card in {name} became transparent on hover!"
                assert 'transparent' not in bg_press and bg_press != 'rgba(0, 0, 0, 0)', f"Card in {name} became transparent on press!"
                assert opacity_press == '1', f"Card in {name} had non-1 opacity on press ({opacity_press})"
            
            # Check for console errors
            if errors:
                print(f"  Console errors on {name}: {errors}")
            else:
                print(f"  Zero console errors on {name}!")
                
        await browser.close()
        print("\n CROSS-PORTAL CARD INTERACTION AUDIT COMPLETE & ALL PASSED!")

asyncio.run(audit_pages())
