import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Mobile verification (390x844)
        page_mob = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_mob.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page_mob.wait_for_timeout(800)
        
        # Check scrollWidth
        scroll_width = await page_mob.evaluate('() => document.documentElement.scrollWidth')
        inner_width = await page_mob.evaluate('() => window.innerWidth')
        print(f'Mobile scrollWidth: {scroll_width}, innerWidth: {inner_width}')
        assert scroll_width == inner_width, f"Horizontal overflow! scrollWidth {scroll_width} != innerWidth {inner_width}"
        
        # Verify removed elements are gone
        hub_header = await page_mob.query_selector('.hub-header')
        dept_tabs = await page_mob.query_selector('.dept-quick-tabs')
        back_btn = await page_mob.query_selector('.hub-back-btn')
        print(f'hub-header in DOM: {hub_header is not None}')
        print(f'dept-quick-tabs in DOM: {dept_tabs is not None}')
        print(f'hub-back-btn in DOM: {back_btn is not None}')
        assert hub_header is None, "hub-header should be removed!"
        assert dept_tabs is None, "dept-quick-tabs should be removed!"
        assert back_btn is None, "hub-back-btn should be removed!"

        await page_mob.screenshot(path='scratch/dept_fixed_mobile.png', full_page=True)
        print('Saved scratch/dept_fixed_mobile.png')

        # Test mobile hamburger
        hamb = await page_mob.query_selector('#htbHamburger, .htb-hamburger, [data-action="toggle-sidebar"]')
        if hamb:
            print('Testing mobile hamburger...')
            await hamb.click()
            await page_mob.wait_for_timeout(500)
            await page_mob.screenshot(path='scratch/dept_mobile_drawer_open.png')
            print('Saved scratch/dept_mobile_drawer_open.png')

        # 2. Desktop verification (1440x900)
        page_desk = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_desk.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page_desk.wait_for_timeout(800)
        await page_desk.screenshot(path='scratch/dept_fixed_desktop.png', full_page=True)
        print('Saved scratch/dept_fixed_desktop.png')

        await browser.close()
        print('All department tests passed!')

asyncio.run(main())

