import asyncio
from playwright.async_api import async_playwright

async def verify_drawers():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        results = {}
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
            
            # 1. Click visible hamburger button
            opened = await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn'));
                const vis = btns.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0);
                if (vis.length) {
                    vis[0].click();
                    return true;
                }
                return false;
            }''')
            await page.wait_for_timeout(400)
            
            # Check open state
            open_state = await page.evaluate('''() => {
                const sb = document.getElementById('sidebar');
                const sc = document.getElementById('scrim');
                const cb = document.getElementById('sidebarCloseBtn');
                if (!sb) return null;
                const r = sb.getBoundingClientRect();
                const cs = getComputedStyle(sb);
                return {
                    isOpenClass: sb.classList.contains('open'),
                    x: r.x,
                    y: r.y,
                    w: r.width,
                    h: r.height,
                    vis: cs.visibility,
                    display: cs.display,
                    scrimShow: sc ? sc.classList.contains('show') : false,
                    closeBtnVis: cb ? (cb.offsetWidth > 0 && cb.offsetHeight > 0) : false
                };
            }''')
            
            # 2. Click the close button
            closed = await page.evaluate('''() => {
                const cb = document.getElementById('sidebarCloseBtn');
                if (cb && cb.offsetWidth > 0) {
                    cb.click();
                    return true;
                }
                const sc = document.getElementById('scrim');
                if (sc) {
                    sc.click();
                    return true;
                }
                return false;
            }''')
            await page.wait_for_timeout(400)
            
            # Check closed state
            close_state = await page.evaluate('''() => {
                const sb = document.getElementById('sidebar');
                const sc = document.getElementById('scrim');
                if (!sb) return null;
                const r = sb.getBoundingClientRect();
                const cs = getComputedStyle(sb);
                return {
                    isOpenClass: sb.classList.contains('open'),
                    x: r.x,
                    vis: cs.visibility,
                    scrimShow: sc ? sc.classList.contains('show') : false
                };
            }''')
            
            # Capture screenshot while open to save as proof
            # Re-open for screenshot
            await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn'));
                const vis = btns.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0);
                if (vis.length) vis[0].click();
            }''')
            await page.wait_for_timeout(300)
            await page.screenshot(path=f'scratch/mobile_drawer_{role}_open.png')
            
            results[role] = {
                'opened': opened,
                'open_state': open_state,
                'closed': closed,
                'close_state': close_state
            }
            print(f'[{role.upper()}] Open: {open_state}, Closed: {close_state}')
            
        await browser.close()
        print('All verification complete!')

asyncio.run(verify_drawers())

