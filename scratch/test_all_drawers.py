import asyncio
from playwright.async_api import async_playwright

async def test_all_portals_sidebar():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for role, url in [
            ('index', 'http://127.0.0.1:3000/index.html'),
            ('directory', 'http://127.0.0.1:3000/pages-directory.html'),
            ('teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
            ('student', 'http://127.0.0.1:3000/pages/student/student.html'),
            ('principal', 'http://127.0.0.1:3000/pages/principal/principal.html'),
            ('admin', 'http://127.0.0.1:3000/pages/admin/admin.html')
        ]:
            page = await browser.new_page(viewport={'width': 390, 'height': 844})
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(500)
            
            # Find visible hamburger
            hb = await page.query_selector('[data-action="toggle-sidebar"]:visible, .hamburger-btn:visible, .mobile-hamburger-btn:visible')
            if not hb:
                # Try finding any toggle-sidebar
                all_hb = await page.query_selector_all('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn')
                for b in all_hb:
                    if await b.is_visible():
                        hb = b
                        break
            
            hb_found = hb is not None
            if hb:
                await hb.click()
                await page.wait_for_timeout(400)
            
            # Check sidebar state
            state = await page.evaluate('''() => {
                const sb = document.getElementById('sidebar') || document.querySelector('.sidebar') || document.querySelector('.mobile-nav-drawer');
                const sc = document.getElementById('scrim') || document.querySelector('.scrim');
                if (!sb) return { found: false };
                const cs = getComputedStyle(sb);
                const r = sb.getBoundingClientRect();
                return {
                    found: true,
                    isOpen: sb.classList.contains('open') || sb.classList.contains('active'),
                    display: cs.display,
                    visibility: cs.visibility,
                    transform: cs.transform,
                    width: r.width,
                    height: r.height,
                    x: r.x,
                    y: r.y,
                    scrimShow: sc ? (sc.classList.contains('show') || sc.classList.contains('active')) : false
                };
            }''')
            print(f'[{role}] hamburger_found={hb_found}, drawer_state={state}')
            
        await browser.close()

asyncio.run(test_all_portals_sidebar())

