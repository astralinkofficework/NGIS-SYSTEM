import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop test (1440x900)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/teacher_desktop.png', full_page=True)
        print('Saved scratch/teacher_desktop.png')
        
        # Test ID Modal on desktop
        view_id_btn = await page.query_selector('#viewIdBtn')
        if view_id_btn:
            await view_id_btn.click()
            await page.wait_for_timeout(500)
            await page.screenshot(path='scratch/teacher_id_modal.png')
            print('Saved scratch/teacher_id_modal.png')
            
            # Flip card
            card_wrap = await page.query_selector('#idCardWrap')
            if card_wrap:
                await card_wrap.click()
                await page.wait_for_timeout(600)
                await page.screenshot(path='scratch/teacher_id_modal_flipped.png')
                print('Saved scratch/teacher_id_modal_flipped.png')
            
            # Close modal
            close_btn = await page.query_selector('#idCloseBtn')
            if close_btn:
                await close_btn.click()
                await page.wait_for_timeout(300)

        # 2. Mobile test (390x844)
        page_mobile = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_mobile.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page_mobile.wait_for_timeout(1000)
        await page_mobile.screenshot(path='scratch/teacher_mobile.png', full_page=True)
        print('Saved scratch/teacher_mobile.png')
        
        # Test mobile hamburger button
        hamb = await page_mobile.query_selector('.htb-hamburger, [data-action="toggle-sidebar"]')
        if hamb:
            print('Clicking mobile hamburger button...')
            await hamb.click()
            await page_mobile.wait_for_timeout(500)
            await page_mobile.screenshot(path='scratch/teacher_mobile_sidebar.png')
            print('Saved scratch/teacher_mobile_sidebar.png')

        await browser.close()
        print('All tests completed successfully!')

asyncio.run(main())
