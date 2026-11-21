import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-security.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Check transparent navbar
        navbar_bg = await page.evaluate('''() => {
            const h = document.querySelector('#heroBanner, header.topbar, .topbar');
            return h ? window.getComputedStyle(h).backgroundColor : 'none';
        }''')
        print(f"Top navbar computed background: {navbar_bg}")
        
        # Check threat investigation drawer trigger
        row = page.locator("#secEventsList tr, .sec-event-row").first
        if await row.count() > 0:
            await row.click()
            await page.wait_for_timeout(500)
            drawer = page.locator("#threatForensicsDrawer, #investigationDrawer")
            drawer_visible = await drawer.is_visible()
            print(f"Threat forensics drawer visible on click: {drawer_visible}")
            
        # Check heavy font weights (> 500)
        heavy_count = await page.evaluate('''() => {
            let count = 0;
            document.querySelectorAll('*').forEach(el => {
                if (parseInt(window.getComputedStyle(el).fontWeight, 10) > 500) count++;
            });
            return count;
        }''')
        print(f"Elements with fontWeight > 500: {heavy_count}")
        
        if errors:
            print(f"Errors detected: {errors}")
        else:
            print("Security center verified with zero errors!")
            
        await browser.close()

asyncio.run(main())
