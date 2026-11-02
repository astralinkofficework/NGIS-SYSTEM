import asyncio
from playwright.async_api import async_playwright

async def test_close_behavior():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(500)
        
        # 1. Click hamburger to open
        hb = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('[data-action="toggle-sidebar"], .hamburger-btn'));
            const vis = btns.filter(b => b.offsetWidth > 0 && b.offsetHeight > 0);
            if (vis.length) {
                vis[0].click();
                return true;
            }
            return false;
        }''')
        await page.wait_for_timeout(300)
        print('Opened drawer:', hb)
        
        # 2. Inside the drawer, what is visible?
        collapse_btn = await page.query_selector('#sidebarCollapseBtn')
        is_collapse_vis = await collapse_btn.is_visible() if collapse_btn else False
        print('sidebarCollapseBtn visible inside open drawer:', is_collapse_vis)
        
        if is_collapse_vis:
            # Click it!
            await collapse_btn.click()
            await page.wait_for_timeout(300)
            state = await page.evaluate('''() => {
                const sb = document.getElementById('sidebar');
                const sc = document.getElementById('scrim');
                return {
                    sbOpen: sb.classList.contains('open'),
                    sbCollapsed: sb.classList.contains('collapsed'),
                    scrimShow: sc.classList.contains('show'),
                    sbWidth: sb.offsetWidth,
                    bodySidebarOpen: document.body.classList.contains('sidebar-open')
                };
            }''')
            print('State after clicking collapseBtn:', state)
            await page.screenshot(path='scratch/after_collapse_click.png')
        
        await browser.close()

asyncio.run(test_close_behavior())

