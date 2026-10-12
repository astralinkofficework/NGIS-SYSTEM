import asyncio
from playwright.async_api import async_playwright

async def test_id_modal():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Test desktop Digital ID click
        page = await browser.new_page(viewport={'width': 1268, 'height': 706})
        await page.goto('http://localhost:3000/pages/student/student.html')
        await page.wait_for_timeout(1000)
        btn = page.locator('#viewIdBtn')
        await btn.click()
        await page.wait_for_timeout(500)
        modal_visible = await page.locator('#idModal').is_visible()
        print('Desktop ID Modal visible after click:', modal_visible)
        await page.close()
        
        # Test mobile Digital ID click
        page_mobile = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_mobile.goto('http://localhost:3000/pages/student/student.html')
        await page_mobile.wait_for_timeout(1000)
        m_btn = page_mobile.locator('button:has-text("Digital ID")')
        await m_btn.first.click()
        await page_mobile.wait_for_timeout(500)
        m_modal_visible = await page_mobile.locator('#idModal').is_visible()
        print('Mobile ID Modal visible after click:', m_modal_visible)
        await page_mobile.close()
        
        await browser.close()

asyncio.run(test_id_modal())
