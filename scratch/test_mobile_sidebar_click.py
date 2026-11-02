import asyncio
from playwright.async_api import async_playwright

async def test_mobile_sidebar():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for role, url in [
            ('teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
            ('student', 'http://127.0.0.1:3000/pages/student/student.html'),
            ('principal', 'http://127.0.0.1:3000/pages/principal/principal.html'),
            ('index', 'http://127.0.0.1:3000/index.html')
        ]:
            page = await browser.new_page(viewport={'width': 390, 'height': 844})
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(1000)
            
            # Find the visible hamburger button on mobile
            btn = await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn'));
                const vis = btns.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0);
                return vis.length ? { id: vis[0].id, cls: vis[0].className, text: vis[0].innerText } : null;
            }''')
            print(f'=== {role.upper()} ===')
            print('Visible hamburger button:', btn)
            
            # Click the visible button
            before_state = await page.evaluate('''() => {
                const sb = document.getElementById('sidebar');
                const sc = document.getElementById('scrim');
                return {
                    sidebarExists: !!sb,
                    sidebarCls: sb ? sb.className : null,
                    scrimExists: !!sc,
                    scrimCls: sc ? sc.className : null
                };
            }''')
            print('Before click:', before_state)
            
            # Click it
            await page.evaluate('''() => {
                const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn'));
                const vis = btns.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0);
                if (vis.length) vis[0].click();
            }''')
            await page.wait_for_timeout(500)
            
            after_state = await page.evaluate('''() => {
                const sb = document.getElementById('sidebar');
                const sc = document.getElementById('scrim');
                if (!sb) return null;
                const r = sb.getBoundingClientRect();
                const cs = getComputedStyle(sb);
                return {
                    cls: sb.className,
                    scrimCls: sc ? sc.className : null,
                    rect: { x: r.x, y: r.y, w: r.width, h: r.height },
                    computed: {
                        visibility: cs.visibility,
                        display: cs.display,
                        opacity: cs.opacity,
                        transform: cs.transform,
                        zIndex: cs.zIndex,
                        width: cs.width
                    }
                };
            }''')
            print('After click:', after_state)
            
            # Take screenshot
            await page.screenshot(path=f'scratch/mobile_sidebar_{role}_clicked.png')
            
        await browser.close()

asyncio.run(test_mobile_sidebar())

