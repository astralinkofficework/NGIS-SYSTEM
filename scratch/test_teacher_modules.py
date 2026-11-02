import asyncio
from playwright.async_api import async_playwright

async def test_modules():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Test Teacher Lost & Found
        print("\n--- Testing Teacher Lost & Found ---")
        page_lf = await browser.new_page(viewport={'width': 1280, 'height': 850})
        errors_lf = []
        page_lf.on('console', lambda msg: errors_lf.append(f"CONSOLE: {msg.text}") if msg.type == 'error' else None)
        page_lf.on('pageerror', lambda exc: errors_lf.append(f"PAGEERROR: {exc}"))
        
        await page_lf.goto('http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html', wait_until='networkidle')
        await page_lf.wait_for_timeout(1000)
        await page_lf.screenshot(path='scratch/teacher_lost_found_desktop.png')
        
        card_count = await page_lf.locator('.item-card').count()
        print(f"Desktop Lost & Found loaded! Item cards found: {card_count}")
        
        # Open Report modal
        await page_lf.click('button:has-text("Report Found Item")')
        await page_lf.wait_for_timeout(400)
        modal_visible = await page_lf.is_visible('#reportModal.show')
        print(f"Report modal opened: {modal_visible}")
        await page_lf.click('#reportModal button:has-text("close")')
        await page_lf.wait_for_timeout(300)
        
        # Test mobile viewport for Lost & Found
        page_lf_mob = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_lf_mob.goto('http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html', wait_until='networkidle')
        await page_lf_mob.wait_for_timeout(1000)
        await page_lf_mob.screenshot(path='scratch/teacher_lost_found_mobile.png')
        
        # Test Hamburger menu
        hamburger_lf = page_lf_mob.locator('[data-action="toggle-sidebar"]')
        has_hb_lf = await hamburger_lf.count() > 0 and await hamburger_lf.first.is_visible()
        print(f"Mobile Hamburger visible on Lost & Found: {has_hb_lf}")
        if has_hb_lf:
            await hamburger_lf.first.click()
            await page_lf_mob.wait_for_timeout(500)
            drawer_open = await page_lf_mob.evaluate("() => { const s = document.getElementById('sidebar'); return s && (s.classList.contains('open') || s.classList.contains('active') || window.getComputedStyle(s).transform.indexOf('matrix') !== -1); }")
            print(f"Sidebar drawer opened on Lost & Found: {drawer_open}")
            await page_lf_mob.screenshot(path='scratch/teacher_lost_found_drawer.png')
        
        # 2. Test Teacher Services Hub
        print("\n--- Testing Teacher Services Hub ---")
        page_srv = await browser.new_page(viewport={'width': 1280, 'height': 850})
        errors_srv = []
        page_srv.on('console', lambda msg: errors_srv.append(f"CONSOLE: {msg.text}") if msg.type == 'error' else None)
        page_srv.on('pageerror', lambda exc: errors_srv.append(f"PAGEERROR: {exc}"))
        
        await page_srv.goto('http://127.0.0.1:3000/pages/teacher/teacher-services.html', wait_until='networkidle')
        await page_srv.wait_for_timeout(1000)
        await page_srv.screenshot(path='scratch/teacher_services_desktop.png')
        
        req_count = await page_srv.locator('.req-card').count()
        print(f"Desktop Services Hub loaded! Request cards found: {req_count}")
        
        # Open New Request modal
        await page_srv.click('button:has-text("Submit Service Request")')
        await page_srv.wait_for_timeout(400)
        srv_modal_vis = await page_srv.is_visible('#newRequestModal.show')
        print(f"New Request modal opened: {srv_modal_vis}")
        await page_srv.click('#newRequestModal button:has-text("close")')
        await page_srv.wait_for_timeout(300)
        
        # Test mobile viewport for Services Hub
        page_srv_mob = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_srv_mob.goto('http://127.0.0.1:3000/pages/teacher/teacher-services.html', wait_until='networkidle')
        await page_srv_mob.wait_for_timeout(1000)
        await page_srv_mob.screenshot(path='scratch/teacher_services_mobile.png')
        
        hamburger_srv = page_srv_mob.locator('[data-action="toggle-sidebar"]')
        has_hb_srv = await hamburger_srv.count() > 0 and await hamburger_srv.first.is_visible()
        print(f"Mobile Hamburger visible on Services Hub: {has_hb_srv}")
        if has_hb_srv:
            await hamburger_srv.first.click()
            await page_srv_mob.wait_for_timeout(500)
            await page_srv_mob.screenshot(path='scratch/teacher_services_drawer.png')
            
        # 3. Test Teacher Dashboard
        print("\n--- Testing Teacher Dashboard Links ---")
        page_tch = await browser.new_page(viewport={'width': 1280, 'height': 850})
        await page_tch.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        
        srv_link = await page_tch.locator('a[href*="teacher-services.html"]').count()
        lf_link = await page_tch.locator('a[href*="teacher-lost-found.html"]').count()
        print(f"Dashboard has Services Hub links: {srv_link}")
        print(f"Dashboard has Lost & Found links: {lf_link}")
        
        print("\nErrors in Lost & Found:", errors_lf)
        print("Errors in Services Hub:", errors_srv)
        
        await browser.close()

asyncio.run(test_modules())

